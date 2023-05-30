"""
[TODO] exs command Explanation

"""

import argparse
import sys

import grpc

from experiment_scheduler.submitter.execute import main as exs_execute
from experiment_scheduler.submitter.delete import main as exs_delete
from experiment_scheduler.submitter.edit import main as exs_edit
from experiment_scheduler.submitter.log import main as exs_log
from experiment_scheduler.submitter.init_master import main as exs_init_master
from experiment_scheduler.submitter.init_resource_monitor import (
    main as exs_init_resource_monitor,
)
from experiment_scheduler.submitter.init_task_manager import (
    main as exs_init_task_manager,
)
from experiment_scheduler.submitter.list import main as exs_list
from experiment_scheduler.submitter.status import main as exs_status
from experiment_scheduler.submitter.compile_protobuf import main as exs_compile

COMMAND_LIST = {
    "execute": exs_execute,
    "delete": exs_delete,
    "edit": exs_edit,
    "list": exs_list,
    "status": exs_status,
    "log": exs_log,
    "init_master": exs_init_master,
    "init_task_manager": exs_init_task_manager,
    "init_resource_monitor": exs_init_resource_monitor,
    "grpc_compile": exs_compile,
}

HELP_MESSAGE = {
    "execute": "execute python task",
    "delete": "delete running (or queued) task",
    "edit": "edit task",
    "list": "list all registered tasks",
    "status": "get status of running tasks",
    "log": "get log of the specific task",
    "init_master": "init master server",
    "init_task_manager": "init task manager server",
    "init_resource_monitor": "init resource monitor server",
}


class CustomArgumentParser(argparse.ArgumentParser):
    """
    When a "command not found" error occurs, it displays a help message.
    """

    def error(self, message):
        """
        Custom error function
        """
        print(f"command not found: {message}")
        self.print_help()
        self.exit(2)


def parse_args():
    """
    Parse user's arguments.
    """
    parser = CustomArgumentParser(
        add_help=True, formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "operation",
        choices=COMMAND_LIST,
        metavar="OPERATION",
        help="\n".join(
            "{}: {}".format(key, value)  # pylint: disable=consider-using-f-string
            for key, value in HELP_MESSAGE.items()
        ),
    )
    parser.add_argument(
        "-d",
        "--daemon",
        action="store_true",
        help="Run servers as daemon state. Only valid at init_* commands",
    )

    return parser.parse_known_args()[0]


def main():
    """
    Select and execute a function from the command list.
    """
    name = parse_args().operation
    del sys.argv[sys.argv.index(name)]
    try:
        COMMAND_LIST[name]()
    except grpc.RpcError as err:
        if err.code() == grpc.StatusCode.UNAVAILABLE:
            print(">>> Cannot connect to master.... Check connection status")
        else:
            print(err.details())

if __name__ == "__main__":
    main()
