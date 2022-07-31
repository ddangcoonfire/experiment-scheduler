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
"""The Python implementation of the gRPC route guide client."""

from __future__ import print_function

import os

import grpc
from experiment_scheduler.task_manager.grpc_task_manager import (
    task_manager_pb2, task_manager_pb2_grpc)


def make_route_note(message, latitude, longitude):
    return task_manager_pb2.RouteNote(
        message=message,
        location=task_manager_pb2_grpc.Point(latitude=latitude, longitude=longitude))

def stub_run_task(stub):
    res = stub.run_task(
        task_manager_pb2.TaskStatement(
            gpuidx=7,
            command="ls",
            name="test"
        )
    )
    print("task_id", res.task_id)
    print("response", res.response)

def stub_run_

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = task_manager_pb2_grpc.TaskManagerStub(channel)
        print("-------------- RunTask --------------")
        stub_run_task(stub)
        os.sleep(3)
        guide_get_feature(stub)
        print("DONE!")


if __name__ == '__main__':
    run()
