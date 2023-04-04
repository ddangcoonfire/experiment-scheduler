import subprocess
import re
from pathlib import Path
from typing import Union

from experiment_scheduler.master import grpc_master
from experiment_scheduler.task_manager import grpc_task_manager

try:
    import grpc_tools
except ImportError:
    grpc_tools = None


PROTO_PATH = [grpc_master, grpc_task_manager]

    
def compile_proto_file(proto_file: Union[str, Path]):
    proto_file = Path(proto_file)
    subprocess.run([
        "python", "-m", "grpc_tools.protoc",
        f"--proto_path={proto_file.parent}",
        f"--python_out={proto_file.parent}",
        f"--pyi_out={proto_file.parent}",
        f"--grpc_python_out={proto_file.parent}",
        str(proto_file)
    ])

    pb2_grpc_file = proto_file.parent / f"{proto_file.stem}_pb2_grpc.py"
    with pb2_grpc_file.open("r") as f:
        lines = f.readlines()

    pb2_file = f"{proto_file.stem}_pb2"
    abs_pb2_file = pb2_file
    for key in reversed(proto_file.parent.parts):
        abs_pb2_file = f"{key}." + abs_pb2_file 
        if key == "experiment_scheduler":
            break

    with pb2_grpc_file.open("w") as f:
        for line in lines:
            if  pb2_file in line:
                line = re.sub(rf'{pb2_file}', rf'{abs_pb2_file}', line)
            f.write(line)


def main():
    if grpc_tools is None:
        import grpc
        print(f"grpc_tools isn't installed. Please install grpc_tools=={grpc.__version__}")
        return

    for sub_package in PROTO_PATH:
        pkg_using_proto = Path(sub_package.__file__).parent 
        for proto_file in pkg_using_proto.rglob("*.proto"):
            compile_proto_file(proto_file)


if __name__ == "__main__":
    main()
