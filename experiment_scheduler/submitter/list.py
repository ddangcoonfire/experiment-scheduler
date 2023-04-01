"""
[TODO] exs list command Explanation
"""
import argparse
import ast
import os

import grpc

from experiment_scheduler.common.settings import USER_CONFIG
from experiment_scheduler.master.grpc_master import master_pb2, master_pb2_grpc

TASK_STATUS = ["waiting", "running", "done", "killed", "abnormal", "not found"]


def parse_args():
    """
    Parse file name option argument.
    - ex) if exs command includes "-f sample.yaml", return "sample.yaml"
    """

    parser = argparse.ArgumentParser(description="Execute exeperiments.")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-e", "--experiment")
    return parser.parse_args()


def main():
    """
    Todo
    :return:
    """
    args = parse_args()
    ter_col_size = os.get_terminal_size().columns

    channel = grpc.insecure_channel(
        ast.literal_eval(USER_CONFIG.get("default", "master_address"))
    )
    stub = master_pb2_grpc.MasterStub(channel)
    request = master_pb2.Experiment(experiment_id=args.experiment)
    response = stub.get_all_tasks(request)

    # print(response)

    if args.verbose:
        for exp_status in response.experiment_status_array:
            exp_array_without_last = exp_status.task_status_array.task_status_array[:-1]
            exp_array_last = exp_status.task_status_array.task_status_array[-1]
            print(f"experiment_id: {exp_status.experiment_id:{ter_col_size - 20 }}")
            for task_status in exp_array_without_last:
                print(
                    f"\t├─ {task_status.task_id:{ter_col_size - 20 }} ({TASK_STATUS[task_status.status]})"
                )
            print(
                f"\t└─ {exp_array_last.task_id:{ter_col_size - 20 }} ({TASK_STATUS[exp_array_last.status]})"
            )
    else:
        for exp_status in response.experiment_status_array:
            exp_array_without_last = exp_status.task_status_array.task_status_array[:-1]
            exp_array_last = exp_status.task_status_array.task_status_array[-1]
            print(
                f"experiment_id: "
                f"{exp_status.experiment_id[:70]:{100 if ter_col_size - 20 > 100 else ter_col_size - 20}}"
            )
            for task_status in exp_array_without_last:
                print(
                    f"\t├─ {task_status.task_id[:70]:{100 if ter_col_size - 20 > 100 else ter_col_size - 20}} "
                    f"({TASK_STATUS[task_status.status]})"
                )
            print(
                f"\t└─ {exp_array_last.task_id[:70]:{100 if ter_col_size - 20 > 100 else ter_col_size - 20}} "
                f"({TASK_STATUS[exp_array_last.status]})"
            )
