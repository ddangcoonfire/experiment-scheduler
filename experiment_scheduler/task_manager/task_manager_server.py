"""This file is in charge of server code run as daemon process."""

import os
import subprocess
import ast
from typing import Dict, Optional
from threading import Thread
from concurrent import futures
from os import path as osp
import time
import grpc
import pynvml

from experiment_scheduler.master.grpc_master import master_pb2
from experiment_scheduler.master.grpc_master import master_pb2_grpc
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
from experiment_scheduler.task_manager.task import Task

logger = get_logger(name="task_manager")

KILL_CHILD_MAX_DEPTH = 2
CHUNK_SIZE = 1024 * 5


class ResourceManager:
    """
    Resource Manager checks task manager's status.
    """

    def __init__(self, num_resource: int):
        self._resource_rental_history = {}
        self._available_resources = [True for _ in range(num_resource)]
        self.logger = get_logger(name="resource_manager")

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
        if task_id in self._resource_rental_history:
            raise RuntimeError(f"Resource is alreay assigned for {task_id}")
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
        except pynvml.nvml.NVMLError:
            logger.warning("GPU can't be found. Task will be executed without GPU.")
            num_resource = int(
                USER_CONFIG.get("default", "max_task_without_gpu_simultaneously")
            )
            self._use_gpu = False
        self._resource_manager = ResourceManager(num_resource)
        self.logger = get_logger(name="task_manager")

        checkthread = Thread(target=self.get_dead_tasks, daemon = True)
        checkthread.start()

    @property
    def use_gpu(self):
        """

        :return:
        """
        return self._use_gpu

    def health_check(self, request, context):
        """
        Return current server status and finished task id list which are finished
        """
        server_status = ServerStatus()
        server_status.alive = True
        task_id_list = list(self.tasks.keys())
        done_task_id_list = []
        if len(task_id_list) > 0:
            for task_id in task_id_list:
                task_status = self._get_task_status_by_task_id(task_id)
                if task_status.status == TaskStatus.Status.DONE:
                    server_status.task_id_array.append(task_id)
                    done_task_id_list.append(task_id)
        for done_task_id in done_task_id_list:
            del self.tasks[done_task_id]
        return server_status

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
        self.tasks[task_id] = Task(task.pid)

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
                IS_READ = -1
                while True:
                    chunk = file.read(CHUNK_SIZE)
                    if chunk:
                        IS_READ = 1
                        yield TaskLogFile(log_file=chunk)
                    else:
                        if IS_READ == -1:
                            error_message = f"There is no log in {request.task_id}"
                            yield TaskLogFile(log_file=None, error_message=bytes(error_message, "utf-8"))
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
        _, alive = target_process.kill_process_tree(include_me=True)
        if not alive:
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

    def get_dead_tasks(self):
        """Check task runs well and if there are abnormally exited tasks, then request master to run them again."""
        while True:
            dead_tasks = []
            for task_id, task in self.tasks.items():
                return_code = task.get_return_code()
                if return_code not in [0, None]:
                    self._resource_manager.release_resource(task_id)
                    dead_tasks.append(master_pb2.Task(task_id=task_id))
            if dead_tasks:
                for dead_task in dead_tasks:
                    del self.tasks[dead_task.task_id]
                channel = grpc.insecure_channel(
                    ast.literal_eval(USER_CONFIG.get("default", "master_address"))
                )
                stub = master_pb2_grpc.MasterStub(channel)
                stub.request_abnormal_exited_tasks(master_pb2.TaskList(task_list=dead_tasks))
            time.sleep(1)


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
        for task in self.tasks.values():
            if current_pid == task.pid or task.is_child_pid(current_pid):
                return task
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
