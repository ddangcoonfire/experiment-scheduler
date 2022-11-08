from unittest import TestCase
from unittest.mock import Mock, patch

import experiment_scheduler
from experiment_scheduler.master.process_monitor import ProcessMonitor
from experiment_scheduler.task_manager.grpc_task_manager import task_manager_pb2


class MockTaskManagerStub:
    def __init__(self, *args, **kwargs):
        self.status = {'1': task_manager_pb2.TaskStatus.Status.RUNNING,
                       '2': task_manager_pb2.TaskStatus.Status.DONE,
                       '3': task_manager_pb2.TaskStatus.Status.KILLED,
                       '4': task_manager_pb2.TaskStatus.Status.ABNORMAL}

    def health_check(self, protobuf):
        return True

    def run_task(self, protobuf):
        return task_manager_pb2.TaskStatus(task_id=str(protobuf.task_id[0]),
                                           status=self.status[protobuf.task_id[0]])

    def kill_task(self, protobuf):
        return task_manager_pb2.TaskStatus(task_id=str(protobuf.task_id[0]),
                                           status=self.status[protobuf.task_id[0]])

    def get_task_status(self, protobuf):
        return task_manager_pb2.TaskStatus(task_id=str(protobuf.task_id[0]),
                                           status=self.status[protobuf.task_id[0]])

    def get_all_tasks(self, protobuf):
        all_tasks_status = task_manager_pb2.AllTasksStatus()
        for key, value in self.status.items():
            all_tasks_status.task_status_array.append(task_manager_pb2.TaskStatus(task_id=key,
                                                                                  status=value))
        return all_tasks_status

    def get_task_log(self, protobuf):
        return 'test_log'


class MockTask:
    def __init__(self):
        self.tasks = {'RUN': {'task_id': '1', 'status': task_manager_pb2.TaskStatus.RUNNING},
                      'DONE': {'task_id': '2', 'status': task_manager_pb2.TaskStatus.DONE},
                      'KILL': {'task_id': '3', 'status': task_manager_pb2.TaskStatus.KILLED},
                      'ABNORMAL': {'task_id': '4', 'status': task_manager_pb2.TaskStatus.ABNORMAL}}


class MockRunTask(MockTask):
    def __init__(self):
        self.task_id = '1'
        self.gpu_idx = 0
        self.command = 'Test_Run_Commnad',
        self.name = 'Test_Run_Name',
        self.env = 'Test_Run_Env'


class MockTaskStatement:
    def __init__(self, task_id, gpuidx, command, name, task_env):
        self.task_id = task_id,
        self.gpuidx = gpuidx,
        self.command = command,
        self.name = name,
        self.task_env = task_env


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


class MockTaskManager:
    def __init__(self):
        self.task_manager_address = ['1', '2']


class TestProcessMonitor(TestCase):
    run_task = MockRunTask()

    @patch("grpc.insecure_channel", lambda x: x + "test_channel")
    @patch("threading.Thread", MockThread)
    @patch.object(experiment_scheduler.master.process_monitor, 'TaskManagerStub', MockTaskManagerStub)
    @patch.object(experiment_scheduler.master.process_monitor, 'google_dot_protobuf_dot_empty__pb2',
                  MockGoogleProtoBufEmpty)
    def setUp(self):
        self.task_managers = MockTaskManager().task_manager_address
        self.process_monitor = ProcessMonitor(self.task_managers)
        self.task_manager = self.task_managers[0]
        self.mock_thread_queue = {'is_healthy': True}
        self.mock_task = MockTask()
        # self.mock_task_with_status = MockTaskWithStatus()

    def tearDown(self):
        pass

    @patch("time.sleep", side_effect=Exception)
    def test__health_check(self, mock_time_sleep):
        # when
        self.assertRaises(Exception, lambda: self.process_monitor._health_check(self.mock_thread_queue))

        # then
        self.assertEqual(self.mock_thread_queue['is_healthy'], True)

    def test_are_task_manager_healthy(self):
        # when
        test_return_value = self.process_monitor._are_task_manager_healthy()

        # then
        self.assertIsInstance(test_return_value, bool)

    @patch.object(experiment_scheduler.master.process_monitor, 'TaskStatement', MockTaskStatement)
    def test_run_task(self):
        # given
        run_task = MockRunTask()

        # when
        test_return_value = self.process_monitor.run_task(run_task.task_id, '1', run_task.gpu_idx, run_task.command,
                                                          run_task.name, run_task.env)

        # then
        self.assertEqual(task_manager_pb2.TaskStatus(task_id=str(run_task.task_id),
                                                     status=task_manager_pb2.TaskStatus.Status.RUNNING),
                         test_return_value)

    def test_kill_task(self):
        # given
        task = self.mock_task.tasks['KILL']

        # when
        test_return_value = self.process_monitor.kill_task(self.task_manager, str(task['task_id']))

        # then
        self.assertEqual(task_manager_pb2.TaskStatus(task_id=str(task['task_id']),
                                                     status=task['status']),
                         test_return_value)

    def test_get_task_status(self):
        # given
        for task in self.mock_task.tasks.values():
            # when
            test_return_value = self.process_monitor.get_task_status(self.task_manager, str(task['task_id']))

            # then
            self.assertEqual(task_manager_pb2.TaskStatus(task_id=str(task['task_id']),
                                                         status=task['status']),
                             test_return_value)

    def test_get_all_tasks(self):
        # when
        test_return_value = self.process_monitor.get_all_tasks()

        # then
        task_status_list = []
        for address in self.process_monitor.task_manager_address:
            all_task_status = task_manager_pb2.AllTasksStatus()
            for task in self.mock_task.tasks.values():
                all_task_status.task_status_array.append(task_manager_pb2.TaskStatus(task_id=task['task_id'],                                                                                     status=task['status']))
            task_status_list.append(all_task_status)
        self.assertEqual(test_return_value, task_status_list)

    def test_get_task_log(self):
        # given
        for task in self.mock_task.tasks.values():
            # when
            test_return_value = self.process_monitor.get_task_log(self.task_manager, task['task_id'])
            # then
            self.assertEqual(test_return_value, 'test_log')
