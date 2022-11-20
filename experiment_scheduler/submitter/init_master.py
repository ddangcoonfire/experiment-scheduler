"""
Command script for exs init_master
"""
from experiment_scheduler.submitter import server_on


def main():
    """
    run master grpc server on
    :return:
    """
    server_on("master", "master/master.py")
