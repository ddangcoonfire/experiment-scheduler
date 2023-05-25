"""
Command script for exs init_task_manager
"""

import argparse

from experiment_scheduler.submitter import server_on

def parse_args():
    """
    Parse file name option argument.
    - ex) if exs command includes "-f sample.yaml", return "sample.yaml"
    """

    parser = argparse.ArgumentParser(description="Run task_manager_server.")
    parser.add_argument("-i", "--ip", default="localhost")
    return parser.parse_args()


def main():
    """
    run task_manager grpc server on
    :return:
    """
    args = parse_args()
    server_on("task manager", "task_manager/task_manager_server.py", "--ip", args.ip)
