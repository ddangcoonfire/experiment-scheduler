from experiment_scheduler.common import settings
import os
import subprocess
import time
import sys
# [TODO] daemon option


def main():
    exs_home = os.getenv("EXS_HOME")
    # [TODO] set master's path as constant in settings
    command = ([sys.executable, "-u", os.path.join(exs_home, "master/master.py")])
    print("Master is initiated. Please wait for a second...")
    task = subprocess.Popen(
        args=command,
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    # [TODO] Add Address
    print("Master is now set")
    while True:
        output = task.stdout.readline().decode('utf-8')
        if len(output) > 0:
            print(output, end='')
        sys.stdout.flush()






