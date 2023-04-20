"""This file is in charge of server code run as daemon process."""

import os
import subprocess
import ast
from typing import Dict, List, Optional, Union
from concurrent import futures
from os import path as osp

import grpc
import psutil
import pynvml

from experiment_scheduler.common.logging import get_logger, start_end_logger
from experiment_scheduler.common.settings import USER_CONFIG
from experiment_scheduler.task_manager.grpc_task_manager import task_manager_pb2_grpc
from experiment_scheduler.task_manager.grpc_task_manager.task_manager_pb2 import (
    AllTasksStatus,
    IdleResources,
    ServerStatus,
    TaskLogFile,
    TaskStatus,
    ProgressResponse,
)
from experiment_scheduler.task_manager.return_code import ReturnCode

logger = get_logger(name="task_manager")

KILL_CHILD_MAX_DEPTH = 2
CHUNK_SIZE = 1024 * 5


class ProcessUtil:
    """Wrapper class for psutil.

    Args:
        pid (int): process id.
    """

    def __init__(self, pid: int):
        self._pid = pid
        try:
            self._process = psutil.Process(self._pid)
        except psutil.NoSuchProcess:
            self._process = None
        except psutil.AccessDenied:
            logger.warning("Access to process(%d) is denied.", pid)
            self._process = None

    @property
    def pid(self):
        """
        return process id
        :return: pid
        """
        return self._pid

    def kill_itself_with_child_process(self, max_depth: int) -> bool:
        """kill self recursively up to max depth.

        Args:
            max_depth (int): max depth of child processes to find and kill.

        Returns:
            bool:
                Whether success to kill process recursively.
        """
        if self._process is None:
            logger.warning("Fail to get process(%d).", self._pid)
            return False
        return self.kill_process_recursively(self._process, max_depth, 0)

    @staticmethod
    def kill_process_recursively(
        process: psutil.Process, max_depth: int, cur_depth: int = 0
    ) -> bool:
        """kill process recursively up to max depth.

        Args:
            max_depth (int): max depth of child processes to find and kill.
            cur_depth (int): current depth.

        Returns:
            bool:
                Whether success to kill process recursively.
        """
        if not process.is_running():
            return True

        if cur_depth < max_depth:
            for child_process in process.children():
                ProcessUtil.kill_process_recursively(
                    child_process, max_depth, cur_depth + 1
                )

        if process.is_running():
            process.terminate()
            process.wait()

        return True


class ResourceManager:
    """
    Resource Manager checks task manager's status.
    """

    def __init__(self, num_resource: int):
        self._resource_rental_history = {}
        self._available_resources = [True for _ in range(num_resource)]
        self.logger = get_logger(name="resource_manager")

    def set_resource_as_idle(self, resource_idx: int):
        """

        :param resource_idx:
        :return:
        """
        self._available_resources[resource_idx] = True

    def set_resource_as_used(self, resource_idx: int):
        """

        :param resource_idx:
        :return:
        """
        self._available_resources[resource_idx] = False

    def release_resource(self, task_id):
        """

        :param task_id:
        :return:
        """
        if task_id not in self._resource_rental_history:
            return
        resource_idx = self._resource_rental_history[task_id]
        self._available_resources[resource_idx] = True
        del self._resource_rental_history[task_id]

    def get_resource(self, task_id):
        """

        :param task_id:
        :return:
        """
        resource_idx = None
        for idx, resource_is_idle in enumerate(self._available_resources):
            if resource_is_idle:
                resource_idx = idx
                break
        if resource_idx is None:
            self.logger.info("There isn't any available resource.")
            return None

        self._resource_rental_history[task_id] = resource_idx
        self._available_resources[resource_idx] = False

        return resource_idx

    def has_available_resource(self):
        """

        :return:
        """
        for resource_is_idle in self._available_resources:
            if resource_is_idle:
                return True
        return False

    def get_tasks_using_resource(self):
        """

        :return:
        """
        return list(self._resource_rental_history.keys())


