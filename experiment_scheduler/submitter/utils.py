import re
import subprocess
from copy import deepcopy
from itertools import product
from os import path as osp
from typing import Any, Dict, List, Union

import yaml


def wrap_by_list(value):
    if isinstance(value, (list, tuple)):
        return value
    else:
        return [value]


class YamlParser:
    def __init__(self, file_path: str):
        self._file_path = file_path

    @property
    def file_path(self):
        return self._file_path

    def parse(self):
        loaded_yaml = self._load_yaml()
        parsed_yaml = self._apply_extended_syntax(loaded_yaml)

        return parsed_yaml

    def _load_yaml(self):
        with open(self._file_path, "r") as f:
            parsed_yaml = yaml.safe_load(f)

        return parsed_yaml

    def _apply_extended_syntax(self, loaded_yaml: Dict[str, Any]):
        if "tasks" not in loaded_yaml:
            return loaded_yaml

        tasks = []
        loaded_yaml["tasks"] = wrap_by_list(loaded_yaml["tasks"])
        for task in loaded_yaml["tasks"]:
            task = self._apply_arguments(task)
            task = self._apply_repitition(task)

            if isinstance(task, list):
                tasks.extend(task)
            else:
                tasks.append(task)

        loaded_yaml["tasks"] = tasks

        return loaded_yaml

    def _apply_arguments(self, tasks: Union[Dict, List[Dict]]):
        tasks = wrap_by_list(tasks)
        parsed_tasks = []

        for task in tasks:
            arguments = task.get("arguments", None)
            if arguments is not None:
                for arg_comb in self._get_arguments_combinations(arguments.values()):
                    arguments_applied_task = deepcopy(task)
                    for arg_key, arg_val in zip(arguments.keys(), arg_comb):
                        arguments_applied_task["cmd"] = re.sub(
                            rf"{{{{ {arg_key} }}}}",
                            str(arg_val),
                            arguments_applied_task["cmd"],
                        )
                        arguments_applied_task["name"] += f"_{arg_key}_{arg_val}"

                    parsed_tasks.append(arguments_applied_task)
            else:
                parsed_tasks.append(task)

        return parsed_tasks

    def _get_arguments_combinations(self, arguments_value: Any):
        arguments_value = wrap_by_list(arguments_value)
        return product(*arguments_value)

    def _apply_repitition(self, tasks: Union[Dict, List[Dict]]):
        tasks = wrap_by_list(tasks)

        parsed_tasks = []
        for task in tasks:
            repitition = task.get("repitition", None)
            if repitition is not None:
                for i in range(1, repitition + 1):
                    arguments_applied_task = deepcopy(task)
                    arguments_applied_task["name"] += f"_repit{i}"
                    parsed_tasks.append(arguments_applied_task)
            else:
                parsed_tasks.append(task)

        return parsed_tasks
