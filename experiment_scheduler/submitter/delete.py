"""
[TODO] exs delete command Explanation
"""
import argparse
import ast

import grpc

from experiment_scheduler.common.settings import USER_CONFIG
from experiment_scheduler.master.grpc_master import master_pb2, master_pb2_grpc


def parse_args():
    """
    Todo
    :return:
    """
    parser = argparse.ArgumentParser(description="Delete exeperiments.")
    parser.add_argument("-t", "--task")
    return parser.parse_args()


def main():
    """
    Todo
    :return:
    """
    args = parse_args()
    task_id = args.task

    channel = grpc.insecure_channel(
        ast.literal_eval(USER_CONFIG.get("default", "master_address"))
    )
    stub = master_pb2_grpc.MasterStub(channel)

    request = master_pb2.Task(task_id=task_id)  # pylint: disable=no-member
    response = stub.kill_task(request)

    if response.status in set(
        master_pb2.TaskStatus.Status.KILLED, master_pb2.TaskStatus.Status.DONE
    ):
        print(f"task {response.task_id} is deleted")
    else:
        print(f"fail to delete {response.task_id} task")
