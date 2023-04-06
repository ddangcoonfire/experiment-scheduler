"""
Communication with Task Manager through Process Monitor
"""

import threading
import time
from multiprocessing import Manager
from typing import Any, Dict, List

import grpc
from grpc import RpcError

from experiment_scheduler.common.logging import get_logger
from experiment_scheduler.task_manager.grpc_task_manager.task_manager_pb2 import (
    AllTasksStatus,
    Task,
    TaskLogInfo,
    TaskStatement,
    google_dot_protobuf_dot_empty__pb2,
)
from experiment_scheduler.task_manager.grpc_task_manager.task_manager_pb2_grpc import (
    TaskManagerStub,
)

PROTO_EMPTY = google_dot_protobuf_dot_empty__pb2.Empty()


class ProcessMonitor:
    """
    ProcessMonitor communicates with TaskManagers.
    Select decent TaskManager for new task.
    All commands to TaskManager from Master must use ProcessMonitor
    """

    def __init__(self, task_managers: List[str]):
        self.task_manager_address = task_managers
        self.task_manager_stubs = self._get_stubs()
        # connection initialization

        self.shared_var_manager = Manager()
        self.thread_queue = self.shared_var_manager.dict()
        self._init_thread_queue()
        # shared variable initialization

        self.health_checker = threading.Thread(
            target=self._health_check, args=(self.thread_queue,)
        )
        self.health_checker.start()
        self.logger = get_logger("process_monitor")
        # health_checking_thread_on

        # shared with master memory

    def _init_thread_queue(self) -> None:
        for task_manager in self.task_manager_address:
            self.thread_queue[f"is_{task_manager}_healthy"] = False

    def _get_stubs(self) -> Dict[str, Any]:
        stubs = {}
        for address in self.task_manager_address:
            channel = grpc.insecure_channel(address)
            stubs[address] = TaskManagerStub(channel)
        return stubs

    def _health_check(self, thread_queue, time_interval=5):
        # move to decorator later
        while True:
            for task_manager in self.task_manager_address:
                try:
                    self.task_manager_stubs[task_manager].health_check(PROTO_EMPTY)
                    thread_queue[f"is_{task_manager}_healthy"] = True
                except RpcError as error:
                    thread_queue[f"is_{task_manager}_healthy"] = False
                    self.logger.error(
                        "currently task manager %s is not available.\n error log : %s",
                        task_manager,
                        error,
                    )
            time.sleep(time_interval)

    # should run this code through a thread.

    def _are_task_manager_healthy(self) -> bool:
        """

        :return:
        """
        for address in self.task_manager_address:
            if not self.thread_queue[f"is_{address}_healthy"]:
                return False
        return True

    def run_task(self, task_id, task_manager, command, name, env):
        """
        :param task_id
        :param task_manager:
        :param command:
        :param name:
        :param env:
        :return:
        """
        protobuf = TaskStatement(
            task_id=task_id, command=command, name=name, task_env=env
        )
        response = self.task_manager_stubs[task_manager].run_task(protobuf)
        return response

    def kill_task(self, task_manager, task_id):
        """
        FIXME
        :param task_manager:
        :param task_id:
        :return:
        """
        protobuf = Task(task_id=task_id)
        response = self.task_manager_stubs[task_manager].kill_task(protobuf)
        return response

    def get_task_log(self, task_manager, task_id, log_file_path):
        """
        :param task_manager:
        :param task_id:
        :param log_file_path:
        The response is sent by streaming.
        """
        protobuf = TaskLogInfo(task_id=task_id, log_file_path=log_file_path)
        for task_log_chunk in self.task_manager_stubs[task_manager].get_task_log(protobuf):
            yield task_log_chunk

    def get_available_task_managers(self):
        """
        returns addresses of runnable task managers
        :return:
        """
        available_task_managers = []
        for tm_address, tm_stub in self.task_manager_stubs.items():
            if tm_stub.has_idle_resource(PROTO_EMPTY).exists:
                available_task_managers.append(tm_address)
        return available_task_managers
