import grpc

from experiment_scheduler.task_manager.grpc_task_manager.task_manager_pb2_grpc import TaskManagerStub

class Task:

    def __init__(self, id, name, command, env):
        # self.task_manager = None
        # self.channel = None
        # self.stub = None
        # self.master_pipe = None
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


    # def set_task_manager(self, task_manager):
    #     self.task_manager = task_manager
    #
    # def set_master_pipe_manager(self, master_pipe):
    #     self.master_pipe = master_pipe

    # = grpc.insecure_channel(self.task_manager)
    # = TaskManagerStub(self.channel)
    # = master_pipe
    # task 인스턴스 메소드로 해당 인스턴스가 process monitor의 함수를 호출
    def run_task(self):
        pass

    def kill_task(self):
        pass

    def get_task_status(self):
        pass

    def get_task_log(self):
        pass