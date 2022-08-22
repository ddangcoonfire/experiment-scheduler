from unittest import TestCase
from unittest.mock import Mock, patch
import uuid
from experiment_scheduler.master.master import Master
import experiment_scheduler



def mockGetTaskManagers():
    return ["test_network"]

class MockPipe():
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

class TestRequest():
    name = "test_name"
    tasks = "test_tasks"
    def __init__(self, *args, **kwargs):
        pass


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
    task_env = {"test":"env"}
    def __init__(self, *args, **kwargs):
        pass

class TestMaster(TestCase):

    @patch.object(experiment_scheduler.master.master, "ProcessMonitor", MockProcessMonitor)
    @patch.object(experiment_scheduler.master.master, "Process", MockProcess)
    @patch.object(experiment_scheduler.master.master, "Pipe", mockPipe)
    @patch("threading.Thread", MockThread)
    def setUp(self):
        Master.get_task_managers = Mock(return_value=mockGetTaskManagers())
        self.master = Master()
        self.master.queued_tasks = [MockTask()]

    def tearDown(self):
        patch.stopall()

    @patch("time.sleep", side_effect=Exception)
    def test__execute_command(self, mock_time_sleep):
        # given
        # MockPipe = Mock()
        # MockPipe.__setattr__('poll', True)
        # self.master.master_pipes = {'test_network': MockPipe}
        self.master.execute_task = Mock()

        # when
        self.assertRaises(Exception, lambda : self.master._execute_command())

        # then
        self.master.execute_task.assert_called_with('test_network')
        self.assertIsInstance(self.master.master_pipes['test_network'], MockPipe)


    @patch.object(experiment_scheduler.master.master, "ProcessMonitor", MockProcessMonitor)
    def test__run_process_monitor(self):
        # given
        MockProcessMonitor.start = Mock()

        # when
        self.master._run_process_monitor("test_tm_address", MockPipe())

        # then
        MockProcessMonitor.start.assert_called_once()

    def test__process_monitor_termintion(self):
        pass

    @patch.object(experiment_scheduler.master.master, "Process", MockProcess)
    @patch.object(experiment_scheduler.master.master, "Pipe", mockPipe)
    def test_create_process_monitor(self):
        # given
        self.master._run_process_monitor = Mock()

        # # when
        test_return_value = self.master.create_process_monitor()

        # then
        self.assertIsInstance(test_return_value, list)

    def test_get_task_managers(self):
        # when
        test_return_value = self.master.get_task_managers()

        # then
        self.assertEqual(test_return_value, ['test_network'])


    def test_select_task_manager(self):
        # when
        test_return_value = self.master.select_task_manager()

        # then
        self.assertEqual(test_return_value, 'test_network')


    @patch.object(uuid, "uuid1", (lambda : 123))
    def test_request_experiments(self):
        # given
        test_request = TestRequest()

        # when
        test_return_value = self.master.request_experiments(test_request, "context")

        # then
        self.assertEqual(test_return_value.experiment_id, "test_name-123")
        self.assertEqual(test_return_value.response, 0)


    def test_delete_experiment(self):
        pass

    def test_delete_experiments(self):
        pass

    def test_check_task_manager_run_task_available(self):
        # when
        test_return_value = self.master.check_task_manager_run_task_available("test_network")

        # then
        self.assertEqual(test_return_value, True)

    def test_get_available_task_managers(self):
        # when
        test_return_value = self.master.get_available_task_managers()

        # then
        self.assertEqual(test_return_value, ['test_network'])


    @patch.object(experiment_scheduler.master.master, "Pipe", mockPipe)
    def test_execute_task(self):
        # when
        self.master.execute_task(task_manager='test_network')

        # then
        self.assertIsInstance(self.master.master_pipes['test_network'], MockPipe)