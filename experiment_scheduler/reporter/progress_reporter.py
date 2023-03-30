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
from experiment_scheduler.common.logging import get_logger

logger = get_logger(name='reporter')

def report_progress(progress) -> None:
    """
    Parse user input and record current time to Progress shape for grpc
    progress : current progress of task
    """
    channel = grpc.insecure_channel(
        ast.literal_eval(USER_CONFIG.get("default", "task_manager_address"))
    )
    stub = task_manager_pb2_grpc.TaskManagerStub(channel)

    input = task_manager_pb2.Progress(
        progress=git status`progress,
        leap_seoncd=time.time(),
        pid=os.getpid()
    )
    response = stub.report_progress(input)

    if response.response == task_manager_pb2.ProgressResponse.ReceivedStatus.FAIL:
        logger.warning('fail to report progress')