class Task:
    """Wrapper class for Task."""

    def __init__(self, process: subprocess.Popen):
        self._process = process
        self._history: List[Dict[str, float]] = []

    def get_return_code(self) -> Optional[int]:
        """Get return code."""
        return self._process.poll()

    def register_progress(self, progress: Union[int, float], leap_second: float):
        """Register progress."""
        self._history.append({"progress": progress, "leap_second": leap_second})

    def get_progress(self) -> Optional[Union[int, float]]:
        """Get latest progress."""
        if self._history:
            return self._history[-1]["progress"]
        return None

    def get_pid(self) -> int:
        """Get pid."""
        return self._process.pid


class TaskManagerServicer(task_manager_pb2_grpc.TaskManagerServicer, ReturnCode):
    """Provides methods that implement functionality of task manager server."""

    # pylint: disable=no-member, unused-argument

    def __init__(self, log_dir=os.getcwd()):
        super(task_manager_pb2_grpc.TaskManagerServicer, self).__init__()
        self.tasks: Dict[str, Task] = {}
        self.log_dir = log_dir
        self._use_gpu = True
        try:
            pynvml.nvmlInit()
            num_resource = pynvml.nvmlDeviceGetCount()
            pynvml.nvmlShutdown()
        except pynvml.nvml.NVMLError_LibraryNotFound:
            logger.warning("GPU can't be found. Task will be executed without GPU.")
            num_resource = int(
                USER_CONFIG.get("default", "max_task_without_gpu_simultaneously")
            )
            self._use_gpu = False
        self._resource_manager = ResourceManager(num_resource)
        self.logger = get_logger(name="task_manager")

    @property
    def use_gpu(self):
        """

        :return:
        """
        return self._use_gpu

    def health_check(self, request, context):
        """Return current server status"""
        return ServerStatus(alive=True)

    @start_end_logger
    def run_task(self, request, context):
        """run task based on request"""
        self.logger.info("task_manager_running")
        self._validate_task_statement(request)
        self._release_unused_resource()

        task_id = request.task_id
        resource_idx = self._resource_manager.get_resource(task_id)
        if resource_idx is None:
            return TaskStatus(task_id=task_id, status=TaskStatus.Status.NO_RESOURCE)

        if self.use_gpu:
            request.task_env["CUDA_VISIBLE_DEVICES"] = str(resource_idx)
        task = subprocess.Popen(  # pylint: disable=consider-using-with
            args=request.command,
            shell=True,
            env=request.task_env,
            stdout=open(  # pylint: disable=consider-using-with
                osp.join(self.log_dir, f"{task_id}_log.txt"), "w", encoding="utf-8"
            ),
            stderr=subprocess.STDOUT,
        )
        self.tasks[task_id] = Task(task)

        self.logger.info("%s is now running!", task_id)

        return TaskStatus(task_id=task_id, status=TaskStatus.Status.RUNNING)

    def _validate_task_statement(self, task_statement):
        if not task_statement.command:
            raise ValueError("Command shouldn't empty!")

    def _release_unused_resource(self):
        for task_id in self._resource_manager.get_tasks_using_resource():
            self._get_process_return_code(task_id)

    def _get_process_return_code(self, task_id: str):
        task = self.tasks.get(task_id)
        if task is None:
            return (
                False  # to be distinguished from None which means process is running.
            )
        return_code = task.get_return_code()
        if return_code is not None:
            self._resource_manager.release_resource(task_id)
        return return_code

    @start_end_logger
    def get_task_log(self, request, context):
        """
        Save an output of the requested task and return output file path.
        The response is sent by streaming.
        """
        log_file_path = osp.join(request.log_file_path, f"{request.task_id}_log.txt")
        try:
            with open(log_file_path, mode="rb") as file:
                while True:
                    chunk = file.read(CHUNK_SIZE)
                    if chunk:
                        yield TaskLogFile(log_file=chunk)
                    else:
                        return
        except OSError:
            error_message = f"Getting the log for {request.task_id} fail"
            logger.error(error_message)
            yield TaskLogFile(
                log_file=None, error_message=bytes(error_message, "utf-8")
            )

    @start_end_logger
    def kill_task(self, request, context):
        """Kill a requsted task if the task is running"""
        target_process = self.tasks.get(request.task_id)
        self.logger.info("kill task with id : %s", request.task_id)
        if target_process is None:
            return TaskStatus(
                task_id=request.task_id, status=TaskStatus.Status.NOTFOUND
            )
        sign = self._get_process_return_code(request.task_id)

        if sign is not None:
            return TaskStatus(task_id=request.task_id, status=TaskStatus.Status.DONE)
        p_util = ProcessUtil(target_process.get_pid())
        if p_util.kill_itself_with_child_process(KILL_CHILD_MAX_DEPTH):
            self.logger.info("%s is killed!", request.task_id)
            return TaskStatus(task_id=request.task_id, status=TaskStatus.Status.KILLED)
        self.logger.info("Fail to kill %s", request.task_id)
        return TaskStatus(task_id=request.task_id, status=TaskStatus.Status.ABNORMAL)

    @start_end_logger
    def get_task_status(self, request, context):
        """Get single requested task status"""
        return self._get_task_status_by_task_id(request.task_id)

    @start_end_logger
    def get_all_tasks(self, request, context):
        """Get all tasks managed by task manager"""
        all_tasks_status = AllTasksStatus()
        for task_id in self.tasks:
            all_tasks_status.task_status_array.append(
                self._get_task_status_by_task_id(task_id)
            )
        return all_tasks_status

    def _get_task_status_by_task_id(self, task_id):
        target_process = self.tasks.get(task_id)

        if target_process is None:
            return TaskStatus(task_id=task_id, status=TaskStatus.Status.NOTFOUND)

        result_return_code = self._get_process_return_code(task_id)
        return TaskStatus(
            task_id=task_id, status=self._convert_to_task_status(result_return_code)
        )

    def _convert_to_task_status(self, return_code):
        """Make task_manager_pb2.TaskStatus using return code of task."""
        if return_code is self.get_return_code("RUNNING"):
            return TaskStatus.Status.RUNNING
        if return_code == self.get_return_code("DONE"):
            return TaskStatus.Status.DONE
        if return_code == self.get_return_code("KILLED"):
            return TaskStatus.Status.KILLED
        return TaskStatus.Status.ABNORMAL

    def has_idle_resource(self, request, context):
        """Check there is available resource."""
        self._release_unused_resource()
        return IdleResources(exists=self._resource_manager.has_available_resource())

    @start_end_logger
    def report_progress(self, request, context):
        """get and save progress of task"""
        task = self._find_which_task_report(request.pid)
        if task is None:
            logger.warning("task(pid: %d) can not be found", request.pid)
            return ProgressResponse(
                received_status=ProgressResponse.ReceivedStatus.FAIL
            )

        task.register_progress(request.progress, request.leap_second)
        return ProgressResponse(received_status=ProgressResponse.ReceivedStatus.SUCCESS)

    def _find_which_task_report(self, current_pid: int) -> Optional[Task]:
        """find out all pids of task considering a case that pid is child process of task"""
        tasks_pid = {task.get_pid(): task for task in self.tasks.values()}
        pid_hierachy = [current_pid]

        try:
            current_process = psutil.Process(current_pid)
        except psutil.NoSuchProcess:
            return None

        pid_hierachy += [process.pid for process in current_process.parents()]

        for pid in pid_hierachy:
            if pid in tasks_pid:
                return tasks_pid[pid]

        return None


def serve():
    """run task manager server"""

    with futures.ThreadPoolExecutor(max_workers=10) as pool:
        server = grpc.server(pool)
        local_port = ast.literal_eval(USER_CONFIG.get("task_manager", "local_port"))
        local_address = ":".join(["0.0.0.0", str(local_port)])

        task_manager_pb2_grpc.add_TaskManagerServicer_to_server(
            TaskManagerServicer(), server
        )
        server.add_insecure_port(local_address)  # [TODO] set multiple task manager
        server.start()
        server.wait_for_termination()
        print("Interrupt Occurs. Now closing...")


if __name__ == "__main__":
    serve()
