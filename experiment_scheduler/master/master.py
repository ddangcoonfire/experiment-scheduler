"""
[TODO] Master Explanation

"""
from concurrent import futures
from multiprocessing import Process, Pipe
import uuid
import time
import threading
import ast
import grpc
from experiment_scheduler.master.process_monitor import ProcessMonitor
from experiment_scheduler.master.grpc_master.master_pb2_grpc import (
    MasterServicer,
    add_MasterServicer_to_server,
    MasterStub,
)
from experiment_scheduler.master.grpc_master import master_pb2
from experiment_scheduler.common import settings
from experiment_scheduler.resource_monitor.monitor import responser
from experiment_scheduler.common.settings import USER_CONFIG

def get_task_managers():
    """
    [TODO] add docstring
    :return:
    """
    return ast.literal_eval(USER_CONFIG.get("default", "task_manager_address"))


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
        # [TODO] need discussion about path and env vars
        self.queued_tasks = []
        self.master_pipes = dict()
        self.process_monitor_pipes = dict()
        self.task_managers_address = get_task_managers()
        self.process_monitor = self.create_process_monitor()
        self.resource_monitor = responser()
        self.runner = threading.Thread(target=self._execute_command, daemon=True)
        self.runner.start()

    def _execute_command(self, interval=1):
        """
        this thread_running_function periodically checks queued_task and available task_managers.
        If a task exists and available task manager exists, toss command to Process Monitor
        :param interval: time interval
        :return: None
        """
        while True:
            gpu_idx = responser.get_max_free_gpu()
            if gpu_idx != -1:
                available_task_managers = self.get_available_task_managers()
                self.resource_monitor.queued_gpu_idx.append(gpu_idx)
                for _ in self.queued_tasks:
                    if len(available_task_managers) > 0:
                        task_manager = available_task_managers.pop(0)
                        self.execute_task(task_manager, gpu_idx)
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

    def halt_process_monitor(self, request, context):
        for process in self.process_monitor:
            process.terminate()
        return master_pb2.google_dot_protobuf_dot_empty__pb2.Empty()

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
        gpu_idx = self.resource_monitor.queued_gpu_idx.pop(0)
        self.master_pipes[task_manager].send(
            [
                "run_task",
                gpu_idx,
                prior_task.command,
                prior_task.name,
                dict(prior_task.task_env),
            ]
        )

def halt_process_monitor():
    """
    kill process monitor before close master server
    process monitor can be closed through communication with master
    :return: None
    """
    stub = MasterStub(grpc.insecure_channel("localhost:50052"))
    empty = master_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
    stub.halt_process_monitor(empty)


def serve():
    """
    Run Master Server with try, catch.
    If an anomaly action erupt, kill process monitor before close master object
    :return: None
    """
    
    with futures.ThreadPoolExecutor(max_workers=10) as pool:
        master = grpc.server(pool)
        print(settings.HEADER)
        master_address = ast.literal_eval(USER_CONFIG.get("default", "master_address"))
        print("set master server to %s" % master_address)
        add_MasterServicer_to_server(Master(), master)
        master.add_insecure_port(master_address)
        try:
            master.start()
            master.wait_for_termination()
        except KeyboardInterrupt as exception:
            print("keyboardInterrupt occurred \n %s", exception)
            print("halting master immediately...")
            halt_process_monitor()
        except Exception as error_case:  # pylint: disable=broad-except
            print("Error Occurred %s", error_case)
            print("halting master immediately...")
            halt_process_monitor()


if __name__ == "__main__":
    serve()
