from unittest import TestCase
from unittest.mock import Mock, patch

import experiment_scheduler
from experiment_scheduler.master.process_monitor import ProcessMonitor


class MockPipe:
    def __init__(self, *args, **kwargs):
        pass

    def send(self, *args, **kwargs):
        pass

    def poll(self, *args, **kwargs):
        pass

    def recv(self, *args, **kwargs):
        pass

class Response:
    task_id = 'test_id'
    def __init__(self, *args, **kwargs):
        pass

class MockTaskManagerStub:
    def __init__(self, *args, **kwargs):
        pass

    def health_check(self, protobuf):
        return True

    def run_task(self, protobuf):
        return Response()

    def kill_task(self, protobuf):
        return 'kill_task'

    def get_task_status(self, protobuf):
        return 'task_status'

    def get_all_tasks(self, protobuf):
        return ['task1', 'task2']

    def get_task_log(self, protobuf):
        return 'test_log'

class MockTaskStatement:
    def __init__(self, *args, **kwargs):
        pass


class MockGoogleProtoBufEmpty:
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def Empty():
        pass


class MockThread:
    def __init__(self, *args, **kwargs):
        pass

    def start(self):
        pass


class MockTask:
    def __init__(self, *args, **kwargs):
        pass


class TestProcessMonitor(TestCase):

    @patch("grpc.insecure_channel", lambda x: x + "test_channel")
    @patch("threading.Thread", MockThread)
    @patch.object(experiment_scheduler.master.process_monitor, 'TaskManagerStub', MockTaskManagerStub)
    @patch.object(experiment_scheduler.master.process_monitor, 'google_dot_protobuf_dot_empty__pb2',
                  MockGoogleProtoBufEmpty)
    def setUp(self):
        self.process_monitor = ProcessMonitor('test_network', MockPipe())
        self.mock_thread_queue = {'is_healthy': False}

    def tearDown(self):
        pass

    @patch("time.sleep", side_effect=Exception)
    def test__health_check(self, mock_time_sleep):
        # when
        self.assertRaises(Exception, lambda: self.process_monitor._health_check(self.mock_thread_queue))

        # then
        self.assertEqual(self.mock_thread_queue['is_healthy'], True)

    def test_is_healthy(self):
        # when
        test_return_value = self.process_monitor.is_healthy()

        # then
        self.assertIsInstance(test_return_value, bool)

    def test__request_task_manager(self):
        # given
        command_list = \
            [("kill_task", 'test', 'test', 'test', 'test', 'test')
                , ("get_task_status", 'test', 'test', 'test', 'test', 'test')
                , ("get_all_tasks", 'test', 'test', 'test', 'test', 'test')
                , ("run_task", 'test', 'test', 'test', 'test', 'test')]
        self.process_monitor.kill_task = Mock()
        self.process_monitor.get_task_status = Mock()
        self.process_monitor.get_all_tasks = Mock()
        self.process_monitor.run_task = Mock()

        # when
        for cmd in command_list:
            self.process_monitor._request_task_manager(cmd)

        # then
        self.process_monitor.kill_task.assert_called_once()
        self.process_monitor.get_task_status.assert_called_once()
        self.process_monitor.get_all_tasks.assert_called_once()
        self.process_monitor.run_task.assert_called_once()

    @patch.object(experiment_scheduler.master.process_monitor, 'TaskStatement', MockTaskStatement)
    def test_run_task(self):
        # given
        gpu_idx = 0
        command = 'cmd'
        name = 'test'
        env = 'test_env'

        # when
        test_return_value = self.process_monitor.run_task(gpu_idx, command, name, env)

        # then
        self.assertEqual(test_return_value, 'test_id')


    def test_kill_task(self):
        # given
        task_id = 'test_id'

        # when
        test_return_value = self.process_monitor.kill_task(task_id)

        # then
        self.assertEqual(test_return_value, 'kill_task')

    def test_get_task_status(self):
        # given
        task_id = 'test_id'

        # when
        test_return_value = self.process_monitor.get_task_status(task_id)

        # then
        self.assertEqual(test_return_value, 'task_status')

    def test_get_all_tasks(self):
        # when
        test_return_value = self.process_monitor.get_all_tasks()

        # then
        self.assertEqual(test_return_value, ['task1', 'task2'])



    def test_get_task_log(self):
        # given
        task_id = 'test_id'

        # when
        test_return_value = self.process_monitor.get_task_log(task_id)

        # then
        self.assertEqual(test_return_value, 'test_log')

    @patch("time.sleep", side_effect=Exception)
    def test_start(self, mock_time_sleep):
        # given
        MockPipe.poll = Mock(return_value= True)
        MockPipe.recv = Mock(return_value= 'cmd')
        self.process_monitor._request_task_manager = Mock()

        # when
        self.assertRaises(Exception, lambda : self.process_monitor.start())

        # then
        self.process_monitor.master_pipe.poll.assert_called_once()
        self.process_monitor.master_pipe.recv.assert_called_once()
        self.process_monitor._request_task_manager.assert_called_once()



