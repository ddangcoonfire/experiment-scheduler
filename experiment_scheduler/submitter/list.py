"""
[TODO] exs list command Explanation
"""
import ast
import grpc
from experiment_scheduler.common.settings import USER_CONFIG
from experiment_scheduler.master.grpc_master import master_pb2_grpc, master_pb2

TASK_STATUS = [
    "waiting",
    "running",
    "done",
    "killed",
    "abnormal",
    "not found"
]

def main():
    """
    Todo
    :return:
    """
    channel = grpc.insecure_channel(
        ast.literal_eval(USER_CONFIG.get("default", "master_address"))
    )
    stub = master_pb2_grpc.MasterStub(channel)
    request = master_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
    response = stub.get_all_tasks(request)
    print(f"{'TASK ID':50}| STATUS")
    for task_status in response.task_status_array:
        print(
            f"{task_status.task_id:50}| {TASK_STATUS[task_status.status]}"
        )
