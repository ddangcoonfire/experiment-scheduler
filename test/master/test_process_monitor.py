from unittest import TestCase
from unittest.mock import Mock, patch

import experiment_scheduler
from experiment_scheduler.master.process_monitor import ProcessMonitor
from experiment_scheduler.task_manager.grpc_task_manager import task_manager_pb2


class MockTaskManagerStub:
    def __init__(self, has_idle_resource=True):
        self.status = {
            "1": task_manager_pb2.TaskStatus.Status.RUNNING,
            "2": task_manager_pb2.TaskStatus.Status.DONE,
            "3": task_manager_pb2.TaskStatus.Status.KILLED,
            "4": task_manager_pb2.TaskStatus.Status.ABNORMAL,
        }
        self.has_idle = has_idle_resource

    def health_check(self, protobuf):
        return True

    def run_task(self, protobuf):
        return task_manager_pb2.TaskStatus(
            task_id=str(protobuf.task_id[0]), status=self.status[protobuf.task_id[0]]
        )

    def kill_task(self, protobuf):
        return task_manager_pb2.TaskStatus(
            task_id=str(protobuf.task_id[0]), status=self.status[protobuf.task_id[0]]
        )

    def get_task_status(self, protobuf):
        return task_manager_pb2.TaskStatus(
            task_id=str(protobuf.task_id[0]), status=self.status[protobuf.task_id[0]]
        )

    def get_all_tasks(self, protobuf):
        response = []
        for key, value in self.status.items():
            if response is not None:
                response.append(task_manager_pb2.TaskStatus(task_id=key, status=value))
            else:
                response = task_manager_pb2.TaskStatus(task_id=key, status=value)
        return response

    def get_task_log(self, protobuf):
        return "test_log"

    def has_idle_resource(self, protobuf):
        if self.has_idle:
            return True
        else:
            return False


class MockTask:
    def __init__(self):
        self.tasks = {
            "RUN": {
                "task_id": "1",
                "task_manager": "tm_address1",
                "status": task_manager_pb2.TaskStatus.RUNNING,
            },
            "DONE": {
                "task_id": "2",
                "task_manager": "tm_address1",
                "status": task_manager_pb2.TaskStatus.DONE,
            },
            "KILL": {
                "task_id": "3",
                "task_manager": "tm_address1",
                "status": task_manager_pb2.TaskStatus.KILLED,
            },
            "ABNORMAL": {
                "task_id": "4",
                "task_manager": "tm_address1",
                "status": task_manager_pb2.TaskStatus.ABNORMAL,
            },
        }


class MockRunTask(MockTask):
    def __init__(self):
        self.task_id = "1"
        self.task_manager = "tm_address1"
        self.command = ("Test_Run_Commnad",)
        self.name = ("Test_Run_Name",)
        self.env = "Test_Run_Env"


class MockTaskStatement:
    def __init__(self, task_id, command, name, task_env):
        self.task_id = (task_id,)
        self.command = (command,)
        self.name = (name,)
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
        self.task_manager_address = ["tm_address1"]


class TestProcessMonitor(TestCase):
    run_task = MockRunTask()

    @patch("grpc.insecure_channel", lambda x: x + "test_channel")
    @patch("threading.Thread", MockThread)
    @patch.object(
        experiment_scheduler.master.process_monitor,
        "TaskManagerStub",
        MockTaskManagerStub,
    )
    @patch.object(
        experiment_scheduler.master.process_monitor,
        "google_dot_protobuf_dot_empty__pb2",
        MockGoogleProtoBufEmpty,
    )
    def setUp(self):
        self.task_managers = MockTaskManager().task_manager_address
        self.process_monitor = ProcessMonitor(self.task_managers)
        self.task_manager = self.task_managers[0]
        self.mock_thread_queue = {"is_healthy": True}
        self.mock_task = MockTask()
        self.process_monitor.task_manager_stubs = {
            "tm_address1": MockTaskManagerStub(),
            "tm_address2": MockTaskManagerStub(False),
        }
        # self.mock_task_with_status = MockTaskWithStatus()

    def tearDown(self):
        pass

    @patch("time.sleep", side_effect=Exception)
    def test__health_check(self, mock_time_sleep):
        # when
        self.assertRaises(
            Exception,
            lambda: self.process_monitor._health_check(self.mock_thread_queue),
        )

        # then
        self.assertEqual(self.mock_thread_queue["is_healthy"], True)

    def test_are_task_manager_healthy(self):
        # when
        test_return_value = self.process_monitor._are_task_manager_healthy()

        # then
        self.assertIsInstance(test_return_value, bool)

    @patch.object(
        experiment_scheduler.master.process_monitor, "TaskStatement", MockTaskStatement
    )
    def test_run_task(self):
        # given
        run_task = MockRunTask()

        # when
        test_return_value = self.process_monitor.run_task(
            run_task.task_id,
            run_task.task_manager,
            run_task.command,
            run_task.name,
            run_task.env,
        )

        # then
        self.assertEqual(
            task_manager_pb2.TaskStatus(
                task_id=str(run_task.task_id),
                status=task_manager_pb2.TaskStatus.Status.RUNNING,
            ),
            test_return_value,
        )

    def test_kill_task(self):
        # given
        task = self.mock_task.tasks["KILL"]

        # when
        test_return_value = self.process_monitor.kill_task(
            task["task_manager"], str(task["task_id"])
        )

        # then
        self.assertEqual(
            task_manager_pb2.TaskStatus(
                task_id=str(task["task_id"]), status=task["status"]
            ),
            test_return_value,
        )

    def test_get_task_status(self):
        # given
        for task in self.mock_task.tasks.values():
            # when
            test_return_value = self.process_monitor.get_task_status(
                task["task_manager"], str(task["task_id"])
            )

            # then
            self.assertEqual(
                task_manager_pb2.TaskStatus(
                    task_id=str(task["task_id"]), status=task["status"]
                ),
                test_return_value,
            )

    def test_get_all_tasks(self):
        # when
        test_return_value = self.process_monitor.get_all_tasks()

        # then
        task_status_list = []
        for address in self.process_monitor.task_manager_address:
            all_task_status = task_manager_pb2.AllTasksStatus()
            for task in self.mock_task.tasks.values():
                all_task_status.append(
                    task_manager_pb2.TaskStatus(
                        task_id=task["task_id"], status=task["status"]
                    )
                )
            task_status_list.append(all_task_status)
        self.assertEqual(test_return_value, task_status_list)

    def test_get_task_log(self):
        # given
        for task in self.mock_task.tasks.values():
            # when
            test_return_value = self.process_monitor.get_task_log(
                self.task_manager, task["task_id"]
            )
            # then
            self.assertEqual(test_return_value, "test_log")

    def test_get_available_task_managers(self):
        # when
        test_return_value = self.process_monitor.get_available_task_managers()
        # then
        for tm_address, tm_stub in self.process_monitor.task_manager_stubs.items():
            if tm_stub.has_idle:
                self.assertTrue(test_return_value.__contains__(tm_address))
            else:
                self.assertFalse(test_return_value.__contains__(tm_address))
