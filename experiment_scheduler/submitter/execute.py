"""
[TODO] exs execute command Explanation

"""
import argparse
import ast
import os
import yaml
import grpc
from experiment_scheduler.common.settings import USER_CONFIG
from experiment_scheduler.master.grpc_master import master_pb2
from experiment_scheduler.master.grpc_master import master_pb2_grpc


def parse_args():
    """
    Parse file name option argument.
    - ex) if exs command includes "-f sample.yaml", return "sample.yaml"
    """

    parser = argparse.ArgumentParser(description="Execute exeperiments.")
    parser.add_argument("-f", "--file")
    return parser.parse_args()


def parse_input_file(parsed_yaml):
    """
    Parse yaml and change yaml shape to experiment statement shape for grpc
    """
    input = master_pb2.ExperimentStatement(
        name=parsed_yaml["name"],
        tasks=[
            master_pb2.MasterTaskStatement(
                command=task["cmd"], name=task["name"], task_env=os.environ.copy()
            )
            for task in parsed_yaml["tasks"]
        ],
    )
    return input


def main():
    """
    exs execute command calls this function.
    when this func called, open yaml with '-f' option and convert yaml shape to experiment statement shape for grpc
    """
    args = parse_args()
    file_path = args.file

    with open(file_path) as f:
        parsed_yaml = yaml.load(f, Loader=yaml.FullLoader)
    channel = grpc.insecure_channel(
        ast.literal_eval(USER_CONFIG.get("default", "master_address"))
    )
    stub = master_pb2_grpc.MasterStub(channel)

    request = parse_input_file(parsed_yaml)
    response = stub.request_experiments(request)

    if response.response == master_pb2.MasterResponse.ResponseStatus.SUCCESS:
        print("experiment id is", response.experiment_id)
    else:
        print("fail to request experiments")

if __name__ == "__main__":
    main()
