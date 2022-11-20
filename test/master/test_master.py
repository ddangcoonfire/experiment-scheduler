from unittest import TestCase
from unittest.mock import Mock, patch
import uuid
from collections import OrderedDict
from experiment_scheduler.master.master import Master
import experiment_scheduler


def mockGetTaskManagers():
    return ["test_network"]


class MockPipe:
    def __init__(self, *args, **kwargs):
        pass

    def send(self, *args, **kwargs):
        pass

    def poll(self, *args, **kwargs):
        pass

    def recv(self, *args, **kwargs):
        pass


def mockPipe():
    return (MockPipe(), MockPipe())

class Task:

    def __init__(self, name):
        self.name = name


class TestRequest:

    def __init__(self, *args, **kwargs):
        self.name = "test_name"
        self.tasks = [Task("task_name")]


class MockResourceMonitor:
    def __init__(self, *args, **kwargs):
        self.resource_monitor_address = "address"

    def get_available_gpu_idx(*args, **kwargs):
        return 1, 1

    # def get_max_free_gpu(*args, **kwargs):
    #     return 1


class MockProcess:
    def __init__(self, *args, **kwargs):
        pass

    def start(self):
        pass


class MockProcessMonitor:
    def __init__(self, *args, **kwargs):
        pass

    def start(self):
        pass


class MockThread:
    def __init__(self, *args, **kwargs):
        pass

    def start(self):
        pass


class MockTask:
    name = "test"
    command = "task"
    task_env = {"test": "env"}

    def __init__(self, *args, **kwargs):
        pass


class TestMaster(TestCase):
    @patch.object(
        experiment_scheduler.master.master, "ProcessMonitor", MockProcessMonitor
    )
    @patch.object(
        experiment_scheduler.master.master, "get_task_managers", mockGetTaskManagers
    )
    @patch("threading.Thread", MockThread)
    def setUp(self):
        Master.get_task_managers = Mock(return_value=mockGetTaskManagers())
        self.master = Master()
        self.master.queued_tasks = OrderedDict([("test_task_id", MockTask())])

    def tearDown(self):
        patch.stopall()

    @patch("time.sleep", side_effect=Exception)
    @patch.object(
        experiment_scheduler.resource_monitor.resource_monitor_listener, "ResourceMonitorListener",
        MockResourceMonitor
    )
    def test__execute_command(self, mock_time_sleep):
        # given
        self.master.execute_task = Mock()
        self.master._get_available_task_managers = Mock(
            return_value=([("test_network", 1)])
        )

        # when
        self.assertRaises(Exception, lambda: self.master._execute_command())

        # then
        self.master.execute_task.assert_called_with("test_network", 1)

    @patch.object(
        experiment_scheduler.resource_monitor.resource_monitor_listener, "ResourceMonitorListener",
        MockResourceMonitor
    )
    def test_get_available_task_managers(self):
        # given
        self.master._check_task_manager_run_task_available = Mock(
            return_value=(1, 1)
        )

        # when
        test_return_value = self.master._get_available_task_managers()

        # then
        self.assertEqual(test_return_value, [("test_network", 1)])

    def test_select_task_manager(self):
        # when
        test_return_value = self.master.select_task_manager()

        # then
        self.assertEqual(test_return_value, "test_network")

    @patch.object(uuid, "uuid1", (lambda: 123))
    def test_request_experiments(self):
        # given
        test_request = TestRequest()

        # when
        test_return_value = self.master.request_experiments(test_request, "context")

        # then
        self.assertEqual(test_return_value.experiment_id, "test_name-123")
        self.assertEqual(test_return_value.response, 0)


    def test_get_task_managers(self):
        # when
        test_return_value = self.master.get_task_managers()

        # then
        self.assertEqual(test_return_value, ["test_network"])

    def test_delete_experiment(self):
        pass

    def test_delete_experiments(self):
        pass

    def test_check_task_manager_run_task_available(self):
        # when
        test_return_value = self.master.check_task_manager_run_task_available(
            "test_network"
        )

        # then
        self.assertEqual(test_return_value, True)

    @patch.object(experiment_scheduler.master.master, "Pipe", mockPipe)
    def test_execute_task(self):
        # when
        self.master.execute_task(task_manager="test_network", gpu_idx=1)

        # then
        self.assertIsInstance(self.master.master_pipes["test_network"], MockPipe)
