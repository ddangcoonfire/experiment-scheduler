"""Task class for task manager server."""
import signal
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

    def kill_process_tree(
        self,
        sig: signal.Signals = signal.SIGTERM,
        include_me: bool = True,
        timeout: Optional[int] = None,
    ):
        """Kill a process tree (including grandchildren) with signal.

        Args:
            sig: Signal to send to processes.
            include_me: Whether to include itself or not.
            timeout: How many seconds to wait processes.

        Returns:
                Which processes are gone and which ones are still alive.
        """
        children = self._process.children(recursive=True)
        if include_me:
            children.append(self._process)
        for process in children:
            try:
                process.send_signal(sig)
            except psutil.NoSuchProcess:
                pass
        gone, alive = psutil.wait_procs(children, timeout=timeout)

        return (gone, alive)

    def is_child_pid(self, pid: int):
        """Check if the process is a child of this process.

        Args:
                pid: PID of the process to check

        Returns:
                True if the pid is a pid of child of this process
        """
        return pid in self._process.children(recursive=True)
