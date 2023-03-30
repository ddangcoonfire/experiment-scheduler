"""
[TODO]
"""
import time
import ast
import os
import grpc
from experiment_scheduler.common.settings import USER_CONFIG
from experiment_scheduler.task_manager.grpc_task_manager import task_manager_pb2
from experiment_scheduler.task_manager.grpc_task_manager import task_manager_pb2_grpc


def exs_report(reported_progress) -> None:
    """
    Returns: Parse user input and record current time to Progress shape for grpc
    leap_second : current time
    """
    channel = grpc.insecure_channel(
        ast.literal_eval(USER_CONFIG.get("default", "task_manager_address"))[0]
    )
    stub = task_manager_pb2_grpc.TaskManagerStub(channel)

    input = task_manager_pb2.Progress(
        progress=reported_progress, leap_second=time.time(), pid=os.getpid()
    )
    response = stub.report_progress(input)

    if (
        response.received_status
        == task_manager_pb2.ProgressResponse.ReceivedStatus.SUCCESS
    ):
        print("success to report progress", response)
    else:
        print("fail to report progress")
