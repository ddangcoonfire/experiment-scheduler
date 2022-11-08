"""This file is in charge of server code run as daemon process."""

import logging
import os
import platform
import signal
import subprocess
from concurrent import futures
from os import path as osp

import grpc

from experiment_scheduler.task_manager.grpc_task_manager import task_manager_pb2_grpc
from experiment_scheduler.task_manager.grpc_task_manager.task_manager_pb2 import (
    ServerStatus,
    TaskStatus,
    AllTasksStatus,
    TaskLog,
)

logger = logging.getLogger(__name__)


class TaskManagerServicer(task_manager_pb2_grpc.TaskManagerServicer):
    """Provides methods that implement functionality of task manager server."""

    # pylint: disable=no-member

    def __init__(self, log_dir=os.getcwd()):
        self.tasks = {}
        self.log_dir = log_dir

    def health_check(self, request, context):
        """Return current server status"""
        return ServerStatus(alive=True)

    def run_task(self, request, context):
        """run task based on request"""
        self._validate_task_statement(request)

        task_id = self.request.task_id
        task = self._execute_subprocess(request, task_id)
        self._register_task(task_id, task)
        logger.info("%s is now running!", task_id)

        return TaskStatus(task_id=task_id, status=TaskStatus.Status.RUNNING)

    def _validate_task_statement(self, task_statement):
        if task_statement.gpuidx < 0:
            raise ValueError(
                f"GPU index should be positive. your value is {task_statement.gpuidx}"
            )
        if not task_statement.command:
            raise ValueError("Command shouldn't empty!")

    def _execute_subprocess(self, task_statement, task_id: str):
        # pylint: disable=consider-using-with
        task_env = task_statement.task_env
        task_env["CUDA_VISIBLE_DEVICES"] = str(task_statement.gpuidx)
        log_file_path = osp.join(self.log_dir, f"{task_id}_log.txt")
        output_file = open(log_file_path, "w", encoding="utf-8")

        task = subprocess.Popen(
            args=task_statement.command,
            shell=True,
            env=task_env,
            stdout=output_file,
            stderr=subprocess.STDOUT,
        )

        return task

    def _register_task(self, task_id, task):
        self.tasks[task_id] = task

    def get_task_log(self, request, context):
        """
        Save an output of the requested task and return output file path.
        If status of the requeest task is Done, delete it from task manager.
        """
        target_process = self._get_task(request.task_id)
        if target_process is None:
            return TaskStatus(logfile_path="")

        log_file_path = osp.join(self.log_dir, f"{request.task_id}_log.txt")

        if self.tasks[request.task_id].poll() is not None:
            del self.tasks[request.task_id]

        return TaskLog(logfile_path=log_file_path)

    def kill_task(self, request, context):
        """Kill a requsted task if the task is running"""
        target_process = self._get_task(request.task_id)

        if target_process is None:
            return TaskStatus(
                task_id=request.task_id, status=TaskStatus.Status.NOTFOUND
            )
        sign = target_process.poll()

        if sign is not None:
            return TaskStatus(task_id=request.task_id, status=TaskStatus.Status.DONE)

        target_process.terminate()
        target_process.wait()
        logger.info("%s is killed!", request.task_id)
        return TaskStatus(task_id=request.task_id, status=TaskStatus.Status.KILLED)

    def get_task_status(self, request, context):
        """Get single requested task status"""
        target_process = self._get_task(request.task_id)

        if target_process is None:
            return TaskStatus(
                task_id=request.task_id, status=TaskStatus.Status.NOTFOUND
            )

        return self._wrap_by_grpc_task_status(request.task_id)

    def get_all_tasks(self, request, context):
        """Get all tasks managed by task manager"""
        all_tasks_status = AllTasksStatus()

        for task_id in self.tasks:
            all_tasks_status.task_status_array.append(
                self._wrap_by_grpc_task_status(task_id)
            )

        return all_tasks_status

    def _wrap_by_grpc_task_status(self, task_id):
        """Make task_manager_pb2.TaskStatus using return code of task."""
        target_process = self._get_task(task_id)

        if target_process is None:
            return TaskStatus(task_id=task_id, status=TaskStatus.Status.NOTFOUND)

        return_code = target_process.poll()
        if return_code == 0:
            return TaskStatus(task_id=task_id, status=TaskStatus.Status.DONE)
        if return_code is None:
            return TaskStatus(task_id=task_id, status=TaskStatus.Status.RUNNING)
        if platform.system() == 'Windows' and return_code == -signal.SIGTERM:
            return TaskStatus(task_id=task_id, status=TaskStatus.Status.KILLED)
        elif return_code == -signal.SIGKILL:
            return TaskStatus(task_id=task_id, status=TaskStatus.Status.KILLED)
        return TaskStatus(task_id=task_id, status=TaskStatus.Status.ABNORMAL)

    def _get_task(self, task_id):
        """Get a task instance if exists. if not, return None"""
        if task_id not in self.tasks:
            logger.warning("%s is not found in task_manager!", task_id)
            return None
        return self.tasks[task_id]


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
