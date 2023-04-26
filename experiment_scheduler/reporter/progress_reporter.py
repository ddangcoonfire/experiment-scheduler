"""
It enables the user to report the progress of the task currently being performed and
the current time to the task manager along with the pid.
"""
import time
import ast
import os
import grpc
from experiment_scheduler.common.settings import USER_CONFIG
from experiment_scheduler.task_manager.grpc_task_manager import task_manager_pb2
from experiment_scheduler.task_manager.grpc_task_manager import task_manager_pb2_grpc
from experiment_scheduler.common.logging import get_logger

logger = get_logger(name="reporter")


def report_progress(progress) -> None:
    """
    Parse user input and record current time to Progress shape for grpc
    progress : current progress of task
    """
    channel = grpc.insecure_channel(
        ast.literal_eval(USER_CONFIG.get("default", "task_manager_address"))[0]
    )
    stub = task_manager_pb2_grpc.TaskManagerStub(channel)

    progress = task_manager_pb2.Progress(
        progress=progress, leap_second=time.time(), pid=os.getpid()
    )
    response = stub.report_progress(progress)

    if (
        response.received_status
        == task_manager_pb2.ProgressResponse.ReceivedStatus.FAIL
    ):
        logger.warning("fail to report progress")
