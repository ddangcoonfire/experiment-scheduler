"""
Command script for exs init_resource_monitor
"""
from experiment_scheduler.submitter import server_on


def main():
    """
    run resource_monitor server on
    :return:
    """
    server_on("resource monitor", "resource_monitor/resource_monitor.py")
