# https://wikidocs.net/78954 참조
import os
from setuptools import find_packages, setup

setup(
    name="experiment-scheduler",
    version="0.1",
    author="ddanco",
    author_email="ddancoonfire@gmail.com",
    url="https://github.com/ddangcoonfire/experiment-scheduler",
    description="For whom needs easily usable multiple-experiment environment, here's experiment-scheduler",
    long_description="Experiment-Scheduler is open-source, for automating repeated experiments.\n" +
                     "In some environments like where k8s is not supported, where you can only use is ssh servers with python, repeatedly running same experiments with different parameters would be annoying and boring.\n"+
                     "By minimum settings and minimum effort, we provide distributed multi-experiment environment without affecting your already-completed server setting.\n"+
                     "Our goal is make you only concentrate on experiment by providing easily, fastly constructable experiment tool.",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.5',
    entry_points={
        "console_scripts": [
            "exs=experiment_scheduler.submitter.exs:main",
        ]
    },
)