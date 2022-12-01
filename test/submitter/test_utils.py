import pytest
import yaml
import uuid
from os import path as osp

from experiment_scheduler.submitter.utils import wrap_by_list, YamlParser


@pytest.fixture
def ordinary_yaml_format():
    yaml_format = {
        "name": "test",
        "resource": 1,
        "tasks": [
            {"name": "test0", "cmd": "run train", "condition": {"gpu": 1}},
            {
                "name": "test1",
                "cmd": "run train",
            },
            {"name": "test2", "cmd": "run train", "condition": {"gpu": 2}},
        ],
    }
    return yaml_format


@pytest.fixture
def extended_argument_task_format():
    task = {
        "name": "argument_extended",
        "cmd": "torch train --lr {{ lr }} --bs {{ bs }}",
        "arguments": {"lr": [0.1, 0.2], "bs": [4, 8]},
        "condition": {"gpu": 1},
    }

    return task


@pytest.fixture
def expected_extended_argument_task_format():
    extended_task = [
        {
            "name": "argument_extended",
            "cmd": "torch train --lr 0.1 --bs 4",
            "condition": {"gpu": 1},
        },
        {
            "name": "argument_extended",
            "cmd": "torch train --lr 0.2 --bs 4",
            "condition": {"gpu": 1},
        },
        {
            "name": "argument_extended",
            "cmd": "torch train --lr 0.1 --bs 8",
            "condition": {"gpu": 1},
        },
        {
            "name": "argument_extended",
            "cmd": "torch train --lr 0.2 --bs 8",
            "condition": {"gpu": 1},
        },
    ]

    return extended_task


def get_random_yaml_file_name():
    return f"{uuid.uuid4().hex}.yaml"


def save_yaml_file(yaml_format, yaml_file_dir):
    yaml_file_path = osp.join(yaml_file_dir, get_random_yaml_file_name())
    with open(yaml_file_path, "w") as f:
        yaml.dump(yaml_format, f)

    return yaml_file_path


@pytest.fixture(scope="session")
def yaml_file_dir(tmp_path_factory):
    yaml_file_dir = tmp_path_factory.mktemp("yaml_files")
    return yaml_file_dir


@pytest.mark.parametrize("value", [(1, 2), [1, 2]])
def test_wrap_list_by_list(value):
    ret = wrap_by_list(value)
    assert ret == value


@pytest.mark.parametrize("value", [1, "a", {1: 2, 3: 4}])
def test_wrap_not_list_by_list(value):
    ret = wrap_by_list(value)
    assert ret == [value]


class TestYamlParser:
    def test_parse_ordinary_yaml(self, yaml_file_dir, ordinary_yaml_format):
        yaml_file_path = save_yaml_file(ordinary_yaml_format, yaml_file_dir)
        ret = YamlParser(yaml_file_path).parse()
        assert ordinary_yaml_format == ret

    @pytest.mark.skip
    def test_parse_ytt_format(self, yaml_file_dir):
        pass

    @pytest.mark.skip
    def test_parse_ytt_format_wrong_format(self, yaml_file_dir):
        pass

    def test_parse_yaml_extended_arguments(
        self,
        yaml_file_dir,
        ordinary_yaml_format,
        extended_argument_task_format,
        expected_extended_argument_task_format,
    ):
        extended_yaml_format = ordinary_yaml_format
        extended_yaml_format["tasks"] = extended_argument_task_format
        yaml_file_path = save_yaml_file(extended_yaml_format, yaml_file_dir)

        parsed_yaml = YamlParser(yaml_file_path).parse()
        cmds = [task["cmd"] for task in expected_extended_argument_task_format]
        for task in parsed_yaml["tasks"]:
            assert task["cmd"] in cmds

    def test_parse_yaml_extended_arguments_wrong_format(self, yaml_file_dir):
        pass

    def test_parse_yaml_extended_repeat(self, yaml_file_dir):
        pass

    def test_parse_yaml_extended_repeat_wrong_format(self, yaml_file_dir):
        pass
