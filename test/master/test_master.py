import random
import uuid
from collections import OrderedDict
from unittest import TestCase
from unittest.mock import Mock, patch

import experiment_scheduler
from experiment_scheduler.master.grpc_master import master_pb2
from experiment_scheduler.master.grpc_master.master_pb2 import TaskStatus as TaskStatus
from experiment_scheduler.master.master import Master


def mockGetTaskManagers():
    return ["test_network"]


def mockTaskId(run=True):
    if run:
        return "test_task_id"
    else:
        return "test_not_run_task_id"


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

    def get_available_gpu_idx(self, resource_monitor):
        if resource_monitor:
            gpu_idx = random.randint(1, 10)
            return gpu_idx, gpu_idx
        elif resource_monitor == -1:
            return -1, -1


class MockProcess:
    def __init__(self, *args, **kwargs):
        pass


class MockProcessMonitor:
    def __init__(self, *args, **kwargs):
        pass

    def start(self):
        pass

    @staticmethod
    def run_task(task_id, task_manager, gpu_idx, command, name, env):
        return master_pb2.TaskStatus(task_id=task_id, status=TaskStatus.Status.RUNNING)


class MockThread:
    def __init__(self, *args, **kwargs):
        pass

    def start(self):
        pass


class MockTask:
    name = "test"
    command = "task"
    task_env = {"test": "env"}

    def __init__(self, task_id=mockTaskId(), run=True):
        self.task_id = task_id if run else mockTaskId(False)


class MockTaskWithStatus:

    def __init__(self, task_id, status):
        self.task_id = task_id
        self.status = status


class MockTaskManagerAddress:

    def __init__(self, task_managers_address):
        self.address_list = task_managers_address

    def get_address_list(self):
        return self.address_list;


class TestMaster(TestCase):
    @patch.object(
        experiment_scheduler.master.master, "get_task_managers", mockGetTaskManagers
    )
    @patch("threading.Thread", MockThread)
    def setUp(self):
        Master.get_task_managers = Mock(return_value=mockGetTaskManagers())
        self.master = Master()
        self.master.queued_tasks = OrderedDict([(mockTaskId(False), MockTask(None, False))])
        self.master.running_tasks = OrderedDict(
            [(mockTaskId(), {"task": MockTask(), "task_manager": "test_task_manager",
                             "gpu_idx": 1})])

    def tearDown(self):
        patch.stopall()

    @patch("time.sleep", side_effect=Exception)
    def test__execute_command(self, mock_time_sleep):
        # given
        self.master.execute_task = Mock()
        mock_available_task_managers_address = MockTaskManagerAddress([1, 2, 3]);
        self.master.process_monitor.get_available_task_managers = Mock(
            return_value=(mock_available_task_managers_address.get_address_list())
        )

        # when
        self.assertRaises(Exception, lambda: self.master._execute_command())

        # then
        self.master.execute_task.assert_called_with(mock_available_task_managers_address.get_address_list()[0])

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

    def test_kill_not_start_task(self):
        # given
        test_request = MockTask(None, False)
        self.master._wrap_by_task_status = Mock(
            return_value=TaskStatus(
                task_id=test_request.task_id,
                status=TaskStatus.Status.KILLED
            )
        )

        # when
        test_return_value = self.master.kill_task(test_request, None)

        # then
        self.assertEqual(test_request.task_id, test_return_value.task_id)
        self.assertEqual(TaskStatus.Status.KILLED, test_return_value.status)

    def test_kill_run_task(self):
        # given
        test_request = MockTask()
        self.master.process_monitor.kill_task = Mock(
            return_value=TaskStatus(
                task_id=test_request.task_id,
                status=TaskStatus.Status.KILLED
            )
        )

        # when
        test_return_value = self.master.kill_task(test_request, None)

        # then
        self.assertEqual(test_request.task_id, test_return_value.task_id)
        self.assertEqual(TaskStatus.Status.KILLED, test_return_value.status)

    def test_kill_not_found_task(self):
        # given
        test_request = MockTask("not_found_task_id")
        self.master.process_monitor.kill_task = Mock(
            return_value=master_pb2.TaskStatus(
                task_id=test_request.task_id,
                status=TaskStatus.Status.NOTFOUND
            )
        )

        # when
        test_return_value = self.master.kill_task(test_request, None)

        # then
        self.assertEqual(test_request.task_id, test_return_value.task_id)
        self.assertEqual(TaskStatus.Status.NOTFOUND, test_return_value.status)

    def test_get_status_not_start_task(self):
        # given
        test_request = MockTask(None, False)
        self.master._wrap_by_task_status = Mock(
            return_value=TaskStatus(
                task_id=test_request.task_id,
                status=TaskStatus.Status.NOTSTART
            )
        )

        # when
        test_return_value = self.master.get_task_status(test_request, None)

        # then
        self.assertEqual(test_request.task_id, test_return_value.task_id)
        self.assertEqual(TaskStatus.Status.NOTSTART, test_return_value.status)

    def test_get__status_run_task(self):
        # given
        test_request = MockTask()
        self.master.process_monitor.get_task_status = Mock(
            return_value=TaskStatus(
                task_id=test_request.task_id,
                status=TaskStatus.Status.RUNNING
            )
        )

        # when
        test_return_value = self.master.get_task_status(test_request, None)

        # then
        self.assertEqual(test_request.task_id, test_return_value.task_id)
        self.assertEqual(TaskStatus.Status.RUNNING, test_return_value.status)

    def test_get_status_killed_task(self):
        # given
        test_request = MockTask()
        self.master.process_monitor.get_task_status = Mock(
            return_value=TaskStatus(
                task_id=test_request.task_id,
                status=TaskStatus.Status.KILLED
            )
        )

        # when
        test_return_value = self.master.get_task_status(test_request, None)

        # then
        self.assertEqual(test_request.task_id, test_return_value.task_id)
        self.assertEqual(TaskStatus.Status.KILLED, test_return_value.status)
        self.assertEqual(None, self.master.running_tasks.get(test_request.task_id));

    def test_get_status_not_found_task(self):
        # given
        test_request = MockTask("Not_Found_Task")

        # when
        test_return_value = self.master.get_task_status(test_request, None)

        # then
        self.assertEqual(test_return_value.task_id, test_request.task_id)
        self.assertEqual(TaskStatus.Status.NOTFOUND, test_return_value.status)

    def test_execute_task(self):
        # given
        self.master.process_monitor.run_task = Mock(
            return_value=TaskStatus(
                task_id=mockTaskId(False),
                status=TaskStatus.Status.RUNNING
            )
        )
        # when
        test_return_value = self.master.execute_task(task_manager="test_task_manager")

        # then
        self.assertEqual(mockTaskId(False), test_return_value.task_id)
        self.assertEqual(TaskStatus.Status.RUNNING, test_return_value.status)
        self.assertEqual(self.master.running_tasks[test_return_value.task_id]['task_manager'], "test_task_manager")
