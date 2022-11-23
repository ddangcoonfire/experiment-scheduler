"""
Communication with Task Manager through Process Monitor
"""

from multiprocessing import Manager
import threading
import time
from typing import Dict, List, Any
import grpc
from experiment_scheduler.task_manager.grpc_task_manager.task_manager_pb2_grpc import (
    TaskManagerStub,
)
from experiment_scheduler.task_manager.grpc_task_manager.task_manager_pb2 import (
    TaskStatement,
    AllTasksStatus,
    Task,
    google_dot_protobuf_dot_empty__pb2,
)


class ProcessMonitor:
    """
    ProcessMonitor communicates with TaskManagers.
    Select decent TaskManager for new task.
    All commands to TaskManager from Master must use ProcessMonitor
    """

    def __init__(self, task_managers: List[str]):
        self.task_manager_address = task_managers
        self.task_manager_stubs = self._get_stubs()
        self.proto_empty = google_dot_protobuf_dot_empty__pb2.Empty()
        # connection initialization

        self.shared_var_manager = Manager()
        self.thread_queue = self.shared_var_manager.dict()
        self._init_thread_queue()
        # shared variable initialization

        self.health_checker = threading.Thread(
            target=self._health_check, args=(self.thread_queue,)
        )
        self.health_checker.start()
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
                response = self.task_manager_stubs[task_manager].health_check(
                    self.proto_empty
                )
                if response:
                    thread_queue[f"is_{task_manager}_healthy"] = True
                else:
                    thread_queue[f"is_{task_manager}_healthy"] = False
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

    def run_task(
        self, task_id, task_manager, gpu_idx, command, name, env
    ):
        """
        :param task_id
        :param task_manager:
        :param gpu_idx:
        :param command:
        :param name:
        :param env:
        :return:
        """
        protobuf = TaskStatement(
            task_id=task_id, gpuidx=gpu_idx, command=command, name=name, task_env=env
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

    def get_task_status(self, task_manager, task_id):
        """
        FIXME
        :param task_manager:
        :param task_id:
        :return:
        """
        protobuf = Task(task_id=task_id)
        return self.task_manager_stubs[task_manager].get_task_status(protobuf)

    def get_all_tasks(self):
        """
        FIXME
        :param: task_manager
        :return:
        """

        all_tasks_status = []
        for address in self.task_manager_address:
            protobuf = self.proto_empty
            all_tasks_status.append(
                self.task_manager_stubs[address].get_all_tasks(protobuf)
            )
        return all_tasks_status

    def get_task_log(self, task_manager, task_id):
        """
        FIXME
        :param task_manager:
        :param task_id:
        :return:
        """
        protobuf = Task(task_id=task_id)
        return self.task_manager_stubs[task_manager].get_task_log(protobuf)
