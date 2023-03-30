"""
[TODO] exs status command Explanation
"""
import ast
import grpc
import argparse
from os import path as osp
from experiment_scheduler.common.settings import USER_CONFIG
from experiment_scheduler.master.grpc_master import master_pb2
from experiment_scheduler.master.grpc_master import master_pb2_grpc
# from experiment_scheduler.common.logging import get_logger

class Log_Color:
    INFO = "\u001b[32m [LOG] "
    WARNING = "\u001b[33m [WARN] "
    ERROR = "\u001b[31m [ERROR] "
    END = '\033[0m'

def parse_args():
    """
    Todo
    :return:
    """
    parser = argparse.ArgumentParser(description="Search Log for specific Task.")
    parser.add_argument("-t", "--task")
    parser.add_argument("-f", "--file")
    return parser.parse_args()


def main():
    """
    Get log certain task
    :return:
    """
    args = parse_args()
    print(args)
    task_id = args.task
    file_download = args.file
    channel = grpc.insecure_channel(
        ast.literal_eval(USER_CONFIG.get("default", "master_address"))
    )
    stub = master_pb2_grpc.MasterStub(channel)

    request = master_pb2.Task(task_id=task_id)
    responses = stub.get_task_log(request)
    log_file_path = osp.join(f"{task_id}.txt")
    for response in responses:
        if response.error_message:
            print(Log_Color.ERROR + response.error_message.decode("utf-8") + Log_Color.END)
            return
        print(Log_Color.INFO + f"Start Getting Log [{task_id}]:" + Log_Color.END)
        print(Log_Color.INFO + f"{str(response.log_file,'utf-8')}" + Log_Color.END)
        if file_download == "y":
            with open(log_file_path, mode="ab") as file:
                file.write(response.log_file)