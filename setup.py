from setuptools import setup


def get_require_package():
    with open('requirement.txt') as f:
        required = f.read().splitlines()

    return required


setup(
    name="experiment-scheduler",
    py_modules=[],
    install_requires=get_require_package(),
    entry_points={
        "console_scripts": [
            "exs=experiment_scheduler.submitter.exs:main",
        ]
    },
)
