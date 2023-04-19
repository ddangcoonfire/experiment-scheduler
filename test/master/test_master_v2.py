import pytest

import experiment_scheduler
from experiment_scheduler.master.grpc_master import master_pb2
from experiment_scheduler.master.grpc_master.master_pb2 import TaskStatus, Task, TaskList,MasterResponse, RequestAnomalyRequestTasksResponse
from experiment_scheduler.master import master
from experiment_scheduler.master.master import Master

from collections import OrderedDict



class TestMaster: 
    
    @pytest.fixture(autouse=True)
    def init(self, mocker):
        self.mock_thred = mocker.patch.object(master, "threading")
        self.mock_process_monitor = mocker.patch.object(master, "ProcessMonitor")
        self.master = Master()
        
    @pytest.fixture
    def insert_running_task(self):
        self.master.running_tasks.update([
            ("test0", {"task": Task(task_id = "test0"), "task_manager": "test_task_manager"}),
            ("test1", {"task": Task(task_id = "test1"), "task_manager": "test_task_manager"}),
            ("test2", {"task": Task(task_id = "test2"), "task_manager": "test_task_manager"}),
        ])


    def test_request_anomaly_exited_tasks(self, insert_running_task):
        test_request =  TaskList(task_list=[Task(task_id = "test0"), Task(task_id="test1")])
        test_return_value = self.master.request_anomaly_exited_tasks(test_request, "context")

        assert test_request.task_list[0].task_id not in self.master.running_tasks
        assert test_request.task_list[1].task_id not in self.master.running_tasks
        assert test_request.task_list[0].task_id in self.master.queued_tasks
        assert test_request.task_list[1].task_id in self.master.queued_tasks
        assert test_return_value.response == RequestAnomalyRequestTasksResponse.ResponseStatus.SUCCESS
        assert len(test_return_value.not_running_tasks.task_list) == 0


    def test_request_anomaly_exited_tasks_not_running_task(self, insert_running_task):
        test_request =  TaskList(task_list=[Task(task_id = "test0"), Task(task_id="test3")])
        test_return_value = self.master.request_anomaly_exited_tasks(test_request, "context")

        assert test_request.task_list[0].task_id not in self.master.running_tasks
        assert test_request.task_list[0].task_id in self.master.queued_tasks
        assert test_request.task_list[1].task_id not in self.master.queued_tasks
        assert test_return_value.response == RequestAnomalyRequestTasksResponse.ResponseStatus.FAIL
        assert test_request.task_list[1] in test_return_value.not_running_tasks.task_list
