from experiment_scheduler.master.process_monitor import ProcessMonitor
from experiment_scheduler.master.grpc_master.master_pb2_grpc import MasterServicer, add_MasterServicer_to_server
from experiment_scheduler.master.grpc_master import master_pb2
from multiprocessing import Process, Pipe
import grpc
from concurrent import futures
import uuid
import multiprocessing
import time
import threading


class Master(MasterServicer):
    """
    Inherit GrpcServer to run Grpc Socket ( get request from submitter )
    Class that runs on server
    """
    def __init__(self, max_workers=10):
        """
        Init GrpcServer.
        """
        self.queued_tasks = []
        self.master_pipes = dict()
        self.process_monitor_pipes = dict()
        self.task_managers_address = self.get_task_managers()
        self.process_monitor = self.create_process_monitor()
        self.runner = threading.Thread(target=self._execute_command)
        self.runner.start()

    def _execute_command(self, interval=1):
        """
        this thread_running_function periodically checks queued_task and available task_managers.
        If a task exists and available task manager exists, toss command to Process Monitor
        :param interval: time interval
        :return: None
        """
        while True:
            available_task_managers = self.get_available_task_managers()
            for task in self.queued_tasks:
                if len(available_task_managers) > 0:
                    task_manager = available_task_managers.pop(0)
                    self.set_task_manager_environment(task_manager)
                    self.execute_task(task_manager)
            time.sleep(interval)

    def _run_process_monitor(self,task_manager_address, pipe):
        """
        Create Process Monitor process per task manager
        :param task_manager_address:
        :param pipe:
        :return:
        """
        pm = ProcessMonitor(task_manager_address, pipe)
        pm.start()

    def create_process_monitor(self):
        process_monitor_list = list()
        for task_manager in self.task_managers_address:
            self.master_pipes[task_manager], self.process_monitor_pipes[task_manager] = Pipe()
            p = Process(target=self._run_process_monitor, args=(task_manager, self.process_monitor_pipes[task_manager]))
            process_monitor_list.append(p)
        return process_monitor_list

    def get_task_managers(self):
        return ["localhost"]

    def select_task_manager(self, selected=-1):
        """
        Process Monitor automatically provide task that is able to run task
        :return:
        """
        # need convention later
        return self.task_managers_address[0] if selected < 0 else self.task_managers_address[selected]

    def request_experiments(self, request, context):
        experiment_id = request.name + '-' + str(uuid.uuid1())
        for task in request.tasks:
            self.queued_tasks.append(task)
        response_status = master_pb2.MasterResponse.ResponseStatus
        response = response_status.SUCCESS if experiment_id is not None else response_status.FAIL
        return master_pb2.MasterResponse(experiment_id=experiment_id, response=response)

    def check_task_manager_run_task_available(self,task_manager):
        # currently only returns True
        return True

    def get_available_task_managers(self):
        # currently only return first one
        available_task_managers = []
        for task_manager in self.task_managers_address[0]:
            if self.check_task_manager_run_task_available(task_manager):
                available_task_managers.append(task_manager)
        # return available_task_managers
        return [self.task_managers_address[0]]

    def execute_task(self,task_manager):
        prior_task = self.queued_tasks.pop(0)
        self.master_pipes[task_manager].send(["execute_task", prior_task.name, prior_task.command])

    def set_task_manager_environment(self, task_manager):
        self.master_pipes[task_manager].send(["set_env", self.queued_tasks[0].task_env])  # need to add here later


if __name__ == "__main__":
    master = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_MasterServicer_to_server(Master(), master)
    master.add_insecure_port('[::]:50050')
    master.start()
    master.wait_for_termination()
