"""
test resource monitor listener

"""

from experiment_scheduler.resource_monitor.resource_monitor_listener import ResourceMonitorListener
from experiment_scheduler.resource_monitor.grpc_resource_monitor import resource_monitor_pb2,resource_monitor_pb2_grpc
import unittest
from unittest import TestCase


class ResourceMonitorListenerTest(TestCase):
    def setUp(self) -> None:
        self.test_address = list("MockingAddress")
        self.rml = ResourceMonitorListener(self.test_address)

    def test_get_available_gpu_idx(self):
        # Case 1. RM is Not Working
        test_idx = self.rml.get_available_gpu_idx(self.test_address[0])
        assert (type(test_idx) is int)
        # Case 2. RM is working properly
        test_idx = self.rml.get_available_gpu_idx(self.test_address[0])
        assert (type(test_idx) is int)


if __name__ == "__main__":
    unittest.main()