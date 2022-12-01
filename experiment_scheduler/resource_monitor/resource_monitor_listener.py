"""
Master side of resource monitor.
ResourceMonitorListener periodically check task manager side's resource monitor.
Get TM side's status from RM
"""

from typing import List
import threading
import time
import grpc
from grpc import RpcError
from experiment_scheduler.resource_monitor.grpc_resource_monitor import (
    resource_monitor_pb2_grpc,
)


class ResourceMonitorListener:  # pylint: disable=too-few-public-methods
    """
    Master has one ResourceMonitorListener.
    RML has two roles:
        RML checks all resource monitor's status (health checking)
        RML get available gpu index from resource monitor.
    """

    def __init__(self, resource_monitor_address: List[str]):
        self.proto_empty = (
            resource_monitor_pb2_grpc.google_dot_protobuf_dot_empty__pb2.Empty()
        )
        self.resource_monitor_address: List[str] = resource_monitor_address
        self.resource_monitor_health_queue = self._init_resource_monitor_health_queue()
        self.resource_monitor_stubs: dict = self._get_resource_monitor_stubs()
        self.resource_monitor_health_check_thread = threading.Thread(
            target=self._health_check_resource_monitor, daemon=True
        )
        self.resource_monitor_health_check_thread.start()

    def _init_resource_monitor_health_queue(self):
        queue = dict()
        for address in self.resource_monitor_address:
            queue[f"is_{address}_healthy"] = False
        return queue

    def _are_resource_monitors_healthy(self) -> bool:
        """
        if a resource monitor is not connected, returns false.
        :return:
        """
        for address in self.resource_monitor_address:
            if not self.resource_monitor_health_queue[f"is_{address}_healthy"]:
                return False
        return True
        # for HA, this logic must be separated per resource monitor

    def _health_check_resource_monitor(self, time_interval=5) -> None:
        """
        a thread run this method permanently, changing it's value by communicating with resource monitor.
        :param time_interval: how frequently you want to check (sec)
        :return:
        """
        while True:
            for address, stub in self.resource_monitor_stubs.items():
                try:
                    stub.health_check(self.proto_empty)
                    self.resource_monitor_health_queue[f"is_{address}_healthy"] = True
                except RpcError:
                    self.resource_monitor_health_queue[f"is_{address}_healthy"] = False
            time.sleep(time_interval)

    def _get_resource_monitor_stubs(self) -> dict:
        """
        return dictation of channel stubs(communicator)
        :return:
        """
        stubs = dict()
        for address in self.resource_monitor_address:
            channel = grpc.insecure_channel(address)
            stubs[address] = resource_monitor_pb2_grpc.ResourceMonitorStub(channel)
        return stubs

    def get_available_gpu_idx(self, resource_monitor_address: str) -> int:
        """
        return available gpu index
        :param resource_monitor_address:
        :return:
        """
        if self.resource_monitor_health_queue[f"is_{resource_monitor_address}_healthy"]:
            try:
                resource_monitor_response = self.resource_monitor_stubs[
                    resource_monitor_address
                ].get_available_gpu_idx(self.proto_empty)
                response = resource_monitor_response.available_gpu_idx
            except RpcError as error:
                print(
                    f"GRPC Error Occured: {error} \nMaybe you should install NVML Library"
                )
                response = -1
        else:
            # must be replaced with logging
            print(
                f"currently resource monitor {resource_monitor_address} is not available"
            )
            response = -1
        return response
