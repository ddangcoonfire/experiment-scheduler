"""
[TODO] exs status command Explanation
"""
import ast
import grpc
from experiment_scheduler.common.settings import USER_CONFIG
from experiment_scheduler.master.grpc_master import master_pb2
from experiment_scheduler.master.grpc_master import master_pb2_grpc
from experiment_scheduler.submitter.delete import parse_args


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

    request = master_pb2.Task(task_id=task_id)
    response = stub.get_task_status(request)

    print(response)
