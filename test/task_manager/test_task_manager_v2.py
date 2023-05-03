import pytest
import pynvml

from experiment_scheduler.master.grpc_master import master_pb2
from experiment_scheduler.task_manager import task_manager_server
from experiment_scheduler.task_manager.grpc_task_manager import (
    task_manager_pb2,
    task_manager_pb2_grpc,
)
from experiment_scheduler.common.settings import USER_CONFIG
from experiment_scheduler.task_manager.grpc_task_manager.task_manager_pb2 import (
    ServerStatus,
    TaskStatement,
    TaskStatus,
)
from experiment_scheduler.task_manager.task_manager_server import TaskManagerServicer, ResourceManager


class MockTask:
    def __init__(self, pid, return_code=0):
        self.pid = pid
        self.return_code = return_code

    def get_return_code(self):
        return self.return_code


class TestTaskManager:
    @pytest.fixture(autouse=True)
    def init(self, mocker):
        self.mock_thread = mocker.patch.object(task_manager_server, "Thread")
        self.mock_pynvml = mocker.patch.object(task_manager_server, "pynvml")
        self.mock_pynvml.nvmlDeviceGetCount.return_value = 4

    @pytest.fixture
    def mock_resource_manager(self, mocker):
        self.mock_resource_manager_instance = mocker.MagicMock()
        self.mock_resource_manager_class = mocker.patch.object(task_manager_server, "ResourceManager", return_value=self.mock_resource_manager_instance)

    def test_init(self, mock_resource_manager):
        TaskManagerServicer()
        self.mock_resource_manager_class.assert_called_once_with(4)

    def test_use_gpu(self):
        task_manger_server = TaskManagerServicer()
        assert task_manger_server.use_gpu

    def test_health_check(self, mocker):
        task_manger_server = TaskManagerServicer()

        assert task_manger_server.health_check(mocker.MagicMock(), mocker.MagicMock()) == ServerStatus(alive=True)

    def test_run_task(self, mocker, mock_resource_manager):
        # prepare
        task_id = "1"
        task_statement = TaskStatement(
            task_id=task_id, command="command", name="name", task_env={"CUDA_VISIBLE_DEVICES" : "0"})
        self.mock_resource_manager_instance.get_resource.return_value = 0
        mock_popen = mocker.MagicMock()
        mock_popen.pid = 1234
        mock_subprocess = mocker.patch.object(task_manager_server, "subprocess")
        mock_subprocess.Popen.return_value = mock_popen

        # execute
        task_manger_server = TaskManagerServicer()
        assert task_manger_server.run_task(task_statement, mocker.MagicMock()) == TaskStatus(task_id=task_id, status=TaskStatus.Status.RUNNING)

        # check
        assert task_id in task_manger_server.tasks
        mock_subprocess.Popen.assert_called_once()
        popen_call_args = mock_subprocess.Popen.call_args.kwargs
        assert popen_call_args["env"]["CUDA_VISIBLE_DEVICES"] == "0"
        assert popen_call_args["args"] == "command"

    def test_get_dead_tasks(self, mocker, mock_resource_manager):
        task_manger_server = TaskManagerServicer()

        task_manger_server.tasks.update([
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
            task_manger_server.get_dead_tasks()

        # check
        assert "2" not in task_manger_server.tasks
        mock_stub.request_abnormal_exited_tasks.assert_called_once_with(
            master_pb2.TaskList(task_list=[master_pb2.Task(task_id="2")])
        )
        self.mock_resource_manager_instance.release_resource.assert_called_once()
