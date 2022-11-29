"""
test resource monitor listener

"""
import unittest
from unittest import TestCase
from time import sleep
from concurrent import futures
import grpc
from experiment_scheduler.resource_monitor.resource_monitor import ResourceMonitor
from experiment_scheduler.resource_monitor.resource_monitor_listener import (
    ResourceMonitorListener,
)
from experiment_scheduler.resource_monitor.grpc_resource_monitor import (
    resource_monitor_pb2_grpc,
)


class ResourceMonitorListenerTest(TestCase):
    """
    test class for resource monitor listener
    """

    def setUp(self) -> None:
        self.test_address = ["MockingAddress"]
        self.rml = ResourceMonitorListener(self.test_address)
        self.rml_working = ResourceMonitorListener(["localhost:50051"])

        self._server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=10)  # pylint:disable=R1732
        )
        resource_monitor_pb2_grpc.add_ResourceMonitorServicer_to_server(
            ResourceMonitor(), self._server
        )
        self._server.add_insecure_port("[::]:50051")
        self._server.start()
        sleep(5)  # give time for server initialization.

    def test_get_available_gpu_idx(self):
        """
        test class for get_available_gpu_idx
        :return:
        """
        # Case 1. RM is Not Working
        # test_idx = self.rml.get_available_gpu_idx(self.test_address[0])
        test_idx = self.rml.get_available_gpu_idx(self.test_address[0])
        assert test_idx == -1
        # Case 2. RM is working properly
        # assert (type(test_idx) is int)
        test_idx = self.rml_working.get_available_gpu_idx("localhost:50051")
        assert isinstance(test_idx, int)


if __name__ == "__main__":
    unittest.main()
