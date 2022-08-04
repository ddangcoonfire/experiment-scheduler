import grpc
from experiment_scheduler.task_manager.task_manager_pb2_grpc import TaskManagerStub
from experiment_scheduler.task_manager.task_manager_pb2 import TaskStatement, Task
from multiprocessing import Manager
import threading
import time


class ProcessMonitor:
    """
    ProcessMonitor communicates with TaskManagers.
    Select decent TaskManager for new task.
    All commands to TaskManager from Master must use ProcessMonitor
    """
    def __init__(self, task_manager, master_pipe, pool_size=5):
        self.task_manager = task_manager
        self.channel = grpc.insecure_channel(self.task_manager)
        self.stub = TaskManagerStub(self.channel[self.task_manager])
        self.master_pipe = master_pipe
        # connection initialization

        self.task_list = dict()
        self.completed_task_list = dict()
        # task list initializaiton

        self.shared_var_manager = Manager()
        self.thread_queue = self.shared_var_manager.dict()
        self.thread_queue["is_healthy"] = False
        # shared variable initialization

        self.health_checker = threading.Thread(target=self._health_check, args=(self.thread_queue,))
        self.health_checker.start()
        # health_checking_thread_on

        # shared with master memory

    def _health_check(self, thread_queue, time_interval=5):
        while True:
            response = self.stub.health_check()
            if response:
                thread_queue["is_healthy"] = True
            else:
                thread_queue["is_healthy"] = False
            time.sleep(time_interval)
    # should run this code through a thread.

    def is_healthy(self):
        return self.thread_queue["is_healthy"]

    def _request_task_manager(self, command):
        """
        all direct request to task manager use this method
        :param protobuf:
        :param request_type:
            :return:
        """
        # if request_task_manager need multithreading, use asyncio
        # multiprocessing, threading, asyncio
        # unify all task manager communication here.
        cmd = command[0]
        ret = ""
        if cmd == "kill_task":
            ret = self.kill_task(command[1])
        elif cmd == "get_task_status":
            ret = self.get_task_status(command[1])
        elif cmd == "get_all_tasks":
            ret = self.get_all_tasks()
        elif cmd == "run_task":
            ret = self.run_task(command[1], command[2], command[3])
        self.master_pipe.send(ret)

    def run_task(self, gpu_idx, command, name):
        protobuf = TaskStatement(gpuidx=gpu_idx, command=command, name=name)
        response = self.stub.RunTask(protobuf)
        task_id = response.task_id
        return task_id

    def kill_task(self, task_id):
        protobuf = Task(task_id=task_id)
        return self.stub.KillTask(protobuf)

    def get_task_status(self,task_id):
        protobuf = Task(task_id=task_id)
        return self.stub.GetTaskStatus(protobuf)

    def get_all_tasks(self):
        protobuf = ""
        return self.stub.GetAllTaskStatus(protobuf)

    def run(self, command):
        cmd = command[0]
        self._request_task_manager(cmd)

    def start(self, time_interval=1):
        # 로직 구현
        while True:
            # lock between sender and receiver must be set later
            command = self.master_pipe.recv()
            if len(command) > 0:
                self.run(command)
            time.sleep(time_interval)

