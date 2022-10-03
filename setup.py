import os
from setuptools import find_packages, setup

setup(
    name="experiment-scheduler",
    entry_points={
        "console_scripts": [
            "exs=experiment_scheduler.submitter.exs:main",
        ]
    },
)