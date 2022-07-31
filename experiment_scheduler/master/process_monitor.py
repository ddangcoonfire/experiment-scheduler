import grpc
from ..task_manager.task_manager_pb2_grpc import TaskManagerStub
from ..task_manager.task_manager_pb2 import TaskStatement, Task
from multiprocessing.pool import ThreadPool
from multiprocessing import Process, Manager
import threading
import time
# how to set path in python?

class ProcessMonitor:
    """
    ProcessMonitor communicates with TaskManagers.
    Select decent TaskManager for new task.
    All commands to TaskManager from Master must use ProcessMonitor
    """
    def __init__(self, task_manager, shared_memory, pool_size=5):
        self.task_manager = task_manager
        self.channel = grpc.insecure_channel(self.task_manager)
        self.stub = TaskManagerStub(self.channel[self.task_manager])
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

        self.command_queue = shared_memory
        # shared with master memory

    def _health_check(self, thread_queue):
        while True:
            response = self.stub.health_check()
            if response:
                thread_queue["is_healthy"] = True
            else:
                thread_queue["is_healthy"] = False
            time.sleep(5)
    # should run this code through a thread.

    def is_healthy(self):
        return self.thread_queue["is_healthy"]

    def _request_task_manager(self, task_manager, protobuf, request_type):
        """
        all direct request to task manager use this method
        :param protobuf:
        :param request_type:
            :return:
        """
        # if request_task_manager need multithreading, use asyncio
        # multiprocessing, threading, asyncio
        # unify all task manager communication here.
        if request_type == "run_task":
            response = self.stub.RunTask(protobuf)
        elif request_type == "get_task_status":
            response = self.stub.GetTaskStatus(protobuf)
        else:
            response = None
        return response

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
        if cmd == "kill_task":
            self.kill_task(command[1])
        elif cmd == "get_task_status":
            self.get_task_status(command[1])
        elif cmd == "get_all_tasks":
            self.get_all_tasks(command[1])
        elif cmd == "run_task":
            self.run_task(command[1],command[2],command[3])

    def start(self):
        # 로직 구현
        # Master call this method using Process
        # waiting 하면서 들어
        # 1. while waiting, 공통 자원을 바라보면서 값이 들어오면 처리
        # 2. 글쎄 고민해봐야
        while True:
            if len(self.command_queue) > 0:
                command = self.command_queue.pop()
                self.run(command)
            # how to communicate?
            # message queue? (rabbitmq + celery executor)
            # shared_variable? (Manager Object) - 0.1 --> 0.2~3
            # Pipe ( Uni direction... not recommended )
            time.sleep(1)

