import argparse
import sys

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
    COMMAND_LIST[name]()


if __name__ == "__main__":
    main()
