from unittest import TestCase


class ResourceMonitorTest(TestCase):
    def setUp(self):
        pass

    def test_import(self):
        from experiment_scheduler.resource_monitor.setting import pynvml
        pynvml
        # test if imported well

