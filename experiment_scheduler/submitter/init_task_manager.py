import os
import subprocess
import sys
from experiment_scheduler.common.settings import DEFAULT_EXS_HOME

# [TODO] daemon option

def main():
    exs_home = os.getenv("EXS_HOME")
    # [TODO] set task_manager's path as constant in settings
    command = ([sys.executable, "-u", os.path.join(DEFAULT_EXS_HOME,"task_manager/task_manager_server.py")])
    print("Task manager is initiated. Please wait for a second...")
    task = subprocess.Popen(
        args=command,
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    # [TODO] Add Address
    print("Task manager is now set.")
    while True:
        output = task.stdout.readline().decode('utf-8')
        if len(output) > 0:
            print(output, end='')





