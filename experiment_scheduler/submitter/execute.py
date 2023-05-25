"""
[TODO] exs execute command Explanation

"""
import argparse
import ast
import os

import grpc
import yaml

from experiment_scheduler.common.settings import USER_CONFIG
from experiment_scheduler.master.grpc_master import master_pb2, master_pb2_grpc

CHUNK_SIZE = 1024 * 5


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
    input_file = master_pb2.ExperimentStatement(
        name=parsed_yaml["name"],
        tasks=[
            master_pb2.MasterTaskStatement(
                command=task["cmd"],
                name=task["name"],
                task_env=os.environ.copy(),
                files=list(map(lambda x: x.split("/")[-1], task["files"]))
                if "files" in task
                else [],
            )
            for task in parsed_yaml["tasks"]
        ],
    )
    return input_file


def main():
    """
    exs execute command calls this function.
    when this func called, open yaml with '-f' option and convert yaml shape to experiment statement shape for grpc
    """
    args = parse_args()
    file_path = args.file

    with open(file_path, "r", encoding="utf-8") as file_pointer:
        parsed_yaml = yaml.load(file_pointer, Loader=yaml.FullLoader)
    channel = grpc.insecure_channel(
        ast.literal_eval(USER_CONFIG.get("default", "master_address"))
    )
    stub = master_pb2_grpc.MasterStub(channel)

    request = parse_input_file(parsed_yaml)
    files = [task["files"] if "files" in task else [] for task in parsed_yaml["tasks"]]

    for task_files in files:
        for task_file in task_files:
            file_name = task_file.split("/")[-1]
            stub.delete_file(master_pb2.MasterFileDeleteRequest(name=file_name))
            with open(task_file, mode="rb") as file_pointer:

                def request_iterator():
                    while True:
                        data = file_pointer.read(
                            CHUNK_SIZE
                        )  # pylint:disable=cell-var-from-loop
                        if not data:
                            break
                        yield master_pb2.MasterFileUploadRequest(
                            name=file_name,  # pylint:disable=cell-var-from-loop
                            file=data,
                        )

                stub.upload_file(request_iterator())

    response = stub.request_experiments(request)

    if response.response == master_pb2.MasterResponse.ResponseStatus.SUCCESS:
        print("experiment id is", response.experiment_id)
    else:
        print("fail to request experiments")
