import argparse
import sys

import grpc
from ..master.grpc import master_pb2
from ..master.grpc import master_pb2_grpc

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


def main():
    """
    Select and execute a function from the command list.
    """

    name = parse_args().operation
    del sys.argv[1]
    request = COMMAND_LIST[name]()

    # channel = grpc.insecure_channel('localhost:50050')
    # stub = master_pb2_grpc.MasterStub()
    # response = stub.Add(matser_pb)

if __name__ == "__main__":
    main()


