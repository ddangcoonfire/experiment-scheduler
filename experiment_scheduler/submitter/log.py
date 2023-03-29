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
import logging


_level_color_map = {
    logging.INFO: "\u001b[32m [INFO] " + "%(message)s" + "\u001b[0m",
    logging.WARNING: "\u001b[33m [WARN] " + "%(message)s" + "\u001b[0m",
    logging.ERROR: "\u001b[31m [ERROR] " + "%(message)s" + "\u001b[0m",
}

def get_client_logger(name, task_id, *args, **kwargs):
    logger = logging.getLogger(name=name, *args, **kwargs)
    ch = logging.StreamHandler()
    ch.setFormatter(ClientLoggingFormatter())
    logger.addHandler(ch)
    logger.setLevel(logging.INFO)
    return logger


class ClientLoggingFormatter(logging.Formatter):
    """
    custom logging
    """

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = _level_color_map.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

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
    task_id = args.task
    file_download = args.file
    channel = grpc.insecure_channel(
        ast.literal_eval(USER_CONFIG.get("default", "master_address"))
    )
    stub = master_pb2_grpc.MasterStub(channel)

    request = master_pb2.Task(task_id=task_id)
    responses = stub.get_task_log(request)
    logger = get_client_logger(name=task_id, task_id=task_id)
    log_file_path = osp.join(f"{task_id}.txt")
    for response in responses:
        if response.error_message:
            logger.error(response.error_message.decode("utf-8"))
            return
        print("hhh")
        logger.info(f"Start Getting Log [{task_id}]:")
        logger.info(f"{str(response.log_file,'utf-8')}")
        if file_download == "y":
            with open(log_file_path, mode="ab") as file:
                file.write(response.log_file)