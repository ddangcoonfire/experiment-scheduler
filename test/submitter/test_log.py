import pytest

import argparse
from os import path as osp

from experiment_scheduler.master.grpc_master import master_pb2, master_pb2_grpc
from experiment_scheduler.submitter.log import main


class MockMasterPb2GrpcMasterStub:

    @staticmethod
    def get_task_log(request):
        return [master_pb2.TaskLogFile(log_file=bytes("Test log", "utf-8"), error_message=None)]


class TestClass:
    @pytest.fixture
    def localhost(self):
        return "0.0.0.0:50052"

    @pytest.fixture
    def log_file_name(self):
        return "task_id-test0001"

    @pytest.fixture
    def mock_master_pb2_grpc_master_stub(self):
        return MockMasterPb2GrpcMasterStub()

    @pytest.fixture
    def parser(self):
        parser = argparse.ArgumentParser(description="Search Log for specific Task.")
        parser.add_argument("-t", "--task")
        parser.add_argument("-f", "--file")
        return parser

    @pytest.fixture
    def parser_with_no_file_option(self, parser, log_file_name):
        return parser.parse_args(["-t", log_file_name])

    @pytest.fixture
    def parser_with_file_option(self, parser, log_file_name):
        return parser.parse_args(["-t", log_file_name, "-f", "y"])

    @pytest.fixture
    def mock_grpc_insecure_channel(self, mocker):
        return mocker.patch("experiment_scheduler.submitter.log.grpc.insecure_channel",
                            return_value="test_grpc")

    @pytest.fixture
    def mock_master_pb2_grpc(self, mocker, mock_master_pb2_grpc_master_stub):
        return mocker.patch("experiment_scheduler.submitter.log.master_pb2_grpc.MasterStub",
                            return_value=mock_master_pb2_grpc_master_stub)

    def test_parse_args_with_no_file_option(self, parser_with_no_file_option, log_file_name):
        assert parser_with_no_file_option == argparse.Namespace(task=log_file_name, file=None)

    def test_parse_args_with_file_option(self, parser_with_file_option, log_file_name):
        assert parser_with_file_option == argparse.Namespace(task=log_file_name, file="y")

    def test_main_with_no_file_option(self, mocker, parser_with_no_file_option,
                                      mock_grpc_insecure_channel, mock_master_pb2_grpc, localhost):
        mock_parse_args = mocker.patch("experiment_scheduler.submitter.log.parse_args",
                                       return_value=parser_with_no_file_option)
        main()
        mock_parse_args.assert_called_once()
        mock_grpc_insecure_channel.assert_called_with(localhost)
        mock_master_pb2_grpc.assert_called_with("test_grpc")

    def test_main_with_file_option(self, mocker, parser_with_file_option, mock_grpc_insecure_channel,
                                   mock_master_pb2_grpc, localhost, log_file_name):
        mock_parse_args = mocker.patch("experiment_scheduler.submitter.log.parse_args",
                                       return_value=parser_with_file_option)
        log_path = osp.join(f"{log_file_name}.txt")
        main()
        mock_parse_args.assert_called_once()
        mock_grpc_insecure_channel.assert_called_with(localhost)
        mock_master_pb2_grpc.assert_called_with("test_grpc")
        assert osp.exists(log_path)
