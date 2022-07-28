import grpc
from ..task_manager.task_manager_pb2_grpc import TaskManagerStub
from ..task_manager.task_manager_pb2 import TaskStatement, Task

# how to set path in python?

class ProcessMonitor:
    """
    ProcessMonitor communicates with TaskManagers.
    Select decent TaskManager for new task.
    All commands to TaskManager from Master must use ProcessMonitor
    """
    def __init__(self, task_managers):
        self.task_managers = task_managers
        self.channels = dict()
        self.init_task_manager_connection()
        self.task_list = dict()
        self.stubs = dict()

    # def _health_check(self, task_manager):
    #     response = self.stubs[task_manager].health_check()
    #     return response

    def init_task_manager_connection(self):
        """register all task manager's address"""
        for task_manager_address in self.task_managers:
            self.channels[task_manager_address] = grpc.insecure_channel(task_manager_address)
            self.stubs[task_manager_address] = TaskManagerStub(self.channels[task_manager_address])

    def select_task_manager(self, selected=-1):
        """
        Process Monitor automatically provide task that is able to run task
        :return:
        """
        # need convention later
        return self.task_managers[0] if selected < 0 else self.task_managers[selected]

    def _request_task_manager(self, task_manager, protobuf, request_type):
        """
        all direct request to task manager use this method
        :param protobuf:
        :param request_type:
        :return:
        """
        # unify all task manager communication here.
        if request_type == "run_task":
            response = self.stubs[task_manager].RunTask(protobuf)
        elif request_type == "get_task_status":
            response = self.stubs[task_manager].GetTaskStatus(protobuf)
        else:
            response = None
        return response

    def run_task(self, gpu_idx, command, name):
        task_manager = self.select_task_manager()
        protobuf = TaskStatement(gpuidx = gpu_idx, command = command, name = name)
        response = self._request_task_manager(task_manager, protobuf, "run_task")
        task_id = response.task_id
        return task_id

    def kill_task(self, task_id):
        task_manager = self.select_task_manager()
        protobuf = ""
        self._request_task_manager(task_manager, protobuf, "kill_task")

    def get_task_status(self,task_id):
        task_manager = self.select_task_manager()
        protobuf = Task(task_id = task_id)
        self._request_task_manager(task_manager, protobuf, "get_task_status")

    def get_all_tasks(self):
        task_manager = self.select_task_manager()
        protobuf = ""
        self._request_task_manager(task_manager, protobuf, "get_task_status")
