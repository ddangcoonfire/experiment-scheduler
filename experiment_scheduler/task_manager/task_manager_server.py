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
    READY = 0
    RUNNING = 1
    DONE = 2
    KILLED = 3
    ABNORMAL = 4


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
        target_process = self.tasks[request.task_id]
        target_process.kill()

        return task_manager_pb2.Response(task_id=request.task_id, response=Response.KILLED)

    def GetTaskStatus(self, request, context):
        target_process = self.tasks[request.task_id]
        return_code = target_process.returncode
        if return_code == 0:
            return task_manager_pb2.Response(task_id=request.task_id, response=Response.DONE)
        elif return_code is None:
            return task_manager_pb2.Response(task_id=request.task_id, response=Response.RUNNING)
        else:
            target_process_pid = target_process.PID
            cmd = "ps -o " + target_process_pid + ",s |grep " + target_process_pid
            status = (os.system(cmd).read().split(' '))[1]
            return task_manager_pb2.Response(task_id=request.task_id, response=get_status(status))

    def GetAllTasks(self, request_iterator, context):
        task_list = self.tasks.values()
        all_tasks_status = []
        for target_process in task_list:
            task_id = get_task_id(self.tasks, target_process)
            return_code = target_process.returncode
            if return_code == 0:
                return all_tasks_status.extend(task_manager_pb2.Response(task_id=task_id, response=Response.DONE))
            elif return_code is None:
                return all_tasks_status.extend(task_manager_pb2.Response(task_id=task_id, response=Response.RUNNING))
            else:
                target_process_pid = target_process.PID
                cmd = "ps -o " + target_process_pid + ",s |grep " + target_process_pid
                status = (os.system(cmd).read().split(' '))[1]
                return all_tasks_status.extend(task_manager_pb2.Response(task_id=task_id, response=get_status(status)))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    task_manager_pb2_grpc.add_TaskManagerServicer_to_server(
        RouteGuideServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()


def get_status(code):
    return {'D': 0, 'R': 1, 'X': 3, 'Z': 4}.get(code, '2')


def get_task_id(tasks, val):
    for key, value in tasks.items():
        if val == value:
            return key
