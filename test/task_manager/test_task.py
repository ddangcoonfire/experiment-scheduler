import pytest

from experiment_scheduler.task_manager import task
from experiment_scheduler.task_manager.task import Task


class TestTask:
    @pytest.fixture(autouse=True)
    def init(self, mocker):
        self.mock_psutil = mocker.patch.object(task, "psutil")
        self.mock_process = mocker.MagicMock()
        self.mock_psutil.Process = self.mock_process

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
        self.mock_process.wait.return_value = 0
        self.mock_process.is_runinng.return_value = False
        self.mock_process.status.return_value = 0

        task = Task(1234)

        assert task.get_return_code == 0
