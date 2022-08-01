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

TASK_ID = "test-5f10ce8dafd64b048a11d2c5bdf7ae18"

def stub_run_task(stub):
    print("-------------- run_task --------------")
    res = stub.run_task(
        task_manager_pb2.TaskStatement(
            gpuidx=7,
            command="sleep 100",
            name="test",
            task_env=os.environ.copy()
        )
    )
    print("task_id", res.task_id)
    print("response", res.status)

def stub_get_all_task(stub):
    print("-------------- get_all_task --------------")
    empty = task_manager_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
    res = stub.get_all_tasks(empty)
    for val in res.task_status_array:
        print(val)

def stub_health_check(stub):
    print("-------------- health_check --------------")
    empty = task_manager_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
    res = stub.health_check(empty)
    print(res)

def stub_get_task_log(stub):
    print("-------------- get_task_log --------------")
    res = stub.get_task_log(
        task_manager_pb2.Task(
            task_id=TASK_ID
        )
    )
    print(res.logfile_path)

def stub_get_task_status(stub):
    print("-------------- get_task_status --------------")
    res = stub.get_task_status(
        task_manager_pb2.Task(
            task_id=TASK_ID
        )
    )
    print(res.status)

def stub_kill_task(stub):
    print("-------------- get_task_status --------------")
    res = stub.kill_task(
        task_manager_pb2.Task(
            task_id=TASK_ID
        )
    )
    print(res.status)

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = task_manager_pb2_grpc.TaskManagerStub(channel)
        # stub_run_task(stub)
        stub_get_all_task(stub)
        # stub_health_check(stub)
        # stub_get_task_log(stub)
        # stub_get_task_status(stub)
        # stub_kill_task(stub)
        print("DONE!")


if __name__ == '__main__':
    run()
