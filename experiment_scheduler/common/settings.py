"""
Setting file for Common Experiment-Scheduler Value.
In package, these variables work like constant, but they need initial setting.
"""
import configparser
import os

import experiment_scheduler


def _set_user_config():
    """
    set cfg file object to USER_CONFIG
    :return: ConfigParser Object
    """
    parser = configparser.ConfigParser()
    config_path = os.path.join(DEFAULT_EXS_HOME, "experiment_scheduler.cfg")
    parser.read(config_path)
    print("Set configuration path to %s", config_path)
    return parser


HEADER = "\n".join(
    [
        "┌────────────────────────────────────┐",
        "│ Welcome to Experiment-Scheduler !! │",
        "└────────────────────────────────────┘",
    ]
)
DEFAULT_EXS_HOME = os.getenv("EXS_HOME", experiment_scheduler.__path__[0])
USER_CONFIG = _set_user_config()
