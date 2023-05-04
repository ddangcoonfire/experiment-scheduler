"""
Unit Test Code for Master
"""

import pytest
from experiment_scheduler.master.master import Master
from experiment_scheduler.master.grpc_master.master_pb2 import (
    TaskStatus,
    TaskLogFile,
    ExperimentsStatus,
    AllExperimentsStatus,
    AllTasksStatus,
    MasterResponse,
)
from experiment_scheduler.task_manager.grpc_task_manager.task_manager_pb2 import (
    TaskStatus as TMTaskStatus,
)


class MockRequest:
    """
    Mock Simple Request (used commonly)
    """

    def __init__(self, task_id):
        self.task_id = task_id


class MockEditRequest:
    """
    Mock class for edit_task
    """

    def __init__(self, task_id, cmd, task_env):
        self.task_id = task_id
        self.cmd = cmd
        self.task_env = task_env


class MockExperimentRequest:
    """
    Mock class for ExperimentRequest (protobuf format)
    """

    def __init__(self, experiment_id):
        self.experiment_id = experiment_id


class MockExperimentTasks:
    """
    Mock class for ORM ExperimentTasks
    """

    def __init__(self):
        self.id = "TestID"  # pylint:disable=invalid-name
        self.tasks = [
            MockTask("1", TaskStatus.Status.RUNNING),
            MockTask("2", TaskStatus.Status.RUNNING),
        ]


class MockRequestExperiments:
    """
    Mock class for request_experiments
    """

    def __init__(self, name, tasks):
        self.name = name
        self.tasks = tasks


class MockExperiment:
    """
    Mock class for ORM Experiment
    """

    def get(self):
        """
        ORM get Method
        :return:
        """
        return MockExperimentTasks()

    def list(self):
        """
        ORM list method
        :return:
        """
        return [MockExperimentTasks(), MockExperimentTasks()]


class MockTask:
    """
    Mock class for Task object
    """

    def __init__(  # pylint:disable=too-many-arguments
        self,
        task_id="task_id",
        status=None,
        name="test",
        task_manager_id="task_manager",
        task_env=None,
        command="python test.py",
    ):
        if task_env is None:
            task_env = {"test_key": "test_val"}
        self.id = task_id  # pylint:disable=invalid-name
        self.name = name
        self.status = status
        self.task_manager_id = task_manager_id
        self.task_env = task_env
        self.command = command

    def list_success(self):
        """
        list mock for success case
        :return:
        """
        return [
            MockTask("test_task_id", TaskStatus.Status.RUNNING),
            MockTask("2", TaskStatus.Status.RUNNING),
            MockTask("3", TaskStatus.Status.RUNNING),
        ]

    def list_fail(self):
        """
        list mock for failed case
        :return:
        """
        return [
            MockTask("1", TaskStatus.Status.RUNNING),
            MockTask("2", TaskStatus.Status.RUNNING),
            MockTask("3", TaskStatus.Status.RUNNING),
        ]

    def commit(self):
        """
        commit should not do anything while test.
        :return:
        """
        return None


class MockTaskManager:
    """
    Mock class for ORM TaskManager
    """

    def __init__(self, address, path=""):
        self.address = address
        self.log_file_path = path
        self.id = "testID"  # pylint:disable=invalid-name


class MockProcessMonitor:
    """
    Mock class for Process Monitor Class
    """

    def kill_task(self):
        """
        Mock mehtod for kill_task
        :return:
        """
        return TaskStatus(task_id="test_task_id", status=TaskStatus.Status.KILLED)

    def get_task_log(self):
        """
        Mock method for get_task_log
        :return:
        """
        return "task completed"

    def run_task_success(self):
        """
        Mock method for run_task in success case
        :return:
        """
        return TMTaskStatus(task_id="test1", status=TaskStatus.Status.RUNNING)

    def run_task_failed(self):
        """
        Mock method for run_task in failure case
        :return:
        """
        return TMTaskStatus(task_id="test1", status=TaskStatus.Status.NOTSTART)


class MockThread:
    """
    Make Thread not work during test
    """

    @classmethod
    def start(cls):
        """
        Thread's Start should do nothing
        :return:
        """
        return


