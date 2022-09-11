"""
[TODO] Master Explanation

"""
from concurrent import futures
from multiprocessing import Process, Pipe
import uuid
import time
import threading
import configparser
import os
import ast
import grpc
from experiment_scheduler.master.process_monitor import ProcessMonitor
from experiment_scheduler.master.grpc_master.master_pb2_grpc import (
    MasterServicer,
    add_MasterServicer_to_server,
)
from experiment_scheduler.master.grpc_master import master_pb2
from experiment_scheduler.common import settings


class Master(MasterServicer):
    """
    Inherit GrpcServer to run Grpc Socket ( get request from submitter )
    Class that runs on server
    """

    def __init__(self):
        """
        Init GrpcServer.
        """
        # [Todo] Logging required
        self.conf = configparser.ConfigParser()
        self.conf.read(
            os.path.join(os.getenv("EXS_HOME", ""), "experiment_scheduler.cfg")
        )
        # [TODO] need discussion about path and env vars
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
            for _ in self.queued_tasks:
                if len(available_task_managers) > 0:
                    task_manager = available_task_managers.pop(0)
                    self.execute_task(task_manager)
            # [TODO] master pipe recv logic required here
            for task_manager, pipe in self.master_pipes.items():
                if pipe.poll():
                    print(pipe.recv())  # need change later
            time.sleep(interval)

    def _run_process_monitor(  # pylint: disable=no-self-use
        self, task_manager_address, pipe
    ):
        """
        Create Process Monitor process per task manager
        :param task_manager_address:
        :param pipe:
        :return:
        """
        process_monitor = ProcessMonitor(task_manager_address, pipe)
        process_monitor.start()

    def _process_monitor_termintion(self):
        # [TODO] all process monitors should be halted if master stopped
        pass

    def create_process_monitor(self):
        """
        [TODO] add docstring
        :return:
        """
        print("create process monitor")  # print should be replaced as log later
        process_monitor_list = list()
        for task_manager in self.task_managers_address:
            (
                self.master_pipes[task_manager],
                self.process_monitor_pipes[task_manager],
            ) = Pipe()
            process_monitor = Process(
                target=self._run_process_monitor,
                args=(task_manager, self.process_monitor_pipes[task_manager]),
            )
            process_monitor_list.append(process_monitor)
            process_monitor.start()
        return process_monitor_list

    def get_task_managers(self):
        """
        [TODO] add docstring
        :return:
        """
        return ast.literal_eval(self.conf.get("default", "task_manager_address"))

    def select_task_manager(self, selected=-1):
        """
        Process Monitor automatically provide task that is able to run task
        :return:
        """
        # [TODO] need to set convention with resource monitor later
        return (
            self.task_managers_address[0]
            if selected < 0
            else self.task_managers_address[selected]
        )

    def request_experiments(self, request, context):
        """
        [TODO] add docstring
        :param request:
        :param context:
        :return:
        """
        experiment_id = request.name + "-" + str(uuid.uuid1())
        print(experiment_id)
        for task in request.tasks:
            self.queued_tasks.append(task)
        response_status = (
            master_pb2.MasterResponse.ResponseStatus  # pylint: disable=E1101
        )
        response = (
            response_status.SUCCESS
            if experiment_id is not None
            else response_status.FAIL
        )
        return master_pb2.MasterResponse(experiment_id=experiment_id, response=response)

    def delete_experiment(self, request, context):
        """
        delete all experiments registered in a group
        :param request:
        :param context:
        :return:
        """
        pass  # pylint: disable=unnecessary-pass

    def delete_experiments(self, request, context):
        """
        delete certain experiment
        :param request:
        :param context:
        :return:
        """
        pass  # pylint: disable=unnecessary-pass

    def check_task_manager_run_task_available(  # pylint: disable=unused-argument,no-self-use
        self, task_manager
    ):
        """
        [TODO] add docstring
        :param task_manager:
        :return:
        """
        # currently only returns True
        return True

    def get_available_task_managers(self):
        """
        [TODO] add docstring
        :return:
        """
        # currently only return first one
        available_task_managers = []
        for task_manager in self.task_managers_address[0]:
            if self.check_task_manager_run_task_available(task_manager):
                available_task_managers.append(task_manager)
        # return available_task_managers
        return [self.task_managers_address[0]]

    def execute_task(self, task_manager):
        """
        [TODO] add docstring
        :param task_manager:
        :return:
        """
        prior_task = self.queued_tasks.pop(0)
        gpu_idx = 0  # need to get idx from Resource Monitor
        self.master_pipes[task_manager].send(
            [
                "run_task",
                gpu_idx,
                prior_task.command,
                prior_task.name,
                dict(prior_task.task_env),
            ]
        )


def serve():
    """
    [TODO] add docstring
    :return:
    """
    print(settings.HEADER)
    master = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)  # pylint: disable=E1129,R1732
    )
    add_MasterServicer_to_server(Master(), master)
    master.add_insecure_port("[::]:50052")
    master.start()
    master.wait_for_termination()


if __name__ == "__main__":
    serve()
