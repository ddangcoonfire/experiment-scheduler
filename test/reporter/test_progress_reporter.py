"""
Test codes for progress_reporter
"""
import unittest
from unittest.mock import patch

from experiment_scheduler.reporter.progress_reporter import report_progress
from experiment_scheduler.task_manager.grpc_task_manager import task_manager_pb2


class TestReportProgress(unittest.TestCase):
    """
    Test Class for Report Progress
    """

    @patch(
        "experiment_scheduler.task_manager.grpc_task_manager.task_manager_pb2_grpc.TaskManagerStub"
    )
    @patch("experiment_scheduler.reporter.progress_reporter.logger.warning")
    def test_report_progress(self, mock_warning, mock_stub):
        """
        report progress test method
        :param mock_warning:
        :param mock_stub:
        :return:
        """
        # prepare
        mock_response = task_manager_pb2.ProgressResponse()
        mock_response.received_status = (
            task_manager_pb2.ProgressResponse.ReceivedStatus.SUCCESS
        )
        mock_stub.return_value.report_progress.return_value = mock_response

        # run and check
        report_progress(0.5)

        # prepare
        mock_response.received_status = (
            task_manager_pb2.ProgressResponse.ReceivedStatus.FAIL
        )
        mock_stub.return_value.report_progess.return_value = mock_response

        # run and check
        report_progress(1.0)
        mock_warning.assert_called_once_with("fail to report progress")


if __name__ == "__main__":
    unittest.main()
