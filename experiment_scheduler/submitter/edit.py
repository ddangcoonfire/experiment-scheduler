"""
exs edit --tid [task_id] --cmd [cmd]
If certain task need to be re-run with new configuration, use exs edit
"""
import argparse
import ast
import grpc
from experiment_scheduler.common.settings import USER_CONFIG
from experiment_scheduler.master.grpc_master import master_pb2
from experiment_scheduler.master.grpc_master import master_pb2_grpc


def parse_args():
    """
    parse only tid, cmd option.
    :return: parsed_arguments
    """
    parser = argparse.ArgumentParser(description="Execute exeperiments.")
    parser.add_argument("-t", "--tid")
    parser.add_argument("-c", "--cmd")
    return parser.parse_args()


def main():
    """
    run exs edit

    :return:
    """
    args = parse_args()
    task_id = args.tid
    cmd = args.cmd

    channel = grpc.insecure_channel(
        ast.literal_eval(USER_CONFIG.get("default", "master_address"))
    )
    stub = master_pb2_grpc.MasterStub(channel)

    request = master_pb2.EditTask(task_id=task_id, cmd=cmd)
    response = stub.edit_task(request)

    # pylint: disable=no-member
    if response.status == master_pb2.MasterResponse.ResponseStatus.FAIL:
        print(
            f"Cannot edit {task_id}. Task does not exist or Already finished".format(
                task_id=request.task_id
            )
        )
    else:
        print("Success")
