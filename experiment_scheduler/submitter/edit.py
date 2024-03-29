"""
exs edit --task-id [task_id] --cmd [cmd]
If certain task need to be re-run with new configuration, use exs edit
"""
import argparse
import ast
import os
import grpc
from experiment_scheduler.common.settings import USER_CONFIG
from experiment_scheduler.master.grpc_master import master_pb2
from experiment_scheduler.master.grpc_master import master_pb2_grpc


def parse_args():
    """
    parse only task-id, cmd option.
    :return: parsed_arguments
    """
    parser = argparse.ArgumentParser(description="Execute exeperiments.")
    parser.add_argument("-t", "--task-id", required=True)
    parser.add_argument("-c", "--cmd", required=True)
    return parser.parse_args()


def main():
    """
    run exs edit

    :return:
    """
    args = parse_args()
    task_id = args.task_id
    cmd = args.cmd

    channel = grpc.insecure_channel(
        ast.literal_eval(USER_CONFIG.get("default", "master_address"))
    )
    stub = master_pb2_grpc.MasterStub(channel)

    request = master_pb2.EditTask(  # pylint: disable=no-member
        task_id=task_id, cmd=cmd, task_env=os.environ.copy()
    )
    response = stub.edit_task(request)
    if (
        hasattr(master_pb2.MasterResponse, "response")
        and response.response == master_pb2.MasterResponse.ResponseStatus.FAIL
    ):
        print(
            f"Cannot edit {task_id}. Task does not exist or Already finished".format(
                task_id=request.task_id
            )
        )
    else:
        print("Success")
