import os
from subprocess import PIPE, run
import time

from experiment_scheduler import submitter
from experiment_scheduler.master.grpc_master import master_pb2
from experiment_scheduler.master.master import Master
from experiment_scheduler.resource_monitor.resource_monitor import ResourceMonitor
import grpc
from concurrent import futures
from experiment_scheduler.master.grpc_master.master_pb2_grpc import (
    add_MasterServicer_to_server,
    MasterStub,
)
from experiment_scheduler.master.grpc_master.master_pb2 import (
    ExperimentStatement,
    MasterTaskStatement,
    MasterResponse,
    TaskStatus,
)
from experiment_scheduler.task_manager.grpc_task_manager.task_manager_pb2_grpc import (
    add_TaskManagerServicer_to_server,
    TaskManagerStub,
)
from experiment_scheduler.task_manager.task_manager_server import TaskManagerServicer
from experiment_scheduler.resource_monitor.grpc_resource_monitor.resource_monitor_pb2_grpc import (
    add_ResourceMonitorServicer_to_server,
    ResourceMonitorStub,
)
from multiprocessing import Process, set_start_method

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), "sample.yaml")


def turn_resource_monitor_on():
    resource_monitor = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    add_ResourceMonitorServicer_to_server(ResourceMonitor(), resource_monitor)
    resource_monitor.add_insecure_port("[::]:50053")
    print("Turn resource_monitor on for testing")
    resource_monitor.start()
    resource_monitor.wait_for_termination()


def turn_master_on():
    master = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    add_MasterServicer_to_server(Master(), master)
    master.add_insecure_port("[::]:50052")
    print("Turn master on for testing")
    master.start()
    master.wait_for_termination()


def turn_task_manager_on():
    task_manager = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    add_TaskManagerServicer_to_server(TaskManagerServicer(), task_manager)
    task_manager.add_insecure_port("[::]:50051")
    print("Turn task manager on for testing")
    task_manager.start()
    task_manager.wait_for_termination()


class MasterTester:
    def __init__(self):
        master_process = Process(
            target=turn_master_on,
        )
        master_process.start()
        task_manager_process = Process(
            target=turn_task_manager_on,
        )
        task_manager_process.start()
        resource_monitor = Process(
            target=turn_resource_monitor_on(),
        )
        resource_monitor.start()
        time.sleep(1)
        self.task_manager_stub = TaskManagerStub(
            grpc.insecure_channel("localhost:50051")
        )
        self.master_stub = MasterStub(grpc.insecure_channel("localhost:50052"))
        self.resource_monitor_listener_stub = ResourceMonitorStub(
            grpc.insecure_channel("localhost:50053")
        )

    def test_master(self):
        self._request_experiments_test()
        self._script_running_test()
        self._submitter_request_test()

    async def _submitter_request_test(self):
        submitter.server_on()

        def out(command):
            result = run(
                command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True
            )
            return result.stdout

        response = await out("exs execute -f sample.yaml")
        print("result:: ", response)
        assert type(response.experiment_id) is str
        assert response.response is MasterResponse.ResponseStatus.SUCCESS

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
        response = self._run_example_experiment("name1", "test1")
        assert type(response.experiment_id) is str
        assert response.response is MasterResponse.ResponseStatus.SUCCESS

    def run_unit_test(self):
        self._run_example_experiment("name2", "test2")
        status_list = self.master_stub.get_task_status(
            master_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        )
        assert type(status_list) is master_pb2.AllTasksStatus
        get_status_response = self.master_stub.get_task_status(status_list[0][0])
        assert type(get_status_response.task_id) is str
        assert get_status_response.response is (
            TaskStatus.Status.DONE
            or TaskStatus.Status.RUNNING
            or TaskStatus.Status.NOTFOUND
        )
        kill_response = self.master_stub.kill_task(status_list[0][0])
        assert type(kill_response.task_id) is str
        assert kill_response.response is (
            TaskStatus.Status.KILLED or TaskStatus.Status.DONE
        )

    def _run_example_experiment(self, name, test_name):
        master_task_statement = MasterTaskStatement()
        master_task_statement.command = "echo $a"
        master_task_statement.name = name
        master_task_statement.task_env["a"] = "b"
        protobuf = ExperimentStatement(name=test_name, tasks=[master_task_statement])
        response = self.master_stub.request_experiments(protobuf)
        return response


if __name__ == "__main__":
    tester = MasterTester()
    tester.run_unit_test()
    tester.test_master()