class TestMaster:
    """
    Master Test class
    """

    @pytest.fixture
    def master(self, mocker):
        """
        Fixture for Master class
        :param mocker:
        :return:
        """
        # mocker.patch("threading.Thread", return_value=MockThread)
        mocker.patch(
            "experiment_scheduler.master.process_monitor.ProcessMonitor._health_check",
            return_value=None,
        )
        mocker.patch(
            "experiment_scheduler.master.master.Master._execute_command",
            return_value=None,
        )
        master = Master()
        return master

    def test_get_task_managers(self, master, mocker):
        """
        Test for get_task_managers
        :param master:
        :param mocker:
        :return:
        """
        mocker.patch("ast.literal_eval", return_value=["test_address"])
        task_managers = master.get_task_managers()
        assert task_managers == ["test_address"]
        mocker.patch("os.getenv", return_value="test_address2")
        task_managers = master.get_task_managers()
        assert task_managers == ["test_address2"]

    def test_select_task_manager(self, master, mocker):
        """
        Test for select_task_manager
        :param master:
        :param mocker:
        :return:
        """
        mocker.patch("os.getenv", return_value="test_address1 test_address2")
        master = Master()
        selected_task_manager = master.select_task_manager()
        assert selected_task_manager == "test_address1"

        selected_task_manager = master.select_task_manager(1)
        assert selected_task_manager == "test_address2"

    def test_request_experiments(self, master):
        """
        Test for request_experiments
        :param master:
        :return:
        """
        master = Master()
        request = MockRequestExperiments(
            name="test_experiment",
            tasks=[MockTask(name="test_task", command="test_command")],
        )
        context = ""
        response = master.request_experiments(request, context)
        assert response.experiment_id.startswith("test_experiment-")
        assert response.response == MasterResponse.ResponseStatus.SUCCESS

    def test_get_task_log(self, master, mocker):
        """
        Test for get_task_log
        :param master:
        :param mocker:
        :return:
        """
        mocker.patch(
            "experiment_scheduler.db_util.task.Task.get",
            return_value=MockTask(
                task_id="test_task_id", status=TaskStatus.Status.RUNNING
            ),
        )
        mocker.patch(
            "experiment_scheduler.db_util.task_manager.TaskManager.get",
            return_value=MockTaskManager(address="test_address"),
        )
        master = Master()
        request = MockRequest(task_id="test_task_id")
        context = ""
        response = master.get_task_log(request, context)
        assert next(response) == TaskLogFile(
            error_message=bytes("Check task id", "utf-8")
        )

        mocker.patch(
            "experiment_scheduler.db_util.task_manager.TaskManager.get",
            return_value=MockTaskManager(address="test_address", path="not empty"),
        )
        mocker.patch(
            "experiment_scheduler.master.process_monitor.ProcessMonitor.get_task_log",
            return_value=MockProcessMonitor().get_task_log(),
        )
        response = master.get_task_log(request, context)
        assert "".join(response) == "task completed"

    def test_get_task_status(self, master, mocker):
        """
        test for get_task_status
        :param master:
        :param mocker:
        :return:
        """
        mocker.patch("experiment_scheduler.db_util.task.Task.get", return_value=None)
        request = MockRequest(task_id="test_task_id")
        context = ""
        response = master.get_task_status(request, context)
        assert response.task_id == "test_task_id"
        assert response.status == TaskStatus.Status.NOTFOUND

        mocker.patch(
            "experiment_scheduler.db_util.task.Task.get",
            return_value=MockTask(
                task_id="test_task_id", status=TaskStatus.Status.RUNNING
            ),
        )
        response = master.get_task_status(request, context)
        assert response.task_id == "test_task_id"
        assert response.status == TaskStatus.Status.RUNNING

    def test_kill_task(self, master, mocker):
        """
        test for kill_task
        :param master:
        :param mocker:
        :return:
        """
        mocker.patch("experiment_scheduler.db_util.task.Task.get", return_value=None)
        request = MockRequest(task_id="test_task_id")
        context = ""
        response = master.kill_task(request, context)
        assert response == TaskStatus(
            task_id="test_task_id", status=TaskStatus.Status.NOTFOUND
        )

        mocker.patch(
            "experiment_scheduler.db_util.task.Task.get",
            return_value=MockTask(
                task_id="test_task_id", status=TaskStatus.Status.NOTSTART
            ),
        )
        response = master.kill_task(request, context)
        assert response == TaskStatus(
            task_id="test_task_id", status=TaskStatus.Status.KILLED
        )

        mocker.patch(
            "experiment_scheduler.db_util.task.Task.get",
            return_value=MockTask(
                task_id="test_task_id",
                status=TaskStatus.Status.RUNNING,
                task_manager_id=None,
            ),
        )
        response = master.kill_task(request, context)
        assert response == TaskStatus(
            task_id="test_task_id", status=TaskStatus.Status.KILLED
        )

        mocker.patch(
            "experiment_scheduler.db_util.task.Task.get",
            return_value=MockTask(
                task_id="test_task_id", status=TaskStatus.Status.RUNNING
            ),
        )
        mocker.patch(
            "experiment_scheduler.db_util.task_manager.TaskManager.get",
            return_value=MockTaskManager(address="test_address"),
        )
        mocker.patch(
            "experiment_scheduler.master.process_monitor.ProcessMonitor.kill_task",
            return_value=MockProcessMonitor().kill_task(),
        )
        response = master.kill_task(request, context)
        assert response == TaskStatus(
            task_id="test_task_id", status=TaskStatus.Status.KILLED
        )

        mocker.patch(
            "experiment_scheduler.db_util.task.Task.get",
            return_value=MockTask(
                task_id="test_task_id", status=TaskStatus.Status.DONE
            ),
        )
        response = master.kill_task(request, context)
        assert response == TaskStatus(
            task_id="test_task_id", status=TaskStatus.Status.DONE
        )

    def test_get_all_tasks(self, master, mocker):
        """
        Test for get_all_tasks
        :param master:
        :param mocker:
        :return:
        """
        mocker.patch(
            "experiment_scheduler.db_util.experiment.Experiment.get",
            return_value=MockExperiment().get(),
        )
        master = Master()
        request = MockExperimentRequest(experiment_id="test_experiment_id")
        context = ""
        response = master.get_all_tasks(request, context)
        assert response == AllExperimentsStatus(
            experiment_status_array=[
                ExperimentsStatus(
                    experiment_id="test_experiment_id",
                    task_status_array=AllTasksStatus(
                        task_status_array=[
                            TaskStatus(task_id="1", status=TaskStatus.Status.RUNNING),
                            TaskStatus(task_id="2", status=TaskStatus.Status.RUNNING),
                        ]
                    ),
                )
            ]
        )

        mocker.patch(
            "experiment_scheduler.db_util.experiment.Experiment.list",
            return_value=MockExperiment().list(),
        )
        request = MockExperimentRequest(experiment_id=None)
        response = master.get_all_tasks(request, context)

        assert response == AllExperimentsStatus(
            experiment_status_array=[
                ExperimentsStatus(
                    experiment_id="TestID",
                    task_status_array=AllTasksStatus(
                        task_status_array=[
                            TaskStatus(task_id="1", status=TaskStatus.Status.RUNNING),
                            TaskStatus(task_id="2", status=TaskStatus.Status.RUNNING),
                        ]
                    ),
                ),
                ExperimentsStatus(
                    experiment_id="TestID",
                    task_status_array=AllTasksStatus(
                        task_status_array=[
                            TaskStatus(task_id="1", status=TaskStatus.Status.RUNNING),
                            TaskStatus(task_id="2", status=TaskStatus.Status.RUNNING),
                        ]
                    ),
                ),
            ]
        )

    def test_execute_task(self, master, mocker):
        """
        test for execute_task
        :param master:
        :param mocker:
        :return:
        """
        mocker.patch(
            "experiment_scheduler.db_util.task.Task.get",
            return_value=MockTask(
                task_id="test_task_id", status=TaskStatus.Status.RUNNING
            ),
        )
        mocker.patch(
            "experiment_scheduler.db_util.task_manager.TaskManager.get",
            return_value=MockTaskManager(address="test_task_manager_address"),
        )
        mocker.patch(
            "experiment_scheduler.master.process_monitor.ProcessMonitor.run_task",
            return_value=MockProcessMonitor().run_task_success(),
        )

        master = Master()
        task_manager_address = "test_task_manager_address"
        task_id = "test_task_id"
        response = master.execute_task(task_manager_address, task_id)
        assert response.status == TaskStatus.Status.RUNNING

        mocker.patch(
            "experiment_scheduler.master.process_monitor.ProcessMonitor.run_task",
            return_value=MockProcessMonitor().run_task_failed(),
        )
        response = master.execute_task(task_manager_address, task_id)
        assert response.status == TaskStatus.Status.NOTSTART

    def test_edit_task(self, master, mocker):
        """
        Test for edit_task
        :param master:
        :param mocker:
        :return:
        """
        mocker.patch(
            "experiment_scheduler.db_util.task.Task.list",
            return_value=MockTask("1", TaskStatus.Status.RUNNING).list_success(),
        )
        mocker.patch(
            "experiment_scheduler.db_util.task.Task.get",
            return_value=MockTask("1", TaskStatus.Status.RUNNING),
        )
        master = Master()
        request = MockEditRequest(
            task_id="test_task_id", cmd="test_cmd", task_env={"key": "val"}
        )
        context = ""
        response = master.edit_task(request, context)
        assert response.experiment_id == "0"
        assert response.response == MasterResponse.ResponseStatus.SUCCESS

        mocker.patch(
            "experiment_scheduler.db_util.task.Task.list",
            return_value=MockTask("1", TaskStatus.Status.RUNNING).list_fail(),
        )
        response = master.edit_task(request, context)
        assert response.experiment_id == "0"
        assert response.response == MasterResponse.ResponseStatus.FAIL
