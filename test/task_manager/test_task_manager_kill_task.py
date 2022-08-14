from unittest.mock import MagicMock

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


class MockRequset:
    def __init__(self, task_id):
        self.task_id = task_id


class TestClass:
    @pytest.fixture
    def task_manager_servicer(self):
        task_manager_servicer = task_manager_server.TaskManagerServicer(task_manager_pb2_grpc.TaskManagerServicer)
        return task_manager_servicer

    @pytest.mark.parametrize('requested', [MockRequset('1')])
    def test_kill_not_found_task(self, requested, task_manager_servicer):
        assert task_manager_servicer.kill_task(requested, any) == task_manager_pb2.TaskStatus(task_id=requested.task_id,
                                                                                              status=task_manager_pb2.
                                                                                              TaskStatus.Status.NOTFOUND)

    @pytest.mark.parametrize('requested', [MockRequset('1')])
    def test_kill_done_task(self, requested, task_manager_servicer):
        task_manager_servicer.tasks[requested.task_id] = MockDoneTask(1)
        assert task_manager_servicer.kill_task(requested, any) == task_manager_pb2.TaskStatus(task_id=requested.task_id,
                                                                                              status=task_manager_pb2.
                                                                                              TaskStatus.Status.DONE)
    @pytest.mark.parametrize('requested', [MockRequset('1')])
    def test_kill_run_task(self, requested, task_manager_servicer):
        task_manager_servicer.tasks[requested.task_id] = MockRunTask(1)
        assert task_manager_servicer.kill_task(requested, any) == task_manager_pb2.TaskStatus(task_id=requested.task_id,
                                                                                              status=task_manager_pb2.
                                                                                              TaskStatus.Status.KILLED)


