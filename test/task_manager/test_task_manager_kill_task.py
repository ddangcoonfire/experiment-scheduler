import pytest
from ddangko.experiment_scheduler.experiment-scheduler.task_manager import task_manager_server
from experiment_scheduler.task_manager.grpc_task_manager import task_manager_pb2

@pytest.mark.parametrize("request", [{"task_id" : 1}])


class TestClass:

    @pytest.fixture
    def task_manager_servicer(self):
        task_manager_servicer = task_manager_server.TaskManagerServicer()
        return task_manager_servicer

    @pytest.mark.parametrize("TaskStatus", [{"task_id": 1, "status": 0}])
    def test_kill_running_task(self, request):
        assert task_manager_servicer.kill_task(request) == task_manager_pb2.TaskStatus(
                task_id= request.task_id,
                status= task_manager_pb2.TaskStatus.Status.KILLED
            )

    @pytest.mark.parametrize("TaskStatus", [{"task_id": 1, "status": 1}])
    def test_kill_done_task(self, request):
        assert task_manager_servicer.kill_task(request) == task_manager_pb2.TaskStatus(
            task_id=request.task_id,
            status=task_manager_pb2.TaskStatus.Status.DONE
        )

    @pytest.mark.parametrize("TaskStatus", [{"task_id": 1, "status": 4}])
    def test_kill_not_found_task(self, request):
        assert task_manager_servicer.kill_task(request) == task_manager_pb2.TaskStatus(
            task_id=request.task_id,
            status=task_manager_pb2.TaskStatus.Status.NOTFOUND
        )