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
    Progress,
    ProgressResponse,
    IdleResources,
)
from experiment_scheduler.task_manager.task_manager_server import TaskManagerServicer, ResourceManager


class MockTask:
    def __init__(self, pid, return_code=0, kill_flag=True):
        self.pid = pid
        self.return_code = return_code
        self.kill_flag = kill_flag

    def get_return_code(self):
        return self.return_code
    
    def kill_process_tree(self, include_me=True):
        if self.kill_flag:
            return [1], []
        else:
            return [], [1]
    
    def is_child_pid(self, pid):
        return False
            


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
    
    def add_mock_tasks(self, task_manager_server):
        task_manager_server.tasks.update([
            ("1", MockTask(1)), ("2", MockTask(2, 1)), ("3", MockTask(3, None)), ("killed_abnormally", MockTask(4, None, False))
        ])

    def test_get_dead_tasks(self, mocker, mock_resource_manager):
        task_manager_server = TaskManagerServicer()
        self.add_mock_tasks(task_manager_server)

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
            task_manager_server.get_dead_tasks()

        # check
        assert "2" not in task_manager_server.tasks
        mock_stub.request_abnormal_exited_tasks.assert_called_once_with(
            master_pb2.TaskList(task_list=[master_pb2.Task(task_id="2")])
        )
        self.mock_resource_manager_instance.release_resource.assert_called_once()

    @pytest.mark.parametrize("status,return_value", [
            (TaskStatus.Status.KILLED, None),
            (TaskStatus.Status.DONE, 0),
        ]
    )
    def test_kill_task(self, mocker, status, return_value):
        task_manager_server = TaskManagerServicer()
        task_manager_server.tasks["task_id"] = MockTask(1, return_value)
        task_statement1 = TaskStatement(
            task_id="task_id", command="command", name="name", task_env={"CUDA_VISIBLE_DEVICES" : "0"})
        
        task_status1 = task_manager_server.kill_task(task_statement1, mocker.MagicMock())
        assert task_status1 == TaskStatus(task_id="task_id", status=status)

    def test_kill_task_not_found(self, mocker):
        task_manager_server = TaskManagerServicer()
        task_statement1 = TaskStatement(
            task_id="task_id", command="command", name="name", task_env={"CUDA_VISIBLE_DEVICES" : "0"})
        
        task_status1 = task_manager_server.kill_task(task_statement1, mocker.MagicMock())

        assert task_status1 == TaskStatus(task_id="task_id", status=TaskStatus.Status.NOTFOUND)

    def test_kill_task_abnormal(self, mocker):
        task_manager_server = TaskManagerServicer()
        task_manager_server.tasks["task_id"] = MockTask(1, None, False)
        task_statement1 = TaskStatement(
            task_id="task_id", command="command", name="name", task_env={"CUDA_VISIBLE_DEVICES" : "0"})

        task_status1 = task_manager_server.kill_task(task_statement1, mocker.MagicMock())

        assert task_status1 == TaskStatus(task_id="task_id", status=TaskStatus.Status.ABNORMAL)

    @pytest.mark.parametrize("status,return_value", [
            (TaskStatus.Status.DONE, 0),
            (TaskStatus.Status.ABNORMAL, 1),
            (TaskStatus.Status.RUNNING, None),
        ]
    )
    def test_get_task_status(self, mocker, status, return_value):
        task_manager_server = TaskManagerServicer()
        task_manager_server.tasks["task_id"] = MockTask(1, return_value)

        task_statement1 = TaskStatement(
            task_id="task_id", command="command", name="name", task_env={"CUDA_VISIBLE_DEVICES" : "0"})

        task_status1 = task_manager_server.get_task_status(task_statement1, mocker.MagicMock())
        assert task_status1 == TaskStatus(task_id="task_id", status= status)

    def test_get_task_status_not_found(self, mocker):
        task_manager_server = TaskManagerServicer()
        task_statement1 = TaskStatement(
            task_id="task_id", command="command", name="name", task_env={"CUDA_VISIBLE_DEVICES" : "0"})

        task_status1 = task_manager_server.get_task_status(task_statement1, mocker.MagicMock())
        assert task_status1 == TaskStatus(task_id="task_id", status= TaskStatus.NOTFOUND)


    def test_get_all_tasks(self, mocker):
        task_manager_server = TaskManagerServicer()
        self.add_mock_tasks(task_manager_server)

        all_task_status = task_manager_server.get_all_tasks(mocker.MagicMock(), mocker.MagicMock())

        assert all_task_status.task_status_array == [
            TaskStatus(task_id="1", status= TaskStatus.Status.DONE),
            TaskStatus(task_id="2", status= TaskStatus.Status.ABNORMAL),
            TaskStatus(task_id="3", status= TaskStatus.Status.RUNNING),
            TaskStatus(task_id="killed_abnormally", status= TaskStatus.Status.RUNNING),
            ]
    @pytest.mark.parametrize("return_value", [True, False])
    def test_has_idle_resource(self, mocker, return_value, mock_resource_manager):
        task_manager_server = TaskManagerServicer()

        self.mock_resource_manager_instance.has_available_resource.return_value = return_value
        test_idle1 = task_manager_server.has_idle_resource(mocker.MagicMock(), mocker.MagicMock())
        assert test_idle1 == IdleResources(exists=return_value)

    def test_report_progress(self, mocker):
        task_manager_server = TaskManagerServicer()
        pid = 1234
        mock_task_instance = mocker.MagicMock()
        mock_task_instance.pid = pid
        mock_task_instance.is_child_pid.return_value = False
        task_manager_server.tasks.update([("mock", mock_task_instance)])
        test_progress_mock = Progress(progress=1., leap_second=0.1, pid=pid)
        test_response_mock = task_manager_server.report_progress(test_progress_mock, mocker.MagicMock())

        assert mock_task_instance.register_progess.called_once_with(1., 0.1)
        assert test_response_mock == ProgressResponse(received_status=ProgressResponse.ReceivedStatus.SUCCESS)

    def test_report_progress_fail(self, mocker):
        task_manager_server = TaskManagerServicer()
        self.add_mock_tasks(task_manager_server)

        test_progress1 = Progress(progress=1., leap_second=0.1, pid=5)
        test_response1 = task_manager_server.report_progress(test_progress1, mocker.MagicMock())
        assert test_response1 == ProgressResponse(
                                    received_status=ProgressResponse.ReceivedStatus.FAIL)
