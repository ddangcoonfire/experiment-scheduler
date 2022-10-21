"""
---
resource monitor
---
resource monitor gathers resource information of task managers.
master can decide which task manager to use by checking resource monitor
"""
import psutil as psutil
import logging
from experiment_scheduler.resource_monitor.setting import pynvml as N


class Monitor:
    def __init__(self):
        self.queued_gpu_idx = []
        self.task_manager_gpu_info = dict()
        self.global_processes = dict()

    def get_process_info(self, target_process):
        process = {}
        if target_process.pid not in self.global_processes:
            self.global_processes[target_process.pid] = psutil.Process(
                pid=target_process.pid
            )
        process["pid"] = target_process.pid
        return process

    def _get_gpu_info(self, handle):
        logger = logging.getLogger()
        try:
            nv_comp_processes = N.nvmlDeviceGetComputeRunningProcesses(handle)
        except N.NVMLError as e:
            logger.info("compute_processes", e)
            nv_comp_processes = None
        try:
            nv_graphics_processes = N.nvmlDeviceGetGraphicsRunningProcesses(handle)
        except N.NVMLError as e:
            logger.info("graphics_processes", e)
            nv_graphics_processes = None

        if nv_comp_processes is None and nv_graphics_processes is None:
            processes = None

        else:
            processes = []
            nv_comp_processes = nv_comp_processes or []
            nv_graphics_processes = nv_graphics_processes or []
            seen_pids = set()
            for nv_process in nv_comp_processes + nv_graphics_processes:
                if nv_process.pid in seen_pids:
                    continue
                seen_pids.add(nv_process.pid)
                process = self.get_process_info(nv_process)
                processes.append(process)

        util_info = N.nvmlDeviceGetUtilizationRates(handle)

        return {
            "gpu-index": N.nvmlDeviceGetIndex(handle),
            "processes": processes,
            "available_util": (100 - util_info.gpu),
        }

    def get_all_gpu_info(self):
        N.nvmlInit()
        gpu_all_stat = []
        device_count = N.nvmlDeviceGetCount()

        for index in range(device_count):
            handle = N.nvmlDeviceGetHandleByIndex(index)
            info = self._get_gpu_info(handle)
            gpu_all_stat.append(info)

        return gpu_all_stat

    def get_max_free_gpu(self):
        gpu_all_stat = self.get_all_gpu_info()
        max_free_gpu = {"gpu-index": -1, "process": None, "available_util": -1}
        for gpu in gpu_all_stat:
            if (
                gpu.get("available_util") > max_free_gpu.get("available_util")
                and gpu.get("available_util") > 20
            ):
                max_free_gpu = gpu
        return max_free_gpu.get("gpu-index")

    # resource monitor requirements
    # get task_manager's status by remote communication
    # need tuple (task_manager, gpu_index)
    # maybe observer pattern can be used this time
