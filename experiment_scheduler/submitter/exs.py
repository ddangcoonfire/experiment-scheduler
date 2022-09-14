import argparse
import sys

from experiment_scheduler.submitter.execute import main as exs_execute
from experiment_scheduler.submitter.delete import main as exs_delete
from experiment_scheduler.submitter.edit import main as exs_edit
from experiment_scheduler.submitter.list import main as exs_list
from experiment_scheduler.submitter.status import main as exs_status
from experiment_scheduler.submitter.init_master import main as exs_init_master
from experiment_scheduler.submitter.init_task_manager import main as exs_init_task_manager


COMMAND_LIST = {
    "execute": exs_execute,
    "delete": exs_delete,
    "edit": exs_edit,
    "list": exs_list,
    "status": exs_status,
    "init_master": exs_init_master,
    "init_task_manager": exs_init_task_manager,
}


def parse_args():
    """
    Parse user's arguments.
    """

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "operation",
        choices=list(COMMAND_LIST.keys())
    )

    return parser.parse_known_args()[0]


def main():
    """
    Select and execute a function from the command list.
    """
    name = parse_args().operation
    del sys.argv[1]
    COMMAND_LIST[name]()


if __name__ == "__main__":
    main()


