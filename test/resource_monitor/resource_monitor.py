"""
test resource monitor

"""

import unittest
from unittest import TestCase
from unittest.mock import Mock
from concurrent import futures
from time import sleep
import grpc
from grpc import RpcError
from experiment_scheduler.resource_monitor.resource_monitor import ResourceMonitor
from experiment_scheduler.resource_monitor.grpc_resource_monitor import (
    resource_monitor_pb2_grpc,
)


class ResourceMonitorTest(TestCase):
    """
    test class for resource monitor.
    """

    def turnLocalServerOn(self):
        """
        turn grpc local server
        :return:
        """
        self._server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=10),
            options=(("grpc.so_reuseport", 5),),  # pylint:disable=R1732
        )
        resource_monitor_pb2_grpc.add_ResourceMonitorServicer_to_server(
            ResourceMonitor(), self._server
        )
        self._server.add_insecure_port("[::]:50051")
        self._server.start()
        sleep(5)

    def turnLocalServerOff(self):
        """
        turn grpc local server off
        :return:
        """
        self._server.stop(grace=None)

    def setUp(self) -> None:
        self._server = None
        self._channel = grpc.insecure_channel("localhost:50051")
        self._wrong_channel = grpc.insecure_channel("wrong_channel:50052")
        self._stub = resource_monitor_pb2_grpc.ResourceMonitorStub(self._channel)
        self._wrong_stub = resource_monitor_pb2_grpc.ResourceMonitorStub(
            self._wrong_channel
        )

        self._context = Mock()
        self._rm = ResourceMonitor()

    def test_health_check(self):
        """
        test health_check method
        :return:
        """
        self.turnLocalServerOn()
        # Case 1. return true to alive RM
        request = resource_monitor_pb2_grpc.google_dot_protobuf_dot_empty__pb2.Empty()
        response = self._stub.health_check(request)
        assert response.alive is True
        # Case 2. return Error to dead RM
        request = resource_monitor_pb2_grpc.google_dot_protobuf_dot_empty__pb2.Empty()
        try:
            self._wrong_stub.health_check(request)
            assert False
        except RpcError:
            print("return RpcError to wrong address")
        self.turnLocalServerOff()
        # Case 3. [Later] Return False to situation where RM is alive but has it's another problem.

    def test_get_available_gpu_idx(self):
        """
        test get_available_gpu_idx method
        :return:
        """
        self.turnLocalServerOn()

        request = resource_monitor_pb2_grpc.google_dot_protobuf_dot_empty__pb2.Empty()
        response = self._stub.get_available_gpu_idx(request)
        assert isinstance(response.available_gpu_idx, int)

        self.turnLocalServerOff()


if __name__ == "__main__":
    unittest.main()
