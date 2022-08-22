import time
from experiment_scheduler.master.master import Master
import grpc
from concurrent import futures
from experiment_scheduler.master.grpc_master.master_pb2_grpc import add_MasterServicer_to_server, MasterStub
from experiment_scheduler.master.grpc_master.master_pb2 import ExperimentStatement, MasterTaskStatement, \
    MasterResponse
from experiment_scheduler.task_manager.grpc_task_manager.task_manager_pb2_grpc import add_TaskManagerServicer_to_server, \
    TaskManagerStub
from experiment_scheduler.task_manager.task_manager_server import TaskManagerServicer
from multiprocessing import Process,set_start_method


def turn_master_on():
    master = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    add_MasterServicer_to_server(Master(), master)
    master.add_insecure_port('[::]:50052')
    print("Turn master on for testing")
    master.start()
    master.wait_for_termination()


def turn_task_manager_on():
    task_manager = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    add_TaskManagerServicer_to_server(TaskManagerServicer(), task_manager)
    task_manager.add_insecure_port('[::]:50051')
    print("Turn task manager on for testing")
    task_manager.start()
    task_manager.wait_for_termination()


class MasterTester:
    def __init__(self):
        master_process = Process(target=turn_master_on, )
        master_process.start()
        task_manager_process = Process(target=turn_task_manager_on, )
        task_manager_process.start()
        time.sleep(1)
        self.task_manager_stub = TaskManagerStub(grpc.insecure_channel("localhost:50051"))
        self.master_stub = MasterStub(grpc.insecure_channel("localhost:50052"))

    def test_master(self):
        self._request_experiments_test()
        self._script_running_test()
        self._submitter_request_test()

    def _submitter_request_test(self):
        # from experiment_scheduler.submitter.exs import exs_init_master
        # exs_init_master()
        # [TODO] Set assert logic + Redefine test method
        pass

    def _script_running_test(self):
        master_task_statement = MasterTaskStatement()
        master_task_statement.command = "python test/master/example/test.py"
        master_task_statement.name = "run_script"
        master_task_statement.task_env["RUNNING_SCRIPT"] = "WORKING"
        protobuf = ExperimentStatement(name="test2", tasks=[master_task_statement])
        response = self.master_stub.request_experiments(protobuf)
        print(response.experiment_id)
        assert type(response.experiment_id) is str
        assert response.response is MasterResponse.ResponseStatus.SUCCESS

    def _request_experiments_test(self):
        master_task_statement = MasterTaskStatement()
        master_task_statement.command = "echo $a"
        master_task_statement.name = "name1"
        master_task_statement.task_env["a"] = "b"
        protobuf = ExperimentStatement(name="test1", tasks=[master_task_statement])
        response = self.master_stub.request_experiments(protobuf)
        assert type(response.experiment_id) is str
        assert response.response is MasterResponse.ResponseStatus.SUCCESS

    def run_unit_test(self):
        pass


if __name__ == "__main__":
    set_start_method("fork")
    tester = MasterTester()
    tester.run_unit_test()
    tester.test_master()
