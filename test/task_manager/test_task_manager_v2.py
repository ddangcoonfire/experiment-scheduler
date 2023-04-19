import pytest

from experiment_scheduler.master.grpc_master import master_pb2
from experiment_scheduler.task_manager import task_manager_server
from experiment_scheduler.task_manager.grpc_task_manager import (
    task_manager_pb2,
    task_manager_pb2_grpc,
)
from experiment_scheduler.task_manager.grpc_task_manager.task_manager_pb2 import (
    ServerStatus,
    TaskStatement,
)
from experiment_scheduler.task_manager.task_manager_server import TaskManagerServicer


class MockTask:
    def __init__(self, pid, return_code=0):
        self.pid = pid
        self.return_code = return_code

    def get_return_code(self):
        return self.return_code


class TestTaskManager:
    @pytest.fixture(autouse=True)
    def init(self, mocker):
        mocker.patch.object(task_manager_server, "Thread")
        self.mock_resource_manager = mocker.MagicMock()
        mocker.patch.object(task_manager_server, "ResourceManager", return_value=self.mock_resource_manager)
        self.task_manger_server = TaskManagerServicer()

    def test_get_dead_tasks(self, mocker):
        self.task_manger_server.tasks.update([
            ("1", MockTask(1)), ("2", MockTask(2, 1)), ("3", MockTask(3, None)),
        ])
        mock_master_pb2_grpc = mocker.patch.object(task_manager_server, "master_pb2_grpc")
        mock_stub = mocker.MagicMock()
        mock_master_pb2_grpc.MasterStub.return_value = mock_stub

        # excute
        # trick to escape an infinite loop
        mock_time = mocker.patch.object(task_manager_server, "time")
        def mock_time_sleep(*args, **kwargs):
            raise RuntimeError
        mock_time.sleep = mock_time_sleep
        with pytest.raises(RuntimeError):
            self.task_manger_server.get_dead_tasks()

        # check
        assert "2" not in self.task_manger_server.tasks
        mock_stub.request_anomaly_exited_tasks.assert_called_once_with(
            master_pb2.TaskList(task_list=[master_pb2.Task(task_id="2")])
        )
        self.mock_resource_manager.release_resource.assert_called_once()
