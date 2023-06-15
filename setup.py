from setuptools import setup

def get_require_package():
    with open('requirement.txt') as f:
        required = f.read().splitlines()

    return required




setup(
    version="1.1",
    description="For whom needs easily usable multiple-experiment environment, here's experiment-scheduler",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    name="experiment-scheduler",
    py_modules=[],
    install_requires=get_require_package(),
    entry_points={
        "console_scripts": [
            "exs=experiment_scheduler.submitter.exs:main",
        ]
    },
    project_urls = {
        "repository": "https://github.com/ddangcoonfire/experiment-scheduler.git"
    }
)
