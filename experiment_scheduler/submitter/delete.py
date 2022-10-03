"""
[TODO] exs delete command Explanation

"""
import argparse
import ast
import grpc
from experiment_scheduler.common.settings import USER_CONFIG
from experiment_scheduler.master.grpc_master import master_pb2
from experiment_scheduler.master.grpc_master import master_pb2_grpc


def parse_args():
    """
    Todo
    :return:
    """
    parser = argparse.ArgumentParser(description="Execute exeperiments.")
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

    request = master_pb2.MasterTask(task_id=task_id)
    response = stub.delete_task(request)

    # pylint: disable=no-member
    if response.status == master_pb2.MasterTaskStatus.Status.DELETE:
        print(f"task {response.task_id} is deleted")
    else:
        print(f"fail to delete {response.task_id} task")
