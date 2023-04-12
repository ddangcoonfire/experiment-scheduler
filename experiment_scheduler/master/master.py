"""
Master checks all task manager status and allocates jobs from user's yaml
It is designed to run on localhost while task manager usually recommended to run on another work node.
Still, running master process on remote server is possible.
"""
import ast
import os
import threading
import time
import uuid
from collections import OrderedDict
from concurrent import futures
from typing import List

import grpc
from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import Parse
from google.protobuf.json_format import ParseDict
from google.protobuf.json_format import MessageToDict

from experiment_scheduler.common.logging import get_logger, start_end_logger
from experiment_scheduler.common.settings import USER_CONFIG
from experiment_scheduler.master.grpc_master.master_pb2 import (
    AllExperimentsStatus,
    AllTasksStatus,
    ExperimentsStatus,
    ExperimentStatement,
    MasterResponse,
    TaskStatus,
    MasterTaskStatement,
    TaskLogFile,
)
from experiment_scheduler.master.grpc_master.master_pb2_grpc import (
    MasterServicer,
    add_MasterServicer_to_server,
)
from experiment_scheduler.master.process_monitor import ProcessMonitor

from experiment_scheduler.db_util.connection import initialize_db
from experiment_scheduler.db_util.task_manager import TaskManager
from experiment_scheduler.db_util.experiment import Experiment
from experiment_scheduler.db_util.task import Task
import json
import datetime


# pylint: disable=E1101
def io_logger(func):
    """
    decorator for checking master's request and response
    :param func:
    :return:
    """

    def wrapper(self, *args, **kwargs):
        self.logger.debug(f"task_id from request : {args[1].task_id}")  # request
        result = func(self, *args, **kwargs)
        self.logger.debug(f"response.status : {result.status}")
        return result

    return wrapper


