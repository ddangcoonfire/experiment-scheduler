from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch
import threading
from multiprocessing import Process, Pipe

from experiment_scheduler.master.master import Master
from experiment_scheduler.master.process_monitor import ProcessMonitor



# @patch('multiprocessing.Process.__init__', new=lambda x: None)
# @patch('multiprocessing.Process.start', new=lambda x: None)
# @patch('multiprocessing.Pipe.__init__')
# @patch('multiprocessing.Pipe.poll', new=lambda x: None)
# @patch('multiprocessing.Pipe.recv', new=lambda x: None)
# @patch('multiprocessing.Pipe.send', new=lambda x: None)
class TestMaster(TestCase):

    def setUp(self):
        threading.Thread.start = Mock()
        Master.create_process_monitor = Mock(return_value='test pm')
        Master.get_task_managers = Mock(return_value='test tm')

        self.master = Master()
        self.master.queued_tasks = ['task1']
        self.master.create_process_monitor = Mock(return_value=['pm1'])
        self.master.master_pipes = Mock()
        self.master.master_pipes.poll = Mock()
        self.master.master_pipes.send = Mock()
        self.master.master_pipes.recv = Mock()
        self.master.process_monitor_pipes = Mock()
        self.master.process_monitor_pipes.poll = Mock()
        self.master.process_monitor_pipes.send = Mock()
        self.master.process_monitor_pipes.recv = Mock()


    def tearDown(self):
        pass

    ## 무한루프때문에 종료가 안됨
    @patch("time.sleep", side_effect=InterruptedError)
    def test__execute_command(self, mocked_sleep):
        # given
        self.master.execute_task = Mock()
        self.master.set_task_manager_environment = Mock()

        # when
        self.master._execute_command()

        # then
        self.master.set_task_manager_environment.assert_called_once_with('test')
        self.master.execute_task.assert_called_once_with('test')
        self.assertRaise(InterruptedError)


    ## pipe mocking 문제가 발생
    def test__run_process_monitor(self):
        # given
        ProcessMonitor = Mock()
        ProcessMonitor.start = Mock()

        # when
        self.master._run_process_monitor('test tm', self.master.process_monitor_pipes)

        # then
        ProcessMonitor.assert_called_once()

    def test_create_process_monitor(self):
        self.fail()

    def test_get_task_managers(self):
        self.fail()

    def test_select_task_manager(self):
        self.fail()

    def test_request_experiments(self):
        self.fail()

    def test_check_task_manager_run_task_available(self):
        self.fail()

    def test_get_available_task_managers(self):
        self.fail()

    def test_execute_task(self):
        self.fail()

    def test_set_task_manager_environment(self):
        self.fail()
