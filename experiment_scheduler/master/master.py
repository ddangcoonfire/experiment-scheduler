"""
Master checks all task manager status and allocates jobs from user's yaml
It is designed to run on localhost while task manager usually recommended to run on another work node.
Still, running master process on remote server is possible.
"""
from collections import OrderedDict
from concurrent import futures
import uuid
import time
import threading
import ast
from typing import List, Tuple
import logging
import grpc

from experiment_scheduler.master.process_monitor import ProcessMonitor
from experiment_scheduler.master.grpc_master.master_pb2_grpc import (
    MasterServicer,
    add_MasterServicer_to_server,
)
from experiment_scheduler.master.grpc_master import master_pb2
from experiment_scheduler.common import settings
from experiment_scheduler.common.settings import USER_CONFIG
from experiment_scheduler.resource_monitor.resource_monitor_listener import (
    ResourceMonitorListener,
)
from experiment_scheduler.task_manager.grpc_task_manager.task_manager_pb2 import (
    TaskStatus,
    AllTasksStatus
)

logger = logging.getLogger()


def get_task_managers() -> List[str]:
    """
    Get Task Manager's address from experiment_scheduler.cfg
    :return: list of address
    """
    return ast.literal_eval(USER_CONFIG.get("default", "task_manager_address"))


