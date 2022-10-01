from collections import namedtuple
import pytest
from experiment_scheduler.resource_monitor import monitor
from experiment_scheduler.resource_monitor.setting import pynvml
import psutil
from mockito import when, mock

MB = 1024 * 1024


def _configure_mock(N = pynvml, scenario_nonexistent_pid=False):
    N.NVMLError.__hash__ = lambda _: 0
    assert issubclass(N.NVMLError, BaseException)

    when(N).nvmlInit().thenReturn()

    num_gpus = 3
    mock_handles = ['mock-handle-%d' % i for i in range(3)]
    when(N).nvmlDeviceGetCount().thenReturn(num_gpus)

    def _return_or_raise(v):
        def _callable(*args, **kwargs):
            if isinstance(v, Exception):
                raise v
            return v
        return _callable

    for i in range(num_gpus):
        handle = mock_handles[i]
        when(N).nvmlDeviceGetHandleByIndex(i) \
            .thenReturn(handle)
        when(N).nvmlDeviceGetIndex(handle) \
            .thenReturn(i)

        mock_process_t = namedtuple("Process_t", ['pid'])
        mock_utilization_t = namedtuple("Utilization_t", ['gpu', 'memory'])

        if scenario_nonexistent_pid:
            mock_processes_error = [
                mock_process_t(99999),
                mock_process_t(99995),
            ]
        else:
            mock_processes_error = N.NVMLError_NotSupported()

        when(N).nvmlDeviceGetComputeRunningProcesses(handle) \
            .thenAnswer(_return_or_raise({
                                             0: [mock_process_t(11111), mock_process_t(44444)],
                                             1: [mock_process_t(66666), mock_process_t(55555)],
                                             2: mock_processes_error
                                         }[i]))

        when(N).nvmlDeviceGetGraphicsRunningProcesses(handle) \
            .thenAnswer(_return_or_raise({
                                             0: [mock_process_t(11111)],
                                             1: [],
                                             2: N.NVMLError_NotSupported(),
                                         }[i]))

        when(N).nvmlDeviceGetUtilizationRates(handle) \
            .thenAnswer(_return_or_raise({
                                             0: mock_utilization_t(gpu=76, memory=0),
                                             1: mock_utilization_t(gpu=32, memory=0),
                                             2: mock_utilization_t(gpu=0, memory=0)
                                         }[i]))

    mock_pid_map = {
        11111: ('user1', 'ddangko-sub-1'),
        22222: ('user1', 'ddangko-sub-2'),
        33333: ('user3', 'ddangko-sub-3'),
        44444: ('user2', 'ddangko-sub-4'),
        55555: ('user3', 'ddangko-sub-5'),
        66666: ('user1', 'ddangko-sub-6'),
    }
    assert 99999 not in mock_pid_map, 'scenario_nonexistent_pid'
    assert 99995 not in mock_pid_map, 'scenario_nonexistent_pid'

    def _MockedProcess(pid):
        if pid not in mock_pid_map:
            if pid == 99995:
                raise FileNotFoundError("/proc/99995/stat")
            else:
                raise psutil.NoSuchProcess(pid=pid)
        p = mock(strict=True)
        p.pid = pid
        return p

    when(psutil).Process(...).thenAnswer(_MockedProcess)

@pytest.fixture
def scenario_basic():
    _configure_mock()


@pytest.fixture
def scenario_nonexistent_pid():
    _configure_mock(scenario_nonexistent_pid=True)


class TestGpuMonitor(object):

    def test_get_process_info(self, scenario_basic):
        assert monitor.responser.get_all_gpu_info() == [
            {'gpu-index': 0, 'processes': [{'pid': 11111}, {'pid': 44444}], 'available_util': 24},
            {'gpu-index': 1, 'processes': [{'pid': 66666}, {'pid': 55555}], 'available_util': 68},
            {'gpu-index': 2, 'processes': None, 'available_util': 100}]

    def test_nonexistent_pid(self, scenario_nonexistent_pid):
        with pytest.raises(psutil.NoSuchProcess):
            monitor.responser.get_all_gpu_info()

    def test_get_max_free_gpu(self, scenario_basic):
        assert monitor.responser.get_max_free_gpu() == 2
