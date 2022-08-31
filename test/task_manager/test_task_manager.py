import signal
from enum import Enum

import pytest
from experiment_scheduler.task_manager import task_manager_server
from experiment_scheduler.task_manager.grpc_task_manager import task_manager_pb2, task_manager_pb2_grpc


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
