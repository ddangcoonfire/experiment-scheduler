"""
submitter is for
[TODO] docstring
"""
import argparse
import datetime
import os
import signal
import subprocess
import sys
from experiment_scheduler.common.settings import DEFAULT_EXS_HOME


def parse_args():
    """
    Parse user's arguments.
    """

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-d", "--daemon", action="store_true")
    return parser.parse_known_args()[0]


def _run_as_default_process(command, target):
    with subprocess.Popen(
        args=command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    ) as task:
        print(f"now {target} is running")
        try:
            for line in iter(task.stdout.readline, b""):
                print(line.decode("utf-8"))
        except KeyboardInterrupt:
            os.kill(task.pid, signal.SIGINT)
            task.wait()


def _run_as_daemon_process(command, target):
    file_name = (
        f"{target}-{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-log.txt"
    )
    with open(file_name, "w", encoding="utf-8") as log_file:
        with subprocess.Popen(
            args=command,
            stdout=log_file,
            stderr=log_file,
        ):
            print(f"now {target} is running.")
            print(f"tracking logs in {file_name}")


def server_on(target, script_location):
    """
    run grpc server on
    :return:
    """
    arguments = parse_args()
    command = [
        sys.executable,
        "-u",
        os.path.join(DEFAULT_EXS_HOME, script_location),
    ]  # pylint: disable=R1732
    print(f"{target} is initiated. Please wait for a second...")
    if arguments.daemon:
        _run_as_daemon_process(command, target)
    else:
        _run_as_default_process(command, target)
