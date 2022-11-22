"""
test code for resource_monitor setting
"""
from unittest import TestCase
import unittest
from experiment_scheduler.resource_monitor.setting import pynvml


class ResourceMonitorSettingTest(TestCase):
    """
    test class for resource monitor setting
    """

    def test_import(self):  # pylint: disable=R0201
        """
        test import
        :return:
        """

        try:
            pynvml.nvmlInit()
        except pynvml.NVMLError as error:
            print(f"Tested in environment without NVML. Error msg: {error}")


if __name__ == "__main__":
    unittest.main()
