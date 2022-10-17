"""
[TODO] exs execute command Explanation

"""
import ast
import yaml
import grpc
from experiment_scheduler.common.settings import USER_CONFIG
from experiment_scheduler.master.grpc_master import master_pb2
from experiment_scheduler.master.grpc_master import master_pb2_grpc
from submitter_parser import parse_args_file, parse_input_file


def main():
    """
    exs execute command calls this function.
    when this func called, open yaml with '-f' option and convert yaml shape to experiment statement shape for grpc
    """
    args = parse_args_file()
    file_path = args.file

    with open(file_path, encoding="utf-8") as file:
        parsed_yaml = yaml.load(file, Loader=yaml.FullLoader)

    channel = grpc.insecure_channel(
        ast.literal_eval(USER_CONFIG.get("default", "master_address"))
    )
    stub = master_pb2_grpc.MasterStub(channel)

    request = parse_input_file(parsed_yaml)
    response = stub.request_experiments(request)

    # pylint: disable=no-member
    if response.response == master_pb2.MasterResponse.ResponseStatus.SUCCESS:
        print("experiment id is", response.experiment_id)
    else:
        print("fail to request experiments")
