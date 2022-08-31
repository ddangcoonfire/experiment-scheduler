import os
import signal
from os import path as osp

import pytest
from experiment_scheduler.task_manager import task_manager_server
from experiment_scheduler.task_manager.grpc_task_manager import task_manager_pb2, task_manager_pb2_grpc
from experiment_scheduler.task_manager.grpc_task_manager.task_manager_pb2 import ServerStatus, TaskStatement
from experiment_scheduler.task_manager.task_manager_server import TaskManagerServicer


@pytest.fixture
def task_manager_service(tmp_path):
    return TaskManagerServicer(tmp_path)

class MockTask:
    def __init__(self, task_id):
        self.task_id = task_id

    @staticmethod
    def poll():
        return None

    @staticmethod
    def terminate():
        return None

    @staticmethod
    def wait():
        return None


class MockRunTask(MockTask):
    def __init__(self, task_id):
        self.task_id = task_id


class MockDoneTask(MockTask):
    def __init__(self, task_id):
        self.task_id = task_id

    @staticmethod
    def poll():
        return 0


class MockKilledTask(MockTask):
    def __init__(self, task_id):
        self.task_id = task_id

    @staticmethod
    def poll():
        return -signal.SIGTERM


class MockRequest:
    def __init__(self, task_id):
        self.task_id = task_id


class mock_task_id:
    def __init__(self):
        self.status = {'RUNNING': '1', 'DONE': '2', 'KILLED': '3', 'NOTFOUND': '4'}


class TestClass:

    task_id = mock_task_id()

    @pytest.fixture
    def task_manager_servicer(self):
        task_id = mock_task_id()
        task_manager_servicer = task_manager_server.TaskManagerServicer(task_manager_pb2_grpc.TaskManagerServicer)
        task_manager_servicer.tasks[task_id.status['RUNNING']] = MockRunTask(task_id.status['RUNNING'])
        task_manager_servicer.tasks[task_id.status['DONE']] = MockDoneTask(task_id.status['DONE'])
        task_manager_servicer.tasks[task_id.status['KILLED']] = MockKilledTask(task_id.status['KILLED'])
        return task_manager_servicer

    @pytest.mark.parametrize('requested', [MockRequest(task_id.status['NOTFOUND'])])
    def test_kill_not_found_task(self, requested, task_manager_servicer):
        assert task_manager_servicer.kill_task(requested, '') == task_manager_pb2.TaskStatus(task_id=requested.task_id,
                                                                                             status=task_manager_pb2.
                                                                                             TaskStatus.Status.NOTFOUND)

    @pytest.mark.parametrize('requested', [MockRequest(task_id.status['DONE'])])
    def test_kill_done_task(self, requested, task_manager_servicer):
        assert task_manager_servicer.kill_task(requested, '') == task_manager_pb2.TaskStatus(task_id=requested.task_id,
                                                                                             status=task_manager_pb2.
                                                                                             TaskStatus.Status.DONE)

    @pytest.mark.parametrize('requested', [MockRequest(task_id.status['RUNNING'])])
    def test_kill_run_task(self, requested, task_manager_servicer):
        assert task_manager_servicer.kill_task(requested, '') == task_manager_pb2.TaskStatus(task_id=requested.task_id,
                                                                                             status=task_manager_pb2.
                                                                                             TaskStatus.Status.KILLED)

    @pytest.mark.parametrize('requested', [MockRequest(task_id.status['NOTFOUND'])])
    def test_get_not_found_task_status(self, requested, task_manager_servicer):
        assert task_manager_servicer.get_task_status(requested, '') == task_manager_pb2.TaskStatus(
            task_id=requested.task_id,
            status=task_manager_pb2.
            TaskStatus.Status.NOTFOUND)

    @pytest.mark.parametrize('requested', [MockRequest(task_id.status['RUNNING'])])
    def test_get_running_task_status(self, requested, task_manager_servicer):
        assert task_manager_servicer.get_task_status(requested, '') == task_manager_pb2.TaskStatus(
            task_id=requested.task_id,
            status=task_manager_pb2.
            TaskStatus.Status.RUNNING)

    @pytest.mark.parametrize('requested', [MockRequest(task_id.status['DONE'])])
    def test_get_done_task_status(self, requested, task_manager_servicer):
        assert task_manager_servicer.get_task_status(requested, '') == task_manager_pb2.TaskStatus(
            task_id=requested.task_id,
            status=task_manager_pb2.
            TaskStatus.Status.DONE)

    @pytest.mark.parametrize('requested', [MockRequest(task_id.status['KILLED'])])
    def test_get_killed_task_status(self, requested, task_manager_servicer):
        assert task_manager_servicer.get_task_status(requested, '') == task_manager_pb2.TaskStatus(
            task_id=requested.task_id,
            status=task_manager_pb2.
            TaskStatus.Status.KILLED)

    def test_get_all_tasks(self, task_manager_servicer):
        task_id = mock_task_id()
        expect_all_tasks_status = task_manager_pb2.AllTasksStatus()
        expect_all_tasks_status.task_status_array.append(task_manager_pb2.TaskStatus(task_id=task_id.status['RUNNING'],
                                                                                     status=task_manager_pb2.TaskStatus.Status.RUNNING))
        expect_all_tasks_status.task_status_array.append(
            task_manager_pb2.TaskStatus(task_id=task_id.status['DONE'], status=task_manager_pb2.TaskStatus.Status.DONE))
        expect_all_tasks_status.task_status_array.append(
            task_manager_pb2.TaskStatus(task_id=task_id.status['KILLED'], status=task_manager_pb2.TaskStatus.Status.KILLED))
        assert task_manager_servicer.get_all_tasks(None, '') == expect_all_tasks_status

    @pytest.mark.parametrize('request_task_id', task_id.status['RUNNING'])
    def test_wrap_by_grpc_task_status_running_task(self, request_task_id, task_manager_servicer):
        assert task_manager_servicer._wrap_by_grpc_TaskStatus(request_task_id) == task_manager_pb2.TaskStatus(
            task_id=request_task_id, status=task_manager_pb2.TaskStatus.Status.RUNNING)

    @pytest.mark.parametrize('request_task_id', task_id.status['DONE'])
    def test_wrap_by_grpc_task_status_done_task(self, request_task_id, task_manager_servicer):
        assert task_manager_servicer._wrap_by_grpc_TaskStatus(request_task_id) == task_manager_pb2.TaskStatus(
            task_id=request_task_id, status=task_manager_pb2.TaskStatus.Status.DONE)

    @pytest.mark.parametrize('request_task_id', task_id.status['KILLED'])
    def test_wrap_by_grpc_task_status_killed_task(self, request_task_id, task_manager_servicer):
        assert task_manager_servicer._wrap_by_grpc_TaskStatus(request_task_id) == task_manager_pb2.TaskStatus(
            task_id=request_task_id, status=task_manager_pb2.TaskStatus.Status.KILLED)

    @pytest.mark.parametrize('request_task_id', task_id.status['RUNNING'])
    def test_get_task_running_task(self, request_task_id, task_manager_servicer):
        assert task_manager_servicer._get_task(request_task_id) == task_manager_servicer.tasks[request_task_id]

    @pytest.mark.parametrize('request_task_id', task_id.status['DONE'])
    def test_get_task_done_task(self, request_task_id, task_manager_servicer):
        assert task_manager_servicer._get_task(request_task_id) == task_manager_servicer.tasks[request_task_id]

    @pytest.mark.parametrize('request_task_id', task_id.status['KILLED'])
    def test_get_task_killed_task(self, request_task_id, task_manager_servicer):
        assert task_manager_servicer._get_task(request_task_id) == task_manager_servicer.tasks[request_task_id]

