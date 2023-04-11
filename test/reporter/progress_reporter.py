import unittest
from unittest.mock import patch
from experiment_scheduler.reporter.progress_reporter import report_progress
from experiment_scheduler.task_manager.grpc_task_manager import task_manager_pb2


class TestReportProgress(unittest.TestCase):
    @patch(
        "experiment_scheduler.task_manager.grpc_task_manager.task_manager_pb2_grpc.TaskManagerStub"
    )
    @patch("experiment_scheduler.reporter.progress_reporter.logger.warning")
    def test_report_progress(self, mock_warning, mock_stub):
        mock_response = task_manager_pb2.ProgressResponse()
        mock_response.received_status = (
            task_manager_pb2.ProgressResponse.ReceivedStatus.SUCCESS
        )
        mock_stub.return_value.report_progress.return_value = mock_response
        report_progress(0.5)

        mock_response.received_status = (
            task_manager_pb2.ProgressResponse.ReceivedStatus.FAIL
        )
        mock_stub.return_value.report_progress.return_value = mock_response

        report_progress(1.0)
        mock_warning.assert_called_once_with("fail to report progress")
        # mock_channel.assert_called_once()
        # mock_stub.assert_called_once()
        # mock_stub.return_value.report_progress.assert_called_once()


if __name__ == "__main__":
    unittest.main()
