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
import os
import signal
from concurrent import futures
import logging
import math
import time
import uuid
import subprocess
from enum import Enum

import grpc
import task_manager_pb2
import task_manager_pb2_grpc

logger = logging.getLogger(__name__)


class Response(Enum):
    """Enum class to represent meaning of each number"""
    RUNNING = 0
    DONE = 1
    KILLED = 2
    ABNORMAL = 3
    NOTFOUND = 4


class TaskManagerServicer(task_manager_pb2_grpc.TaskManagerServicer):
    """Provides methods that implement functionality of route guide server."""

    def __init__(self):
        self.tasks = {}

    def RunTask(self, request, context):
        """
        Get task request and run it.
        """
        task_env = request.task_env
        task_env['CUDA_VISIBLE_DEVICES'] = str(request.gpuidx)

        task = subprocess.Popen(
            args=request.command,
            shell=True,
            env=task_env
        )

        # add random hash to make task_id
        task_id = request.name + '-' + uuid.uuid4().hex
        self.tasks = {task_id: task}
        logger.info(f"{task_id} is now running!")

        return task_manager_pb2.Response(task_id=task_id, response=Response.RUNNING)

    def KillTask(self, request, context):
        target_process = self.tasks.get(request.task_id)

        if target_process is None:
            return task_manager_pb2.Response(task_id=request.task_id, response=Response.NOTFOUND)
        sign = target_process.poll()
        if sign is None:
            return task_manager_pb2.Response(task_id=request.task_id, response=Response.DONE)
        else:
            target_process.terminate()
            target_process.wait()
            logger.info(f"{request.task_id} is killed!")
            return task_manager_pb2.Response(task_id=request.task_id, response=Response.KILLED)

    def GetTaskStatus(self, request, context):
        target_process = self.tasks.get(request.task_id)

        if target_process is None:
            return task_manager_pb2.Response(task_id=request.task_id, response=Response.NOTFOUND)

        return get_response(request.task_id, target_process)

    def GetAllTasks(self, request_iterator, context):
        task_dict = self.tasks.items()
        all_tasks_status = []

        for (task_id, target_process) in task_dict:
            all_tasks_status.append(get_response(task_id, target_process))

        return all_tasks_status


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    task_manager_pb2_grpc.add_TaskManagerServicer_to_server(
        RouteGuideServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


def get_response(task_id, target_process):
    return_code = target_process.returncode
    if return_code == 0:
        return task_manager_pb2.Response(task_id=task_id, response=Response.DONE)
    elif return_code is None:
        return task_manager_pb2.Response(task_id=task_id, response=Response.RUNNING)
    elif return_code is (-signal.SIGTERM or -signal.SIGKILL):
        return task_manager_pb2.Response(task_id=task_id, response=Response.KILLED)



if __name__ == '__main__':
    logging.basicConfig()
    serve()
