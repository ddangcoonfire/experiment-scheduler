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
        self.tasks = {task_id : task}
        logger.info(f"{task_id} is now running!")

        return task_manager_pb2.Response(task_id=task_id, response=Response.RUNNING)

    def KillTask(self, request, context):
        pass

    def GetTaskStatus(self, request_iterator, context):
        pass        

    def GetAllTasks(self, request_iterator, context):
        pass


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
