import os
from os import path as osp

import pytest
from experiment_scheduler.task_manager.grpc_task_manager import \
    task_manager_pb2
from experiment_scheduler.task_manager.task_manager_server import \
    TaskManagerServicer

from experiment_scheduler.task_manager.grpc_task_manager.task_manager_pb2 import (
    ServerStatus,
    TaskStatement,
    TaskStatus,
    Task,
    AllTasksStatus,
    TaskLog
)


@pytest.fixture
def task_manager_service(tmp_path):
    return TaskManagerServicer(tmp_path)

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

    def test_run_task_with_wrong_task_statement_type(self, task_manager_service):
        with pytest.raises(TypeError):
            task_manager_service.run_task(
                dict(gpuidx=0, command="pwd", name="test", task_env=""),
                None
            )
