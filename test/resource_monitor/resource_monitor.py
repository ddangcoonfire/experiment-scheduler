"""
test resource monitor

"""

import pytest
from experiment_scheduler.resource_monitor.resource_monitor import ResourceMonitor
from experiment_scheduler.resource_monitor.grpc_resource_monitor import resource_monitor_pb2,resource_monitor_pb2_grpc
# get_available_gpu_idx
# get_resource_status
# health_check
import grpc_testing
import grpc
import unittest
from unittest import TestCase
from concurrent import futures
from unittest.mock import patch
from unittest.mock import Mock

class ResourceMonitorTest(TestCase):
    def setUp(self) -> None:
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        resource_monitor_pb2_grpc.add_ResourceMonitorServicer_to_server(ResourceMonitor, self._server)
        self._server.add_insecure_port('[::]:50051')
        self._server.start()

        self._channel = grpc.insecure_channel('localhost:50051')
        self._stub = resource_monitor_pb2_grpc.ResourceMonitorStub(self._channel)

        self._context = Mock()
        self._rm = ResourceMonitor()

    def test_health_check(self):
        request = resource_monitor_pb2_grpc.google_dot_protobuf_dot_empty__pb2.Empty()
        response = self._rm.health_check(request,self._context)
        # response = self._stub.health_check(request, self._context)
        assert(response.alive == True)

if __name__ == "__main__":
    unittest.main()