from unittest.mock import MagicMock
import psutil
import pytest
import signal

from experiment_scheduler.task_manager import task
from experiment_scheduler.task_manager.task import Task


class MockProcess:
    mock_instance = MagicMock()

    def __init__(self, pid):
        self.pid = pid
        # self.mock_instance = MagicMock()

    def __getattr__(self, name):
        if name == "__setstate__":
            raise AttributeError(name)
        return getattr(self.mock_instance, name)


@pytest.fixture(autouse=True)
def init_mockprocess_mock_instance():
    MockProcess.mock_instance = MagicMock()


class TestTask:
    @pytest.fixture(autouse=True)
    def init(self, mocker):
        self.mock_psutil = mocker.patch.object(task, "psutil")
        self.mock_psutil.Process = MockProcess

    def test_init(self):
        Task(1234)

    def test_init_wrong_pid(self):
        with pytest.raises(ValueError):
            Task(-1)

    def test_pid(self):
        pid = 1234
        task_cls = Task(pid)

        assert task_cls.pid == pid

    def test_get_return_code(self):
        return_code = 12
        MockProcess.mock_instance.wait.return_value = return_code
        MockProcess.mock_instance.is_running.return_value = False
        MockProcess.mock_instance.status.return_value = 0

        task = Task(1234)

        assert task.get_return_code() == return_code

    def test_get_return_code_runnigng_task(self):
        MockProcess.mock_instance.is_running.return_value = True
        MockProcess.mock_instance.status.return_value = 0

        task = Task(1234)

        assert task.get_return_code() is None

    def test_get_return_code_zombie_status(self):
        return_code = 12
        MockProcess.mock_instance.wait.return_value = return_code
        self.mock_psutil.STATUS_ZOMBIE = psutil.STATUS_ZOMBIE
        MockProcess.mock_instance.is_running.return_value = True
        MockProcess.mock_instance.status.return_value = psutil.STATUS_ZOMBIE

        task = Task(1234)

        assert task.get_return_code() == return_code

    def test_register_progress(self):
        task = Task(1234)
        progress = 30
        
        task.register_progress(progress, 12.3)

        assert task.get_progress() == progress

    def test_get_progress_not_registered(self, mocker):
        self.mock_psutil.wait_procs.return_value = ([], [])
        child_p1 = mocker.MagicMock()
        child_p2 = mocker.MagicMock()
        MockProcess.mock_instance.children.return_value = [child_p1, child_p2]
        mock_singal = mocker.MagicMock()
        task = Task(1234)

        task.kill_process_tree(sig=mock_singal)

        assert child_p1.send_signal.called_once_with(mock_singal)

    @pytest.fixture
    def children_processes(self, mocker):
        child_p1 = mocker.MagicMock()
        child_p1.pid = 1
        child_p2 = mocker.MagicMock()
        child_p2.pid = 2
        MockProcess.mock_instance.children.return_value = [child_p1, child_p2]

        return [child_p1, child_p2]

    def test_kill_process_tree(self, children_processes):
        task = Task(1234)
        self.mock_psutil.wait_procs.return_value = ("gone", "alive")
        timeout = 3

        gone, alive = task.kill_process_tree(sig=signal.SIGINT, include_me=True, timeout=timeout)

        assert gone == "gone"
        assert alive == "alive"
        self.mock_psutil.wait_procs.assert_called_once()
        wait_procs_args = self.mock_psutil.wait_procs.call_args
        assert wait_procs_args.kwargs["timeout"] == timeout
        for child_process in children_processes:
            child_process.send_signal.assert_called_once_with(signal.SIGINT)
            assert child_process in wait_procs_args[0][0]
        task._process.send_signal.assert_called_once_with(signal.SIGINT)

    def test_kill_process_tree(self, children_processes):
        task = Task(1234)
        self.mock_psutil.wait_procs.return_value = ("gone", "alive")
        timeout = 3

        task.kill_process_tree(include_me=False, timeout=timeout)
        task._process.send_signal.assert_not_called()

    def test_is_child_pid(self, children_processes):
        task = Task(1234)

        assert task.is_child_pid(1)

    def test_is_not_child_pid(self, children_processes):
        task = Task(1234)

        assert not task.is_child_pid(3)
