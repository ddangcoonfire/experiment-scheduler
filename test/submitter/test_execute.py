from unittest import TestCase
from unittest.mock import patch, Mock, mock_open

import argparse

import grpc
import yaml

from experiment_scheduler.master.grpc_master import master_pb2, master_pb2_grpc
from experiment_scheduler.submitter.execute import parse_input_file
from experiment_scheduler.submitter.execute import main

import os

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), "sample.yaml")


def test_parser():
    parser = argparse.ArgumentParser(...)
    parser.add_argument("-f", "--file")
    return parser.parse_args(["-f", "sample.yaml"])


class Response:
    response = 0
    experiment_id = "test_id"

    def __init__(self, *args, **kwargs):
        pass


class MockMasterStub:
    def __init__(self, *args, **kwargs):
        pass

    def request_experiments(self, *args, **kwargs):
        return Response


class Test(TestCase):
    def test_parse_args(self):
        # when
        return_val = test_parser()

        # then
        self.assertEqual(return_val, argparse.Namespace(file="sample.yaml"))

    def test_parse_input_file(self):
        # given
        parsed_yaml = {
            "name": "test",
            "tasks": [
                {
                    "cmd": "test_cmd",
                    "name": "test_task_name",
                }
            ],
        }
        # when
        return_val = parse_input_file(parsed_yaml)

        # then
        self.assertIsInstance(return_val, master_pb2.ExperimentStatement)

    @patch("builtins.open", mock_open(read_data="sample.yaml"))
    def test_main(self):
        # given
        parse_args = Mock(side_effect=test_parser)
        yaml.load = Mock(
            return_value={
                "name": "smaple",
                "tasks": [
                    {"cmd": "torch train --lr 0.01", "name": "hpo_1"},
                    {"cmd": "torch train --lr 0.02", "name": "hpo_2"},
                ],
            }
        )
        grpc.insecure_channel = Mock()
        master_pb2_grpc.MasterStub = Mock(side_effect=MockMasterStub)

        # when
        main()

        # then
        grpc.insecure_channel.assert_called_with("localhost:50052")
        master_pb2_grpc.MasterStub.assert_called_once()
