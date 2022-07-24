import argparse
import sys

import grpc
from experiment_scheduler.master.grpc_repo import master_pb2
from experiment_scheduler.master.grpc_repo import master_pb2_grpc

from .execute import main as exs_execute
from .delete import main as exs_delete
from .edit import main as exs_edit
from .list import main as exs_list
from .status import main as exs_status


COMMAND_LIST = {
    "execute" : exs_execute,
    "delete" : exs_delete,
    "edit" : exs_edit,
    "list" : exs_list,
    "status" : exs_status,
}


def parse_args():
    """
    Parse user's arguments.
    """

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("operation", choices=[x for x in COMMAND_LIST.keys()])

    return parser.parse_known_args()[0]

def parse_input(parsed_yaml):
    input = master_pb2.ExperiemntStatement(
        name= parsed_yaml['name'],
        tasks= [master_pb2.TaskStatement(
            command = task['cmd'],
            name = task['name'],
            condition = master_pb2.TaskCondition(gpuidx= task['condition']['gpu'])
            ) for task in parsed_yaml['tasks']
        ]
    )
    return input

def main():
    """
    Select and execute a function from the command list.
    """

    channel = grpc.insecure_channel('localhost:50049')
    stub = master_pb2_grpc.MasterStub(channel)

    name = parse_args().operation
    del sys.argv[1]


    request = COMMAND_LIST[name]()

    if name == "execute":
        request = parse_input(request)

    response = stub.request_experiment(request)
    if (response.response == 0):
        print(response.experiment_id)
    else:
        print("fail")

if __name__ == "__main__":
    main()


