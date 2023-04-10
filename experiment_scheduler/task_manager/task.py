"""Task class for task manager server."""
from typing import Dict, List, Optional, Union

import psutil

from experiment_scheduler.common.logging import get_logger

logger = get_logger(name="task_manger.task")


class Task:
    """Task class which includes helpful functions to task manager server."""

    def __init__(self, pid: int):
        self._process = psutil.Process(pid)
        self._history: List[Dict[str, float]] = []

    @property
    def pid(self):
        """Get pid."""
        return self._process.pid

    def get_return_code(self) -> Optional[int]:
        """Get the return code of the process if it is done.

        Returns:
                The return code or None if the process is running
        """
        if self._process.is_running():
            return None
        return self._process.wait()

    def register_progress(self, progress: Union[int, float], leap_second: float):
        """Register progress."""
        self._history.append({"progress": progress, "leap_second": leap_second})

    def get_progress(self) -> Optional[Union[int, float]]:
        """Get latest progress."""
        if self._history:
            return self._history[-1]["progress"]
        return None

    def kill_itself_with_child_process(self, max_depth: int) -> bool:
        """
        Kill itself with child process.
        This is equivalent to calling kill_process_recursively up to max_depth and then returning True if successful.

        Args:
                max_depth: Maximum depth of child processes to find and kill.

        Returns:
                True if successful False otherwise.
        """
        if self._process is None:
            logger.warning("Fail to get process(%d).", self._pid)
            return False
        return self.kill_process_recursively(self._process, max_depth, 0)

    @staticmethod
    def kill_process_recursively(
        process: psutil.Process, max_depth: int, cur_depth: int = 0
    ) -> bool:
        """Kill process recursively up to max_depth.

        Args:
                process: Process to be killed.
                max_depth: Maximum depth of child processes to find and kill.
                cur_depth: Current depth of child processes. Default is 0

        Returns:
                True if process was killed
        """
        if not process.is_running():
            return True

        if cur_depth < max_depth:
            for child_process in process.children():
                Task.kill_process_recursively(child_process, max_depth, cur_depth + 1)

        if process.is_running():
            process.terminate()
            process.wait()

        return True

    def is_child_pid(self, pid: int):
        """Check if the process is a child of this process.

        Args:
                pid: PID of the process to check

        Returns:
                True if the pid is a pid of child of this process
        """
        return pid in self._process.children(recursive=True)
