import unittest
import grpc
import experiment_scheduler.master.grpc_master.master_pb2 as master_pb2
import experiment_scheduler.master.grpc_master.master_pb2_grpc as master_pb2_grpc
from experiment_scheduler.master.master import Master


class TestMaster(unittest.TestCase):
    def setUp(self):
        self.server = grpc.server(grpc.local_server_credentials())
        master_pb2_grpc.add_MasterServicer_to_server(MockMaster(), self.server)
        port = self.server.add_insecure_port("[::]:0")
        self.server.start()
        self.channel = grpc.insecure_channel("localhost:%d" % port)
        self.master = Master(channel=self.channel)

    def tearDown(self):
        self.channel.close()
        self.server.stop(0)

    def test_request_experiments(self):
        # Test request experiments
        experiment_statement = master_pb2.ExperimentStatement()
        response = self.master.request_experiments(experiment_statement)
        self.assertIsInstance(response, master_pb2.MasterResponse)

    def test_kill_task(self):
        # Test kill task
        task = master_pb2.Task()
        response = self.master.kill_task(task)
        self.assertIsInstance(response, master_pb2.TaskStatus)

    def test_get_task_status(self):
        # Test get task status
        task = master_pb2.Task()
        response = self.master.get_task_status(task)
        self.assertIsInstance(response, master_pb2.TaskStatus)

    def test_get_task_log(self):
        # Test get task log
        task = master_pb2.Task()
        response = self.master.get_task_log(task)
        self.assertIsInstance(response, master_pb2.TaskLog)

    def test_get_all_tasks(self):
        """
        Test the `get_all_tasks` method of the `Master` class.

        This method should return a `AllExperimentsStatus` message, which contains
        the status of all tasks in the specified experiment.

        This test case covers the following scenarios:
        - Empty experiment: When there are no tasks in the experiment, the response should
          contain an empty list of tasks.
        - One task experiment: When there is only one task in the experiment, the response
          should contain a list with a single task status.
        - Multiple tasks experiment: When there are multiple tasks in the experiment, the
          response should contain a list with the status of all tasks in the experiment.

        """
        # Test with empty experiment
        experiment = master_pb2.Experiment()
        response = self.master.get_all_tasks(experiment)
        self.assertIsInstance(response, master_pb2.AllExperimentsStatus)
        self.assertEqual(len(response.experiment_statuses), 0)

        # Test with one task experiment
        task = master_pb2.Task()
        experiment = master_pb2.Experiment(tasks=[task])
        response = self.master.get_all_tasks(experiment)
        self.assertIsInstance(response, master_pb2.AllExperimentsStatus)
        self.assertEqual(len(response.experiment_statuses), 1)
        self.assertEqual(len(response.experiment_statuses[0].task_statuses), 1)

        # Test with multiple tasks experiment
        task1 = master_pb2.Task(task_id="task1")
        task2 = master_pb2.Task(task_id="task2")
        experiment = master_pb2.Experiment(tasks=[task1, task2])
        response = self.master.get_all_tasks(experiment)
        self.assertIsInstance(response, master_pb2.AllExperimentsStatus)
        self.assertEqual(len(response.experiment_statuses), 1)
        self.assertEqual(len(response.experiment_statuses[0].task_statuses), 2)
        self.assertIn(
            response.experiment_statuses[0].task_statuses[0].task_id, ["task1", "task2"]
        )
        self.assertIn(
            response.experiment_statuses[0].task_statuses[1].task_id, ["task1", "task2"]
        )
        self.assertNotEqual(
            response.experiment_statuses[0].task_statuses[0].task_id,
            response.experiment_statuses[0].task_statuses[1].task_id,
        )
        experiment = master_pb2.Experiment()
        response = self.master.get_all_tasks(experiment)
        self.assertIsInstance(response, master_pb2.AllExperimentsStatus)

    def test_halt_process_monitor(self):
        # Test halt process monitor
        response = self.master.halt_process_monitor()
        self.assertIsInstance(response, master_pb2.Empty)


class MockMaster(master_pb2_grpc.MasterServicer):
    def request_experiments(self, request, context):
        return master_pb2.MasterResponse()

    def kill_task(self, request, context):
        return master_pb2.TaskStatus()

    def get_task_status(self, request, context):
        return master_pb2.TaskStatus()

    def get_task_log(self, request, context):
        return master_pb2.TaskLog()

    def get_all_tasks(self, request, context):
        return master_pb2.AllExperimentsStatus()

    def halt_process_monitor(self, request, context):
        return master_pb2.Empty()


if __name__ == "__main__":
    unittest.main()
