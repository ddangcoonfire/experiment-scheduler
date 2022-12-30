"""This file is in charge of server code run as daemon process."""

import psutil
import logging
import os
import subprocess
from typing import Dict
from concurrent import futures
from os import path as osp

import grpc
import pynvml

from experiment_scheduler.task_manager.grpc_task_manager import task_manager_pb2_grpc
from experiment_scheduler.task_manager.grpc_task_manager.task_manager_pb2 import (
    ServerStatus,
    TaskStatus,
    AllTasksStatus,
    TaskLog,
    IdleResources,
)
from experiment_scheduler.common.logging import get_logger, start_end_logger

logger = get_logger(name="task_manager")
from experiment_scheduler.task_manager.return_code import return_code

KILL_CHILD_MAX_DEPTH = 2


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
    def kill_process_recursively(process: psutil.Process, max_depth: int, cur_depth: int = 0) -> bool:
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
                ProcessUtil.kill_process_recursively(child_process, max_depth, cur_depth+1)

        if process.is_running():
            process.terminate()
            process.wait()

        return True

class ResourceManager:
    def __init__(self, num_resource: int):
        self._resource_rental_history = {}
        self._available_resources = [True for _ in range(num_resource)]
        self.logger = get_logger(name="resource_manager")

    def set_resource_as_idle(self, resource_idx: int):
        self._available_resources[resource_idx] = True

    def set_resource_as_used(self, resource_idx: int):
        self._available_resources[resource_idx] = False

    def release_resource(self, task_id):
        if task_id not in self._resource_rental_history:
            return
        resource_idx = self._resource_rental_history[task_id]
        self._available_resources[resource_idx] = True
        del self._resource_rental_history[task_id]

    def get_resource(self, task_id):
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
        for resource_is_idle in self._available_resources:
            if resource_is_idle:
                return True
        return False

    def get_tasks_using_resource(self):
        return list(self._resource_rental_history.keys())


class TaskManagerServicer(task_manager_pb2_grpc.TaskManagerServicer, return_code):
    """Provides methods that implement functionality of task manager server."""

    # pylint: disable=no-member

    def __init__(self, log_dir=os.getcwd()):
        super(return_code).__init__()
        self.tasks: Dict[str, subprocess.Popen] = {}
        self.log_dir = log_dir
        pynvml.nvmlInit()
        num_gpu = pynvml.nvmlDeviceGetCount()
        pynvml.nvmlShutdown()
        self._resource_manager = ResourceManager(num_gpu)
        self.logger = get_logger(name="task_manager")

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
        gpu_idx = self._resource_manager.get_resource(task_id)
        if gpu_idx is None:
            return TaskStatus(task_id=task_id, status=TaskStatus.Status.NO_RESOURCE)
        request.task_env["CUDA_VISIBLE_DEVICES"] = str(gpu_idx)

        task = subprocess.Popen(
            args=request.command,
            shell=True,
            env=request.task_env,
            stdout=open(
                osp.join(self.log_dir, f"{task_id}_log.txt"), "w", encoding="utf-8"
            ),
            stderr=subprocess.STDOUT,
        )

        self.tasks[task_id] = task

        self.logger.info("%s is now running!", task_id)

        return TaskStatus(task_id=task_id, status=TaskStatus.Status.RUNNING)

    def _validate_task_statement(self, task_statement):
        if not task_statement.command:
            raise ValueError("Command shouldn't empty!")

    def _release_unused_resource(self):
        for task_id in self._resource_manager.get_tasks_using_resource():
            self._get_process_return_code(task_id)

    def _get_process_return_code(self, task_id: str):
        if task_id not in self.tasks:
            return (
                False  # to be distinguished from None which means process is running.
            )
        return_code = self.tasks[task_id].poll()
        if return_code is not None:
            self._resource_manager.release_resource(task_id)
        return return_code

    @start_end_logger
    def get_task_log(self, request, context):
        """
        Save an output of the requested task and return output file path.
        If status of the requeest task is Done, delete it from task manager.
        """
        target_process = self._get_task(request.task_id)
        if target_process is None:
            return TaskStatus(logfile_path="")

        log_file_path = osp.join(self.log_dir, f"{request.task_id}_log.txt")

        if self._get_process_return_code(request.task_id) is not None:
            del self.tasks[request.task_id]

        return TaskLog(logfile_path=log_file_path)

    @start_end_logger
    def kill_task(self, request, context):
        """Kill a requsted task if the task is running"""
        target_process = self._get_task(request.task_id)
        self.logger.info("kill task with id : {}".format(request.task_id))
        if target_process is None:
            return TaskStatus(
                task_id=request.task_id, status=TaskStatus.Status.NOTFOUND
            )
        sign = self._get_process_return_code(request.task_id)

        if sign is not None:
            return TaskStatus(task_id=request.task_id, status=TaskStatus.Status.DONE)
        p_util = ProcessUtil(target_process.pid)
        if p_util.kill_itself_with_child_process(KILL_CHILD_MAX_DEPTH):
            self.logger.info("%s is killed!", request.task_id)
            return TaskStatus(task_id=request.task_id, status=TaskStatus.Status.KILLED)
        else:
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
        target_process = self._get_task(task_id)

        if target_process is None:
            return TaskStatus(task_id=task_id, status=TaskStatus.Status.NOTFOUND)

        result_return_code = self._get_process_return_code(task_id)
        return TaskStatus(
            task_id=task_id,
            status=self._convert_to_task_status(result_return_code)
        )

    def _convert_to_task_status(self, return_code):
        """Make task_manager_pb2.TaskStatus using return code of task."""
        if return_code is self.get_return_code('RUNNING'):
            return TaskStatus.Status.RUNNING
        if return_code == self.get_return_code('DONE'):
            return TaskStatus.Status.DONE
        if return_code == self.get_return_code('KILLED'):
            return TaskStatus.Status.KILLED
        return TaskStatus.Status.ABNORMAL

    def _get_task(self, task_id):
        """Get a task instance if exists. if not, return None"""
        if task_id not in self.tasks:
            self.logger.warning("%s is not found in task_manager!", task_id)
            return None
        return self.tasks[task_id]

    def has_idle_resource(self, request, context):
        self._release_unused_resource()
        return IdleResources(exists=self._resource_manager.has_available_resource())


def serve(address):
    """run task manager server"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    task_manager_pb2_grpc.add_TaskManagerServicer_to_server(
        TaskManagerServicer(), server
    )
    server.add_insecure_port(address)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve("[::]:50051")
