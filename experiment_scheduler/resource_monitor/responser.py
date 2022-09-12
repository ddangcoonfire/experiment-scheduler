import platform

import psutil as psutil
import logging
from experiment_scheduler.resource_monitor.setting import pynvml as N

class responser(object):
    global_processes = {}

    def __init__(self):
        self.hostname = platform.node()

    @staticmethod
    def get_all_gpu_info():
        logger = logging.getLogger()
        N.nvmlInit()
        def get_gpu_info(handle):

            def get_process_info(nv_process):
                process = {}
                if nv_process.pid not in responser.global_processes:
                    responser.global_processes[nv_process.pid] = \
                        psutil.Process(pid=nv_process.pid)
                process['pid'] = nv_process.pid
                return process

            try:
                nv_comp_processes = \
                    N.nvmlDeviceGetComputeRunningProcesses(handle)
            except N.NVMLError as e:
                logger.info("compute_processes", e)
                nv_comp_processes = None
            try:
                nv_graphics_processes = \
                    N.nvmlDeviceGetGraphicsRunningProcesses(handle)
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
                    process = get_process_info(nv_process)
                    processes.append(process)

            return {'index': N.nvmlDeviceGetIndex(handle), 'processes': processes}


        gpu_all_stat = []
        device_count = N.nvmlDeviceGetCount()

        for index in range(device_count):
            handle = N.nvmlDeviceGetHandleByIndex(index)
            info = get_gpu_info(handle)
            gpu_all_stat.append(info)

        return gpu_all_stat