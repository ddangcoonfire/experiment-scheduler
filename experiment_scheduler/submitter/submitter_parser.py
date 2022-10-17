"""
[TODO] exs delete command Explanation

"""

import argparse
import master_pb2


def parse_args_task():
    """
    Parse task id option argument.
        - ex) if exs command includes "-t id-123", return "id-123"
    """
    parser = argparse.ArgumentParser(description="Delete task.")
    parser.add_argument("-t", "--task")
    return parser.parse_args()

def parse_args_file():
    """
    Parse file name option argument.
        - ex) if exs command includes "-f sample.yaml", return "sample.yaml"
    """
    parser = argparse.ArgumentParser(description="Execute exeperiments.")
    parser.add_argument("-f", "--file")
    return parser.parse_args()


def parse_input_file(parsed_yaml):
    """
    Parse yaml and change yaml shape to experiment statement shape for grpc
    """
    parsed_input = master_pb2.ExperimentStatement(
        name=parsed_yaml["name"],
        tasks=[
            master_pb2.MasterTaskStatement(
                command=task["cmd"], name=task["name"], task_env=os.environ.copy()
            )
            for task in parsed_yaml["tasks"]
        ],
    )
    return parsed_input