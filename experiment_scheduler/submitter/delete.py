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
    parser.add_argument("-e", "--experiment")
    return parser.parse_args()


def main():
    """
    Todo
    :return:
    """
    args = parse_args()
    task_id = args.task
    experiment_id = args.experiment

    channel = grpc.insecure_channel(
        ast.literal_eval(USER_CONFIG.get("default", "master_address"))
    )
    stub = master_pb2_grpc.MasterStub(channel)

    if experiment_id:
        if task_id:
            print("Only experiment will be killed. Please use one option at a time.")
        request = master_pb2.Experiment(
            experiment_id=experiment_id
        )  # pylint: disable=no-member
        task_status_arr = stub.kill_experiment(
            request
        ).task_status_array.task_status_array
    elif task_id:
        request = master_pb2.Task(task_id=task_id)  # pylint: disable=no-member
        task_status_arr = [stub.kill_task(request)]
    else:
        print(
            "usage: exs [-h] -t TASK [-e EXPERIMENT]\n"
            + "exs: error: the following arguments are required: -t/--task or -e/--experiment"
        )

    for task_status in task_status_arr:
        if task_status.status in [
            master_pb2.TaskStatus.Status.KILLED,
            master_pb2.TaskStatus.Status.DONE,
        ]:
            print(f"task {task_status.task_id} is deleted")
        else:
            print(f"fail to delete {task_status.task_id} task")
