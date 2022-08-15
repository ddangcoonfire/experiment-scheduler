# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the gRPC route guide server."""
import logging
import os
import signal
import subprocess
import uuid
from concurrent import futures
from os import path as osp

import grpc

from experiment_scheduler.task_manager.grpc_task_manager import task_manager_pb2
from experiment_scheduler.task_manager.grpc_task_manager import task_manager_pb2_grpc
from experiment_scheduler.task_manager.grpc_task_manager.task_manager_pb2 import (
    ServerStatus,
    TaskStatement,
    TaskStatus,
    Task,
    AllTasksStatus,
    TaskLog
)

logger = logging.getLogger(__name__)

class TaskManagerServicer(task_manager_pb2_grpc.TaskManagerServicer):
    """Provides methods that implement functionality of task manager server."""

    def __init__(self, log_dir = os.getcwd()):
        self.tasks = {}
        self.log_dir = log_dir

    def health_check(self, request, context):
        """Return current server status"""
        return ServerStatus(alive=True)

    def run_task(self, task_statement, context):
        self._validate_task_statement(task_statement)
        task_id = self._create_task_id(task_statement.name)
        task = self._execute_subprocess(task_statement, task_id)
        self.tasks[task_id] = task
        logger.info(f"{task_id} is now running!")

        return TaskStatus(
            task_id=task_id,
            status=TaskStatus.Status.RUNNING
        )

    def _validate_task_statement(self, task_statement):
        if not isinstance(task_statement, TaskStatement):
            raise TypeError(f"type of request should be TaskStatement. Current argument type is {type(task_statement)}")
        if task_statement.gpuidx < 0:
            raise ValueError(f"GPU index should be positive. your value is {task_statement.gpuidx}")
        if not task_statement.command:
            raise ValueError(f"Command shouldn't empty!")

    def _create_task_id(self, name):
        return name + '-' + uuid.uuid4().hex  # add random hash to make task_id

    def _execute_subprocess(self, task_statement, task_id: str):
        task_env = task_statement.task_env
        task_env['CUDA_VISIBLE_DEVICES'] = str(task_statement.gpuidx)
        log_file_path = osp.join(self.log_dir, f"{task_id}_log.txt")
        output_file = open(log_file_path, "w")

        task = subprocess.Popen(
            args=task_statement.command,
            shell=True,
            env=task_env,
            stdout=output_file,
            stderr=subprocess.STDOUT
        )

        return task

    def get_task_log(self, request, context):
        """
        Save an output of the requested task and return output file path.
        If status of the requeest task is Done, delete it from task manager.
        """
        target_process = self._get_task(request.task_id)
        if target_process is None:
            return TaskStatus(logfile_path = "")

        log_file_path = osp.join(
            self.log_dir, f"{request.task_id}_log.txt")

        if self.tasks[request.task_id].poll() is not None:
            del self.tasks[request.task_id]

        return TaskLog(logfile_path = log_file_path)

    def kill_task(self, request, context):
        """Kill a requsted task if the task is running"""
        target_process = self._get_task(request.task_id)

        if target_process is None:
            return TaskStatus(
                task_id=request.task_id,
                status=TaskStatus.Status.NOTFOUND
            )
        sign = target_process.poll()

        if sign is not None:
            return TaskStatus(
                task_id=request.task_id,
                status=TaskStatus.Status.DONE
            )
        else:
            target_process.terminate()
            target_process.wait()
            logger.info(f"{request.task_id} is killed!")
            return TaskStatus(
                task_id=request.task_id,
                status=TaskStatus.Status.KILLED
            )

    def get_task_status(self, request, context):
        """Get single requested task status"""
        target_process = self._get_task(request.task_id)

        if target_process is None:
            return TaskStatus(
                task_id=request.task_id,
                status=TaskStatus.Status.NOTFOUND
            )

        return self._wrap_by_grpc_TaskStatus(request.task_id)

    def get_all_tasks(self, empty_request, context):
        """Get all tasks managed by task manager"""
        all_tasks_status = AllTasksStatus()

        for task_id in self.tasks.keys():
            all_tasks_status.task_status_array.append(
                self._wrap_by_grpc_TaskStatus(task_id))

        return all_tasks_status

    def _wrap_by_grpc_TaskStatus(self, task_id):
        """Make task_manager_pb2.TaskStatus using return code of task."""
        target_process = self._get_task(task_id)

        if target_process is None:
            return TaskStatus(task_id=task_id, status=TaskStatus.Status.NOTFOUND)

        return_code = target_process.poll()
        if return_code == 0:
            return TaskStatus(task_id=task_id, status=TaskStatus.Status.DONE)
        elif return_code is None:
            return TaskStatus(task_id=task_id, status=TaskStatus.Status.RUNNING)
        elif return_code == -signal.SIGTERM or return_code == -signal.SIGKILL:
            return TaskStatus(task_id=task_id, status=TaskStatus.Status.KILLED)
        else:
            return TaskStatus(task_id=task_id, status=TaskStatus.Status.ABNORMAL)

    def _get_task(self, task_id):
        """Get a task instance if exists. if not, return None"""
        if task_id not in self.tasks:
            raise ValueError(f"There is no task whose id is {task_id}")
        return self.tasks[task_id]
    

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    task_manager_pb2_grpc.add_TaskManagerServicer_to_server(TaskManagerServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
