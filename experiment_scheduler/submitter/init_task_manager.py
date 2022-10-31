"""
Command script for exs init_task_manager
"""
from experiment_scheduler.submitter import server_on


def main():
    """
    run task_manager grpc server on
    :return:
    """
    server_on("task manager", "task_manager/task_manager_server.py")
