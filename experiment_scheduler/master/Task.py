import grpc

from experiment_scheduler.task_manager.grpc_task_manager.task_manager_pb2_grpc import TaskManagerStub

class Task:

    def __init__(self, id, name, command, env):
        self.__gpu_idx = None
        self.__task_manager = None
        self.task_id = id
        self.name = name
        self.command = command
        self.env = dict(env)

    @property
    def gpu_idx(self):  # getter
        return self.__gpu_idx

    @gpu_idx.setter
    def gpu_idx(self, gpu_idx):  # setter
        self.__gpu_idx = gpu_idx

    @property
    def task_manager(self):  # getter
        return self.__task_manager

    @task_manager.setter
    def gpu_idx(self, task_manager):  # setter
        self.__task_manager = task_manager
