import signal
from enum import Enum

import pytest
from experiment_scheduler.task_manager import task_manager_server
from experiment_scheduler.task_manager.grpc_task_manager import task_manager_pb2, task_manager_pb2_grpc


class MockRunTask:
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


class MockDoneTask:
    def __init__(self, task_id):
        self.task_id = task_id

    @staticmethod
    def poll():
        return 0

    @staticmethod
    def terminate():
        return None

    @staticmethod
    def wait():
        return None


class MockKilledTask:
    def __init__(self, task_id):
        self.task_id = task_id

    @staticmethod
    def poll():
        return -signal.SIGTERM

    @staticmethod
    def terminate():
        return None

    @staticmethod
    def wait():
        return None


class MockRequset:
    def __init__(self, task_id):
        self.task_id = task_id

class TestClass:
    TaskID = Enum('task_id', {'RUNNING': '1', 'DONE': '2', 'KILLED': '3', 'NOTFOUND': '4'})

    @pytest.fixture
    def task_manager_servicer(self):
        task_manager_servicer = task_manager_server.TaskManagerServicer(task_manager_pb2_grpc.TaskManagerServicer)
        task_id = Enum('task_id', {'RUNNING': '1', 'DONE': '2', 'KILLED': '3', 'NOTFOUND': '4'})
        task_manager_servicer.tasks[task_id.RUNNING.value] = MockRunTask(task_id.RUNNING.value)
        task_manager_servicer.tasks[task_id.DONE.value] = MockDoneTask(task_id.DONE.value)
        task_manager_servicer.tasks[task_id.KILLED.value] = MockKilledTask(task_id.KILLED.value)
        return task_manager_servicer

    @pytest.mark.parametrize('requested', [MockRequset(TaskID.NOTFOUND.value)])
    def test_kill_not_found_task(self, requested, task_manager_servicer):
        assert task_manager_servicer.kill_task(requested, any) == task_manager_pb2.TaskStatus(task_id=requested.task_id,
                                                                                              status=task_manager_pb2.
                                                                                              TaskStatus.Status.NOTFOUND)

    @pytest.mark.parametrize('requested', [MockRequset(TaskID.DONE.value)])
    def test_kill_done_task(self, requested, task_manager_servicer):
        assert task_manager_servicer.kill_task(requested, any) == task_manager_pb2.TaskStatus(task_id=requested.task_id,
                                                                                              status=task_manager_pb2.
                                                                                              TaskStatus.Status.DONE)

    @pytest.mark.parametrize('requested', [MockRequset(TaskID.RUNNING.value)])
    def test_kill_run_task(self, requested, task_manager_servicer):
        assert task_manager_servicer.kill_task(requested, any) == task_manager_pb2.TaskStatus(task_id=requested.task_id,
                                                                                              status=task_manager_pb2.
                                                                                              TaskStatus.Status.KILLED)

    @pytest.mark.parametrize('requested', [MockRequset(TaskID.NOTFOUND.value)])
    def test_get_not_found_task_status(self, requested, task_manager_servicer):
        assert task_manager_servicer.get_task_status(requested, any) == task_manager_pb2.TaskStatus(
            task_id=requested.task_id,
            status=task_manager_pb2.
            TaskStatus.Status.NOTFOUND)

    @pytest.mark.parametrize('requested', [MockRequset(TaskID.RUNNING.value)])
    def test_get_running_task_status(self, requested, task_manager_servicer):
        assert task_manager_servicer.get_task_status(requested, any) == task_manager_pb2.TaskStatus(
            task_id=requested.task_id,
            status=task_manager_pb2.
            TaskStatus.Status.RUNNING)

    @pytest.mark.parametrize('requested', [MockRequset(TaskID.DONE.value)])
    def test_get_done_task_status(self, requested, task_manager_servicer):
        assert task_manager_servicer.get_task_status(requested, any) == task_manager_pb2.TaskStatus(
            task_id=requested.task_id,
            status=task_manager_pb2.
            TaskStatus.Status.DONE)

    @pytest.mark.parametrize('requested', [MockRequset(TaskID.KILLED.value)])
    def test_get_killed_task_status(self, requested, task_manager_servicer):
        assert task_manager_servicer.get_task_status(requested, any) == task_manager_pb2.TaskStatus(
            task_id=requested.task_id,
            status=task_manager_pb2.
            TaskStatus.Status.KILLED)
