"""
[TODO] exs status command Explanation
"""
import ast
import grpc
from os import path as osp
from experiment_scheduler.common.settings import USER_CONFIG
from experiment_scheduler.master.grpc_master import master_pb2
from experiment_scheduler.master.grpc_master import master_pb2_grpc
from experiment_scheduler.submitter.delete import parse_args
import time

def main():
    """
    Get log certain task
    :return:
    """
    args = parse_args()
    task_id = args.task

    channel = grpc.insecure_channel(
        ast.literal_eval(USER_CONFIG.get("default", "master_address"))
    )
    stub = master_pb2_grpc.MasterStub(channel)

    request = master_pb2.Task(task_id=task_id)

    responses = stub.get_task_log(request)
    log_file_path = osp.join(f"{task_id}_exs_log.txt")
    print("Downloading ", f"{task_id}_exs_log.txt")
    for response in responses:
        with open(log_file_path, mode="ab") as file:
            file.write(response.log_file)
    print("Finish Download ", f"{task_id}_exs_log.txt")