def get_resource_monitors() -> List[str]:
    """
    Get Resource Monitor's address from experiment_scheduler.cfg
    :return: list of address
    """
    return ast.literal_eval(USER_CONFIG.get("default", "resource_monitor_address"))


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

        self.task_managers_address: list = get_task_managers()
        self.resource_monitor_listener: ResourceMonitorListener = (
            ResourceMonitorListener(get_resource_monitors())
        )
        self.process_monitor = ProcessMonitor(self.task_managers_address)
        self.runner_thread = threading.Thread(target=self._execute_command, daemon=True)
        self.runner_thread.start()

    def _execute_command(self, interval=1) -> None:
        """
        this thread_running_function periodically checks queued_task and available task_managers.
        If a task exists and available task manager exists, toss command to Process Monitor
        :param interval: time interval
        :return: None
        """
        while True:
            available_task_managers = self._get_available_task_managers()
            if len(available_task_managers) > 0 and len(self.queued_tasks):
                task_manager, gpu_idx = available_task_managers.pop(0)
                self.execute_task(task_manager, gpu_idx)
            time.sleep(interval)

    def _get_available_task_managers(self) -> List[Tuple[str, int]]:
        """
        Get available task manager from resource monitor.
        Currently, it only checks if task manager has available gpu.
        :return: list of available task manager address
        """
        # currently only return first one
        available_task_managers = []
        for task_manager, resource_monitor in zip(
                self.task_managers_address,
                self.resource_monitor_listener.resource_monitor_address,
        ):
            runnable, gpu_idx = self._check_task_manager_run_task_available(
                resource_monitor
            )
            if runnable:
                available_task_managers.append((task_manager, gpu_idx))
        # return available_task_managers
        return available_task_managers
        # return tuple([self.task_managers_address[0], gpu_idx])

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
        print(
            "experiment_id:", experiment_id
        )  # [FIXME] : set to logging pylint: disable=W0511
        for task in request.tasks:
            task_id = task.name + "-" + uuid.uuid4().hex
            print("task_id:", task_id)  # [FIXME] : set to logging pylint: disable=W0511
            self.queued_tasks[task_id] = task
        response_status = (
            master_pb2.MasterResponse.ResponseStatus  # pylint: disable=E1101
        )
        response = (
            response_status.SUCCESS
            if experiment_id is not None
            else response_status.FAIL
        )
        print("waitted tasks keys:", self.queued_tasks.keys())
        print("running tasks keys:", self.running_tasks.keys())
        return master_pb2.MasterResponse(experiment_id=experiment_id, response=response)

    def get_task_status(self, request, context):
        """
        get status certain task
        :param request:
        :param context:
        :return: task's status
        """
        if request.task_id in dict(self.queued_tasks).keys():
            response = self._wrap_by_task_status(
                request.task_id, TaskStatus.Status.NOTSTART
            )
        elif request.task_id in dict(self.running_tasks).keys():
            print('running task!')
            response = self.process_monitor.get_task_status(
                self.running_tasks[request.task_id]["task_manager"], request.task_id
            )
            if response.status == TaskStatus.Status.KILLED:
                del self.running_tasks[request.task_id]
        else:
            response = self._wrap_by_task_status(
                request.task_id, TaskStatus.Status.NOTFOUND
            )
        return response

    def get_task_log(self, request, context):
        """
        get log certain task
        :param request:
        :param context:
        :return: log path
        """
        if request.task_id in dict(self.queued_tasks).keys():
            response = self._wrap_by_task_status(
                request.task_id, TaskStatus.Status.NOTSTART
            )
        elif request.task_id in dict(self.running_tasks).keys():
            response = self.process_monitor.get_task_log(
                self.running_tasks[request.task_id]["task_manager"], request.task_id
            )
            if response.status == TaskStatus.Status.KILLED:
                del self.running_tasks[request.task_id]
        else:
            response = self._wrap_by_task_status(
                request.task_id, TaskStatus.Status.NOTFOUND
            )
        return response

    def kill_task(self, request, context):
        """
        delete certain task
        :param request:
        :param context:
        :return: task's status
        """
        if request.task_id in dict(self.queued_tasks).keys():
            del self.queued_tasks[request.task_id]
            response = self._wrap_by_task_status(
                request.task_id, TaskStatus.Status.KILLED
            )
        elif request.task_id in dict(self.running_tasks).keys():
            response = self.process_monitor.kill_task(
                self.running_tasks[request.task_id]["task_manager"], request.task_id
            )
            if response.status == TaskStatus.Status.KILLED:
                del self.running_tasks[request.task_id]
        else:
            response = self._wrap_by_task_status(
                request.task_id, TaskStatus.Status.NOTFOUND
            )
        return response

    def get_all_tasks(self, request, context):

        """
        get all tasks status
        :param request:
        :param context:
        :return: task's status
        """
        response = self.process_monitor.get_all_tasks()
        for tasks in self.queued_tasks:
            response.task_status_array.append(
                self._wrap_by_task_status(
                    task_id=tasks.task_id,
                    status=TaskStatus.Status.NOTSTART
                )
            )
        if response is None:
            print("there is no task")
        return response

    def execute_task(self, task_manager, gpu_idx):
        """
        run certain task
        :param task_manager:
        :param gpu_idx:
        :return: task's status
        """
        prior_task_id, prior_task = self.queued_tasks.popitem(last=False)
        self.running_tasks[prior_task_id] = {
            "task": prior_task,
            "task_manager": task_manager,
            "gpu_idx": gpu_idx,
        }
        response = self.process_monitor.run_task(
            prior_task_id,
            task_manager,
            gpu_idx,
            prior_task.command,
            prior_task.name,
            dict(prior_task.task_env),
        )
        if response.status == TaskStatus.Status.RUNNING:
            self.running_tasks[prior_task_id] = {'task': prior_task, 'task_manager': task_manager}
        return response

    def _check_task_manager_run_task_available(  # pylint: disable=unused-argument,no-self-use
            self, resource_monitor
    ):
        """
        [TODO] add docstring
        :param task_manager:
        :param resource_monitor:
        :return:
        """
        # currently only checks gpu availability.
        gpu_idx = self.resource_monitor_listener.get_available_gpu_idx(resource_monitor)
        available = gpu_idx != -1
        # currently only returns True
        return available, gpu_idx

    def _wrap_by_task_status(self, task_id, status):
        return master_pb2.TaskStatus(
            task_id=task_id,
            status=status,
        )


def serve():
    """
    Run Master Server with try, catch.
    If an anomaly action erupt, kill process monitor before close master object
    :return: None
    """

    with futures.ThreadPoolExecutor(max_workers=10) as pool:
        master = grpc.server(pool)
        logger.info(settings.HEADER)
        master_address = ast.literal_eval(USER_CONFIG.get("default", "master_address"))
        logger.info("set master server to %s", master_address)
        add_MasterServicer_to_server(Master(), master)
        master.add_insecure_port(master_address)
        try:
            master.start()
            master.wait_for_termination()
        except KeyboardInterrupt as exception:
            logger.info("keyboardInterrupt occurred \n %s", exception)
            logger.info("halting master immediately...")
        except Exception as error_case:  # pylint: disable=broad-except
            logger.info("Error Occurred %s", error_case)
            logger.info("halting master immediately...")


if __name__ == "__main__":
    serve()
