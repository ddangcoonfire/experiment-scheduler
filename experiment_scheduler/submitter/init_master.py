"""
Command script for exs init_master
"""
from pyfiglet import Figlet

from experiment_scheduler.submitter import server_on


def main():
    """
    run master grpc server on
    :return:
    """
    print(Figlet(font='slant', width=200, justify='center').renderText('Experiment Scheduler'))
    server_on("master", "master/master.py")
