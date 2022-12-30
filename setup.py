from setuptools import setup

setup(
    name="experiment-scheduler",
    py_modules=[],
    entry_points={
        "console_scripts": [
            "exs=experiment_scheduler.submitter.exs:main",
        ]
    },
)
