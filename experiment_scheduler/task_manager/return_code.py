"""
Each OS has slightly different return code for process action.
Distinguish it through return_code.py
"""
import platform
import signal


class ReturnCode:
    """Provides return_code which is divided by OS"""

    def __init__(self):
        self.return_code = {
            "RUNNING": None,
            "DONE": 0,
            "KILLED": None,
            "ABNORMAL": "ABNORMAL",
        }

    def get_return_code(self, name):
        """Get a return_code of subprocess status"""
        if name == "KILLED":
            if platform.system() == "Windows":
                return 1
            return -signal.SIGTERM
        return self.return_code[name]