class TestHealthCheck:
    def test_health_check(self, task_manager_service):
        assert task_manager_service.health_check(None, None) == ServerStatus(alive=True)

class TestRunTsak:
    @staticmethod
    def make_run_task_request(gpuidx=0, command="pwd", name="test", task_env=os.environ.copy()):
        """make request of run_task with proper default value"""
        return TaskStatement(
            gpuidx=gpuidx,
            command=command,
            name=name,
            task_env=task_env
        )

    def test_run_task_with_proper_arg(self, task_manager_service):
        request = self.make_run_task_request(gpuidx=0, command="echo a")
        ret = task_manager_service.run_task(request, None)
        log_path = osp.join(task_manager_service.log_dir, f"{ret.task_id}_log.txt")

        assert osp.exists(log_path)
        assert ret.task_id in task_manager_service.tasks

    def test_run_task_with_negative_gpu_idx(self, task_manager_service):
        request = self.make_run_task_request(gpuidx=-1)
        with pytest.raises(ValueError):
            task_manager_service.run_task(request, None)

    def test_run_task_with_empty_command(self, task_manager_service):
        request = self.make_run_task_request(
            command="",
            name="test",
            task_env=os.environ.copy()
        )
        with pytest.raises(ValueError):
            task_manager_service.run_task(request, None)

    def test_run_task_with_wrong_task_statement_type(self, task_manager_service, mocker):
        task_statement = mocker.Mock()
        task_statement.gpuidx = 0
        task_statement.command = "pwd"
        task_statement.name = "test"
        task_statement.task_env = ""

        with pytest.raises(TypeError):
            task_manager_service.run_task(
                task_statement,
                None
            )
