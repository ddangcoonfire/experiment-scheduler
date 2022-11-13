"""
test resource monitor

"""

from experiment_scheduler.resource_monitor.resource_monitor import ResourceMonitor
from experiment_scheduler.resource_monitor.grpc_resource_monitor import resource_monitor_pb2_grpc
import grpc
import unittest
from unittest import TestCase
from concurrent import futures
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
        # Case 1. return true to alive RM
        request = resource_monitor_pb2_grpc.google_dot_protobuf_dot_empty__pb2.Empty()
        # response = self._rm.health_check(request, self._context)
        response = self._stub.health_check(request, self._context)
        # Case 2. return false to dead RM

        assert(response.alive is True)

    def test_get_available_gpu_idx(self):
        request = resource_monitor_pb2_grpc.google_dot_protobuf_dot_empty__pb2.Empty()
        response = self._rm.get_available_gpu_idx(request, self._context)
        """
        CURRENTLY, In no gpu environment, an error pops up: 
        pynvml.nvml.NVMLError_LibraryNotFound: NVML Shared Library Not Found
        It has to throw decent exception when there's no gpu setting,
        return integer value as gpu index.
        """
        assert(response.available_gpu_idx == 1)

    def test_get_resource_status(self):
        request = resource_monitor_pb2_grpc.google_dot_protobuf_dot_empty__pb2.Empty()
        response = self._rm.get_resource_status(request, self._context)
        """
        CURRENTLY, In no gpu environment, an error pops up: 
        pynvml.nvml.NVMLError_LibraryNotFound: NVML Shared Library Not Found
        It has to throw decent exception when there's no gpu setting,
        return integer value as gpu index.
        """
        assert (response.status is dict())


if __name__ == "__main__":
    unittest.main()