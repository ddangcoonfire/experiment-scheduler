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
from concurrent import futures
from typing import List
import datetime
import configparser
import grpc

from experiment_scheduler.common.logging import get_logger, start_end_logger
from experiment_scheduler.common.settings import USER_CONFIG
from experiment_scheduler.master.grpc_master.master_pb2 import (
    AllExperimentsStatus,
    AllTasksStatus,
    ExperimentsStatus,
    ExperimentStatement,
    MasterResponse,
    TaskStatus,
    TaskLogFile,
    TaskList,
    RequestAbnormalExitedTasksResponse,
    MasterFileUploadResponse,
    MasterFileDeleteResponse,
)
from experiment_scheduler.master.grpc_master.master_pb2_grpc import (
    MasterServicer,
    add_MasterServicer_to_server,
)
from experiment_scheduler.master.process_monitor import ProcessMonitor

from experiment_scheduler.db_util.connection import initialize_db
from experiment_scheduler.db_util.task_manager import TaskManager as TaskManagerEntity
from experiment_scheduler.db_util.experiment import Experiment as ExperimentEntity
from experiment_scheduler.db_util.task import Task as TaskEntity


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
        self.task_managers_address: list = self.get_task_managers()
        self.retry_task_list = []
        self.logger = get_logger(name="master class")
        self.process_monitor = ProcessMonitor(self.task_managers_address)
        self.runner_thread = threading.Thread(target=self._execute_command, daemon=True)
        self.runner_thread.start()
        self.health_check_thread = threading.Thread(
            target=self._health_check, daemon=True
        )
        self.health_check_thread.start()

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
            TaskManagerEntity.insert(
                TaskManagerEntity(id="tm_" + str(idx), address=task_manager)
            )
        return address

    def _health_check(self, interval=1) -> None:
        """
        This thread_running_function periodically checks status and tasks of task_manager
        If some task managers are abnormal, tasks of the abnormal task manager are retried
        :param interval: time interval
        :return: None
        """
        while True:
            self.logger.info("health check start")
            if self.process_monitor.selected_task_manager != -1:
                unhealthy_task_manager_list = []
                for task_manager in self.task_managers_address:
                    if not self.process_monitor.thread_queue[
                        f"is_{task_manager}_healthy"
                    ]:
                        unhealthy_task_manager_list.append(task_manager)
                if len(unhealthy_task_manager_list) > 0:
                    for unhealthy_task_manager in unhealthy_task_manager_list:
                        self._retry_execute_task(unhealthy_task_manager)
            time.sleep(interval)

    def _execute_command(self, interval=1) -> None:
        """
        this thread_running_function periodically checks queued_task and available task_managers.
        If a task exists and available task manager exists, toss command to Process Monitor
        :param interval: time interval
        :return: None
        """
        while True:
            if len(self.retry_task_list) == 0:
                queue_task = TaskEntity.get(
                    status=TaskStatus.Status.NOTSTART, order_by=TaskEntity.updated_at
                )
                if queue_task is not None:
                    self._allocate_task(queue_task)
            else:
                self._allocate_task(self.retry_task_list.pop(0), retry=True)
            time.sleep(interval)

    def _allocate_task(self, task, retry=False):
        """
        Task is assigned to available task manager
        :param task: task instance
        :param retry: boolean
        :return: None
        """
        available_task_managers = self.process_monitor.get_available_task_managers()
        if available_task_managers:
            task_manager_address = available_task_managers[0]
            task_manager = TaskManagerEntity.get(address=task_manager_address)
            self.execute_task(task_manager.address, task.id)
        elif retry:
            if task not in self.retry_task_list:
                self.retry_task_list.insert(0, task)

    def _retry_execute_task(self, unhealthy_task_manager):
        """
        Get tasks which is assigned to abnormal task manager and
        allocate tasks to another normal task manager again.
        :param: unhealthy_task_manager instance
        """
        task_manager = TaskManagerEntity.get(address=unhealthy_task_manager)
        task_list = TaskEntity.list(
            status=TaskStatus.Status.RUNNING, task_manager_id=task_manager.id
        )
        for task in task_list:
            self._allocate_task(task, retry=True)

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
        exp = ExperimentEntity(
            id=experiment_id,
            name=request.name,
            status=ExperimentStatement.Status.RUNNING,
            tasks=[],
        )
        for task in request.tasks:
            task_id = task.name + "-" + uuid.uuid4().hex
            task_env = {  # pylint: disable=R1721
                key: val for key, val in task.task_env.items()
            }

            self.logger.info(
                "├─task_id: %s", task_id
            )  # [FIXME] : set to logging pylint: disable=W0511

            task = TaskEntity(
                id=task_id,
                name=task.name,
                status=TaskStatus.Status.NOTSTART,
                task_env=task_env,
                logfile_name=task_id + "_log.txt",
                command=task.command,
                files=",".join(task.files),
                cwd=task.cwd,
            )
            exp.tasks.append(task)
        response_status = MasterResponse.ResponseStatus  # pylint: disable=E1101
        response = (
            response_status.SUCCESS
            if experiment_id is not None
            else response_status.FAIL
        )
        # [todo] add task_id
        # [TODO] Add exception for failed state while requesting experiment.
        ExperimentEntity.insert(exp)
        return MasterResponse(experiment_id=experiment_id, response=response)

    @start_end_logger
    def request_abnormal_exited_tasks(self, request, context):
        """Request to run abnormally exited task again."""
        task_list = request.task_list
        failed_list = TaskList()
        running_tasks = TaskEntity.list(
            status=TaskStatus.Status.RUNNING, order_by=TaskEntity.updated_at
        )
        running_tasks = {each_task.id: each_task for each_task in running_tasks}
        for task_class in task_list:
            if task_class.task_id in running_tasks:
                task_to_rerun = running_tasks[task_class.task_id]
                task_to_rerun.status = TaskStatus.Status.NOTSTART
                task_to_rerun.updated_at = datetime.datetime.now()
                task_to_rerun.commit()
            else:
                self.logger.warning(
                    "├─abnormal exited task_id is not running: %s", task_class.task_id
                )
                failed_list.task_list.append(task_class)

        if not failed_list.task_list:
            response = RequestAbnormalExitedTasksResponse.ResponseStatus.SUCCESS
        else:
            response = RequestAbnormalExitedTasksResponse.ResponseStatus.FAIL
        return RequestAbnormalExitedTasksResponse(
            response=response, not_running_tasks=failed_list
        )

    @start_end_logger
    def get_task_status(self, request, context):
        """
        get status certain task
        :param request:
        :param context:
        :return: task's status
        """
        task = TaskEntity.get(id=request.task_id)
        if task is None:
            response = self._wrap_by_task_status(
                request.task_id, TaskStatus.Status.NOTFOUND
            )
        else:
            response = self._wrap_by_task_status(task.id, task.status)
        return response

    @start_end_logger
    def get_task_log(self, request, context):
        """
        get log certain task
        :param request:
        :param context:
        :return: log_file which is byte format and sent by streaming
        """
        task = TaskEntity.get(id=request.task_id)
        if task is None:
            yield TaskLogFile(
                log_file=None, error_message=bytes("Check task id", "utf-8")
            )
        else:
            task_manager = TaskManagerEntity.get(id=task.task_manager_id)
            task_manager_address = task_manager.address
            task_logfile_path = task_manager.log_file_path
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
        task = TaskEntity.get(id=request.task_id)
        response = None
        if task is None:
            response = self._wrap_by_task_status(
                request.task_id, TaskStatus.Status.NOTFOUND
            )
        elif task.status == TaskStatus.Status.NOTSTART or task.task_manager_id is None:
            response = self._wrap_by_task_status(
                request.task_id, TaskStatus.Status.KILLED
            )
            task.status = TaskStatus.Status.KILLED
            task.commit()
        elif task.status == TaskStatus.Status.RUNNING:
            task_manager = TaskManagerEntity.get(id=task.task_manager_id)
            response = self.process_monitor.kill_task(task_manager.address, task.id)
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
            exp = ExperimentEntity.get(id=request.experiment_id)
            for task in exp.tasks:
                all_tasks_status.task_status_array.append(
                    self._wrap_by_task_status(task.id, task.status)
                )
            all_experiments_status.experiment_status_array.append(
                ExperimentsStatus(
                    experiment_id=request.experiment_id,
                    task_status_array=all_tasks_status,
                )
            )
        else:
            exp_list = ExperimentEntity.list()
            for exp in exp_list:
                all_tasks_status = AllTasksStatus()
                for task in exp.tasks:
                    all_tasks_status.task_status_array.append(
                        self._wrap_by_task_status(task.id, task.status)
                    )
                all_experiments_status.experiment_status_array.append(
                    ExperimentsStatus(
                        experiment_id=exp.id,
                        task_status_array=all_tasks_status,
                    )
                )
        return all_experiments_status

    @start_end_logger
    def execute_task(self, task_manager_address, task_id):
        """
        run certain task
        :param task_manager_address:
        :param task_id:
        :return: task's status
        """
        task = TaskEntity.get(id=task_id)
        task_manager = TaskManagerEntity.get(address=task_manager_address)
        task_env = {  # pylint: disable=R1721
            key: val for key, val in task.task_env.items()
        }
        self.process_monitor.delete_file(task_manager_address, task.files)
        self.process_monitor.upload_file(task_manager_address, task.files)
        response = self.process_monitor.run_task(
            task.id,
            task_manager_address,
            task.command,
            task.name,
            task_env,
            task.cwd,
        )
        if response.status == TaskStatus.Status.RUNNING:
            task.status = TaskStatus.Status.RUNNING
            task.task_manager_id = task_manager.id
            task.task_env = task_env
            task.commit()
        else:
            task.updated_at = datetime.datetime.now()
            task.commit()
        return response

    @start_end_logger
    def upload_file(self, request_iterator, context):
        for request in request_iterator:
            with open(request.name, "ab+") as file_pointer:
                file_pointer.write(request.file)
        return MasterFileUploadResponse(response=MasterResponse.ResponseStatus.SUCCESS)

    def _wrap_by_task_status(self, task_id, status):
        return TaskStatus(
            task_id=task_id,
            status=status,
        )

    @start_end_logger
    def edit_task(self, request, context):
        task_id = request.task_id
        cmd = request.cmd
        task_env = {  # pylint: disable=R1721
            key: val for key, val in request.task_env.items()
        }

        queue_tasks = TaskEntity.list(status=TaskStatus.Status.NOTSTART)
        running_tasks = TaskEntity.list(status=TaskStatus.Status.RUNNING)
        if task_id in [task.id for task in queue_tasks]:
            target_task = TaskEntity.get(id=task_id)
            target_task.command = cmd
            target_task.commit()
            response = MasterResponse(
                experiment_id="0", response=MasterResponse.ResponseStatus.SUCCESS
            )
        elif task_id in [task.id for task in running_tasks]:
            target_task = TaskEntity.get(id=task_id)
            target_task_manager = TaskManagerEntity.get(id=target_task.task_manager_id)
            response = self.process_monitor.kill_task(
                target_task_manager.address, task_id
            )
            if response.status == TaskStatus.Status.KILLED:
                target_task.status = TaskStatus.Status.NOTSTART
                target_task.task_env = task_env
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

    @start_end_logger
    def delete_file(self, request, context):
        file_name = request.name
        try:
            os.remove(file_name)
        except FileNotFoundError:
            pass
        return MasterFileDeleteResponse(response=MasterResponse.ResponseStatus.SUCCESS)


def serve():
    """
    Run Master Server with try, catch.
    If an anomaly action erupt, kill process monitor before close master object
    :return: None
    """
    initialize_db()
    with futures.ThreadPoolExecutor(max_workers=10) as pool:
        master = grpc.server(pool)
        try:
            master_address = ast.literal_eval(
                USER_CONFIG.get("default", "master_address")
            )
        except configparser.NoOptionError as err:
            raise ValueError(
                "There is no option 'master_address' in experiment_scheduler.cfg. "
                + "Please fill in this option."
            ) from err

        address, port = master_address.split(":")

        if address == "localhost" and os.environ.get("EXS_DOCKER_MODE") == "true":
            master_address = ":".join(["0.0.0.0", port])

        add_MasterServicer_to_server(Master(), master)
        master.add_insecure_port(master_address)
        master.start()
        master.wait_for_termination()
        print("Keyboard interrupt occurs. Now closing...")


if __name__ == "__main__":
    serve()
# pylint: enable=E1101
