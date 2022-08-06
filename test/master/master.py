import sys
sys.path.append("./")

from experiment_scheduler.master.master import Master
import grpc
from concurrent import futures
from experiment_scheduler.master.grpc_master.master_pb2_grpc import add_MasterServicer_to_server,MasterStub
from experiment_scheduler.master.grpc_master.master_pb2 import ExperimentStatement, MasterTaskStatement, MasterTaskCondition
from experiment_scheduler.task_manager.task_manager_pb2_grpc import add_TaskManagerServicer_to_server, TaskManagerStub
from experiment_scheduler.task_manager.task_manager_pb2 import TaskManager


def turn_master_on():
    master = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    add_MasterServicer_to_server(Master(), master)
    master.add_insecure_port('[::]:50050')
    master.start()
    master.wait_for_termination()


def turn_task_manager_on():
    task_manager = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    add_TaskManagerServicer_to_server(TaskManagerServicer(), task_manager)
    task_manager.add_insecure_port('[::]:50051')
    task_manager.start()
    task_manager.wait_for_termination()


class MasterTester:
    def __init__(self):
        turn_master_on()
        turn_task_manager_on()
        self.task_manager_stub = TaskManagerStub(grpc.insecure_channel("localhost:50051"))
        self.master_stub = MasterStub(grpc.insecure_channel("localhost:50050"))

    def test_master(self):
        protobuf = ExperimentStatement(name="test1",
                                       tasks=MasterTaskStatement(command="cmd1", name="name1",
                                                           condition=MasterTaskCondition(gpuidx=0)))
        response = self.master_stub.request_experiment(protobuf)
        assert type(response) is int

