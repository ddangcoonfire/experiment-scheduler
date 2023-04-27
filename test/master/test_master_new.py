import pytest
from experiment_scheduler.master.master import Master
from experiment_scheduler.master.grpc_master.master_pb2 import TaskStatus


class MockRequest:
    def __init__(self, task_id):
        self.task_id = task_id


class MockThread:
    @classmethod
    def start(cls):
        return


class TestMaster:
    @pytest.fixture
    def master(self, mocker):
        mocker.patch("threading.Thread", return_value=MockThread)
        master = Master()
        return master

    def test_get_task_managers(self, master, mocker):
        mocker.patch("ast.literal_eval", return_value=["test_address"])
        task_managers = master.get_task_managers()
        assert task_managers == ["test_address"]
        mocker.patch("os.getenv", return_value="test_address2")
        task_managers = master.get_task_managers()
        assert task_managers == ["test_address2"]

    #
    # def test_select_task_manager():
    #     master = Master()
    #     selected_task_manager = master.select_task_manager()
    #     assert selected_task_manager == master.task_managers_address[0]
    #
    #     selected_task_manager = master.select_task_manager(1)
    #     assert selected_task_manager == master.task_managers_address[1]
    #
    #
    # def test_request_experiments():
    #     master = Master()
    #     request = MockRequest(name="test_experiment", tasks=[MockTask(name="test_task", command="test_command")])
    #     context = MockContext()
    #     response = master.request_experiments(request, context)
    #     assert response.experiment_id.startswith("test_experiment-")
    #     assert response.response == MasterResponse.ResponseStatus.SUCCESS
    #
    #
    # def test_get_task_log():
    #     master = Master()
    #     request = MockRequest(task_id="test_task_id")
    #     context = MockContext()
    #     response = master.get_task_log(request, context)
    #     assert isinstance(response, TaskLogFile)
    #
    #
    # def test_get_task_status():
    #     master = Master()
    #     request = MockRequest(task_id="test_task_id")
    #     context = MockContext()
    #     response = master.get_task_status(request, context)
    #     assert response.task_id == "test_task_id"
    #     assert response.status == TaskStatus.Status.NOTFOUND
    #
    #
    def test_kill_task(self, master, mocker):
        mocker.patch("experiment_scheduler.db_util.task.Task.get", return_value=None)
        request = MockRequest(task_id="test_task_id")
        context = ""
        response = master.kill_task(request, context)
        assert response == TaskStatus(
            task_id="test_task_id", status=TaskStatus.Status.NOTFOUND
        )

    #
    #
    # def test_get_all_tasks():
    #     master = Master()
    #     request = MockRequest(experiment_id="test_experiment_id")
    #     context = MockContext()
    #     response = master.get_all_tasks(request, context)
    #     assert isinstance(response, AllExperimentsStatus)
    #
    #
    # def test_execute_task():
    #     master = Master()
    #     task_manager_address = "test_task_manager_address"
    #     task_id = "test_task_id"
    #     response = master.execute_task(task_manager_address, task_id)
    #     assert response.status == TaskStatus.Status.RUNNING
    #
    #
    # def test_edit_task():
    #     master = Master()
    #     request = MockRequest(task_id="test_task_id", cmd="test_cmd", task_env={"key": "val"})
    #     context = MockContext()
    #     response = master.edit_task(request, context)
    #     assert response.experiment_id == "0"
    #     assert response.response == MasterResponse.ResponseStatus.SUCCESS
