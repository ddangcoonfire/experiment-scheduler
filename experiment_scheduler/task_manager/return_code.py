import platform
import signal


class return_code:
    """Provides return_code which is divided by OS"""

    return_code = {"RUNNING": None, "DONE": 0, "KILLED": None, "ABNORMAL": "ABNORMAL"}

    def __init__(self, **kwargs):
        super.__init__(**kwargs)

    def get_return_code(self, name):
        """Get a return_code of subprocess status"""
        if name == "KILLED":
            if platform.system() == "Windows":
                return 1
            else:
                return -signal.SIGTERM
        else:
            return self.return_code[name]
