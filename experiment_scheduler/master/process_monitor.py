from datetime import datetime
import grpc


class ProcessMonitor:
    """
    ProcessMonitor communicates with TaskManagers.
    Select decent TaskManager for new task.
    All commands to TaskManager from Master must use ProcessMonitor
    """
    def __init__(self,task_managers):
        self.task_managers = task_managers
        self.channels = dict()
        self.init_task_manager_connection()
        self.task_list = dict()

    def init_task_manager_connection(self):
        """register all task manager's address"""
        for task_manager_address in self.task_managers:
            self.channels[task_manager_address] = grpc.insecure_channel(task_manager_address)

    def select_task_manager(self, selected=-1):
        """
        Process Monitor automatically provide task that is able to run task
        :return:
        """
        # need convention later
        return self.task_managers[0] if selected < 0 else self.task_managers[selected]

    def _request_task_manager(self, task_manager, command, request_type):
        """
        all direct request to task manager use this method
        :param command:
        :param request_type:
        :return:
        """
        pass

    def run_task(self, command):
        task_manager = self.select_task_manager()
        protobuf = ""
        self._request_task_manager(task_manager, protobuf, "run_task")

    def kill_task(self, task_id):
        task_manager = self.select_task_manager()
        protobuf = ""
        self._request_task_manager(task_manager, protobuf, "kill_task")

    def get_task_status(self,task_id):
        task_manager = self.select_task_manager()
        protobuf = ""
        self._request_task_manager(task_manager, protobuf, "get_task_status")


    def get_all_tasks(self):
        task_manager = self.select_task_manager()
        protobuf = ""
        self._request_task_manager(task_manager, protobuf, "get_task_status")