class Master(MasterServicer):
    """
    As GRPC server, Master receives request from submitter.
    While dealing requests, two daemon threads run on the same process.
    one is work-queue, which used to allocate submitted job to task managers.
    The other one is resource monitor's health checking thread defined at ResourceMonitorListener
    """

    def __init__(self):
        """
        Init GrpcServer.
        """
        # [Todo] Logging required
        # [TODO] need discussion about path and env vars
        self.queued_tasks = OrderedDict()
        self.running_tasks = OrderedDict()
        self.task_managers_address: list = self.get_task_managers()
        self.process_monitor = ProcessMonitor(self.task_managers_address)
        self.runner_thread = threading.Thread(target=self._execute_command, daemon=True)
        self.runner_thread.start()
        self.logger = get_logger(name="master class")

    @staticmethod
    def get_task_managers() -> List[str]:
        """
        Get Task Manager's address from experiment_scheduler.cfg
        :return: list of address
        """
        address_string = os.getenv("EXS_TASK_MANAGER_ADDRESS", None)
        if address_string is not None:
            address = address_string.split(" ")
        else:
            address = ast.literal_eval(
                USER_CONFIG.get("default", "task_manager_address")
            )
        for idx, task_manager in enumerate(address):
            TaskManager.insert(TaskManager(id="tm_" + str(idx), address=task_manager))
        return address

    def _execute_command(self, interval=1) -> None:
        """
        this thread_running_function periodically checks queued_task and available task_managers.
        If a task exists and available task manager exists, toss command to Process Monitor
        :param interval: time interval
        :return: None
        """
        while True:
            queue_task = Task.get(status=TaskStatus.Status.NOTSTART, order_by=Task.last_updated_date)
            if queue_task != None:
                available_task_managers = (
                    self.process_monitor.get_available_task_managers()
                )
                if available_task_managers:
                    task_manager_address = available_task_managers[0]
                    task_manager = TaskManager.get(address = task_manager_address)
                    self.execute_task(task_manager.address, queue_task.id)
            time.sleep(interval)

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

    @start_end_logger
    def request_experiments(self, request, context):
        """
        [TODO] add docstring
        :param request:
        :param context:
        :return:
        """
        experiment_id = request.name + "-" + str(uuid.uuid1())
        self.logger.info("create new experiment_id: %s", experiment_id)
        exp = Experiment(
            id=experiment_id,
            name=request.name,
            status=ExperimentStatement.Status.RUNNING,
            tasks=[],
        )
        for task in request.tasks:
            task_id = task.name + "-" + uuid.uuid4().hex
            self.logger.info(
                "├─task_id: %s", task_id
            )  # [FIXME] : set to logging pylint: disable=W0511
            # self.queued_tasks[task_id] = task
            task = Task(
                id=task_id,
                name=task.name,
                status=TaskStatus.Status.NOTSTART,
                task_env=os.environ.copy(),
                logfile_name=task_id + "_log.txt",
                command=task.command,
            )
            exp.tasks.append(task)
        response_status = MasterResponse.ResponseStatus  # pylint: disable=E1101
        response = (
            response_status.SUCCESS
            if experiment_id is not None
            else response_status.FAIL
        )
        # [todo] add task_id
        Experiment.insert(exp)
        return MasterResponse(experiment_id=experiment_id, response=response)

    @start_end_logger
    def get_task_status(self, request, context):
        """
        get status certain task
        :param request:
        :param context:
        :return: task's status
        """
        task = Task.get(id=request.task_id)
        if task == None:
            response = self._wrap_by_task_status(
                request.task_id, TaskStatus.Status.NOTFOUND
            )
        else:
            response = self._wrap_by_task_status(
                task.id, task.status
            )
        return response

    @start_end_logger
    def get_task_log(self, request, context):
        """
        get log certain task
        :param request:
        :param context:
        :return: log_file which is byte format and sent by streaming
        """
        task = Task.get(id=request.task_id)
        task_manager = TaskManager.get(id=task.task_manager_id)

        task_manager_address = task_manager.address
        task_logfile_path = task_manager.log_file_path
        if task_logfile_path == "":
            yield TaskLogFile(
                log_file=None, error_message=bytes("Check task id", "utf-8")
            )
        else:
            for response in self.process_monitor.get_task_log(
                task_manager_address, request.task_id, task_logfile_path
            ):
                yield response

    @start_end_logger
    def kill_task(self, request, context):
        """
        delete certain task
        :param request:
        :param context:
        :return: task's status
        """
        task = Task.get(id=request.task_id)
        response = None
        if task == None:
            response = self._wrap_by_task_status(
                request.task_id, TaskStatus.Status.NOTFOUND
            )
        elif task.status == TaskStatus.Status.NOTSTART or task.task_manager_id == None:
            # del self.queued_tasks[request.task_id]  # task.status = NOTSTART
            response = self._wrap_by_task_status(
                request.task_id, TaskStatus.Status.KILLED
            )
            task.status = TaskStatus.Status.KILLED
            task.commit()
        elif task.status == TaskStatus.Status.RUNNING: ### 여기
            # del self.running_tasks[request.task_id]
            task_manager = TaskManager.get(id=task.task_manager_id)
            response = self.process_monitor.kill_task(
                task_manager.address, task.id
            )
            task.status = TaskStatus.Status.KILLED
            task.commit()
        elif task.status == TaskStatus.Status.DONE:
            response = self._wrap_by_task_status(
                request.task_id, TaskStatus.Status.DONE
            )
        return response

    @start_end_logger
    def get_all_tasks(self, request, context):

        """
        get all tasks status
        :param request:
        :param context:
        :return: task's status
        """
        all_experiments_status = AllExperimentsStatus()

        if request.experiment_id:
            all_tasks_status = AllTasksStatus()
            exp = Experiment.get(id = request.experiment_id)
            for task in exp.tasks:
                all_tasks_status.task_status_array.append(
                    self._wrap_by_task_status(
                        task.id, task.status
                    )
                )
            all_experiments_status.experiment_status_array.append(
                ExperimentsStatus(
                    experiment_id=request.experiment_id,
                    task_status_array=all_tasks_status,
                )
            )
        else:
            exp_list = Experiment.list()
            for exp in exp_list:
                all_tasks_status = AllTasksStatus()
                for task in exp.tasks:
                    all_tasks_status.task_status_array.append(
                        self._wrap_by_task_status(
                            task.id, task.status
                        )
                    )
                all_experiments_status.experiment_status_array.append(
                    ExperimentsStatus(
                        experiment_id=request.experiment_id,
                        task_status_array=all_tasks_status,
                    )
                )
        return all_experiments_status

    @start_end_logger
    def execute_task(self, task_manager_address, task_id):
        """
        run certain task
        :param task_manager:
        :param gpu_idx:
        :return: task's status
        """
        task = Task.get(id=task_id)
        task_manager = TaskManager.get(address=task_manager_address)
        response = self.process_monitor.run_task(
            task.id,
            task_manager_address,
            task.command,
            task.name,
            task.task_env,
        )
        if response.status == TaskStatus.Status.RUNNING:
            # self.running_tasks[prior_task_id] = {
            #     "task": prior_task,
            #     "task_manager": task_manager,
            # }
            task.status = TaskStatus.Status.RUNNING
            task.task_manager_id = task_manager.id
            task.commit()
        else:
            task.last_updated_date = datetime.datetime.now()
            task.commit()
        return response

    def _wrap_by_task_status(self, task_id, status):
        return TaskStatus(
            task_id=task_id,
            status=status,
        )

    @start_end_logger
    def edit_task(self, request, context):
        task_id = request.task_id
        cmd = request.cmd
        task_env = request.task_env

        ## 아직 task_manager에 도달 X
        queue_tasks = Task.list(status=TaskStatus.Status.NOTSTART)
        running_tasks = Task.list(status=TaskStatus.Status.RUNNING)
        if task_id in [task.id for task in queue_tasks]:
        # if task_id in self.queued_tasks.keys():
        #     self.queued_tasks[task_id].command = cmd
            target_task = Task.get(id=task_id)
            target_task.command = cmd
            target_task.commit()
            response = MasterResponse(
                experiment_id="0", response=MasterResponse.ResponseStatus.SUCCESS
            )
        elif task_id in [task.id for task in running_tasks]:
        # elif task_id in self.running_tasks.keys():
            target_task = Task.get(id=task_id)
            target_task_manager = TaskManager.get(id=target_task.task_manager_id)
            response = self.process_monitor.kill_task(
                target_task_manager.address, task_id
            )
            if response.status == TaskStatus.Status.KILLED:
                # del self.running_tasks[task_id]
                # self.queued_tasks[task_id] = MasterTaskStatement(
                #     name=task_id.split("-")[0], command=cmd, task_env=dict(task_env)
                # )
                target_task.status = TaskStatus.Status.NOTSTART
                target_task.task_env = os.environ.copy()
                target_task.command = cmd
                target_task.commit()

            response = MasterResponse(
                experiment_id="0",
                response=MasterResponse.ResponseStatus.SUCCESS,  # pylint: disable=E1101
            )

        else:
            self.logger.warning("Task to edit isn't running or waiting to run.")
            response = MasterResponse(
                experiment_id="0",
                response=MasterResponse.ResponseStatus.FAIL,  # pylint: disable=E1101
            )

        return response


def serve():
    """
    Run Master Server with try, catch.
    If an anomaly action erupt, kill process monitor before close master object
    :return: None
    """
    initialize_db()
    with futures.ThreadPoolExecutor(max_workers=10) as pool:
        master = grpc.server(pool)
        master_address = ast.literal_eval(USER_CONFIG.get("default", "master_address"))
        add_MasterServicer_to_server(Master(), master)
        master.add_insecure_port(master_address)
        master.start()
        master.wait_for_termination()
        print("Keyboard interrupt occurs. Now closing...")


if __name__ == "__main__":
    serve()
# pylint: enable=E1101
