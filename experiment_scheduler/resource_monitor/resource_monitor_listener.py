from multiprocessing import Manager
import grpc
from typing import List
import threading
import time
from experiment_scheduler.resource_monitor.grpc_resource_monitor import resource_monitor_pb2_grpc, resource_monitor_pb2


class ResourceMonitorListener:
    def __init__(self, resource_monitor_address: List[str]):
        self.proto_empty = resource_monitor_pb2_grpc.google_dot_protobuf_dot_empty__pb2.Empty()
        self.resource_monitor_address: List[str] = resource_monitor_address
        self.resource_monitor_health_checker_manager = Manager()
        self.resource_monitor_health_queue = self.resource_monitor_health_checker_manager.dict()
        self.resource_monitor_stubs: dict = self._get_resource_monitor_stubs()
        self.resource_monitor_health_check_thread = threading.Thread(target=self._health_check_resource_monitor,
                                                                     daemon=True)
        self.resource_monitor_health_check_thread.start()

    def _are_resource_monitors_healthy(self):
        for address in self.resource_monitor_address:
            if not self.resource_monitor_health_queue[f"is_{address}_healthy"]:
                return False
        return True
        # for HA, this logic must be separated per resource monitor

    def _health_check_resource_monitor(self, time_interval=5):
        while True:
            for address, stub in self.resource_monitor_stubs.items():
                response = stub.health_check(self.proto_empty)
                if response:
                    self.resource_monitor_health_queue[f"is_{address}_healthy"] = True
                else:
                    self.resource_monitor_health_queue[f"is_{address}_health"] = False
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

    def get_available_gpu_idx(self, resource_monitor_address):
        if self.resource_monitor_health_queue[f"is_{resource_monitor_address}_healthy"]:
            response = self.resource_monitor_stubs[resource_monitor_address].get_available_gpu_idx(self.proto_empty)
        else:
            # must be replaced with logging
            print(f"currently {resource_monitor_address} is not available")
            response = -1
        return response
