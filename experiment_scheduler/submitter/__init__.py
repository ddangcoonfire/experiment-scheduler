"""
submitter is for
[TODO] docstring
"""
import sys
import subprocess
import os

from experiment_scheduler.common.settings import DEFAULT_EXS_HOME


def server_on(target, script_location):
    """
    run grpc server on
    :return:
    """
    command = [
        sys.executable,
        "-u",
        os.path.join(DEFAULT_EXS_HOME, script_location),
    ]  # pylint: disable=R1732
    print(f"{target} is initiated. Please wait for a second...")
    task = subprocess.Popen(
        args=command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    # [TODO] Add Address
    print(f"{target} is now set")
    while True:
        output = task.stdout.readline().decode("utf-8")
        if len(output) > 0:
            print(output, end="")
        sys.stdout.flush()
