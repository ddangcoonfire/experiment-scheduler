from experiment_scheduler.master.process_monitor import ProcessMonitor
from grpc_master.master_pb2_grpc import MasterServicer, add_MasterServicer_to_server
from grpc_master import master_pb2
from multiprocessing import Process
import grpc
from concurrent import futures
import uuid
import multiprocessing
import time
class Master(MasterServicer):

    """
    Inherit GrpcServer to run Grpc Socket ( get request from submitter )
    Class that runs on server
    """
    """
        To-Do :
        v Health Check
        Task Manager 의 작업 완료 센싱
         - get_task_status : master(폴링) / submitter(사용자 요청) 모두 사용가능
         - process가 필요하나
        request_experiments 로직 추가 검증 필요
        GPU Resource 따라서 Task Manager에 할당하는 알고리즘 추가
         - Resource를 기다리며 wait하는 알고리즘 필요
        Resource Monitor랑 통신
    """
    def __init__(self, max_workers=10):
        """
        Init GrpcServer.
        """
        # something.add ... to server ( , server )
        self.task_managers_address = self.get_task_managers()
        self.process_monitor = self.create_process_monitor()
        self.submitter_socket = None  # something
        self.tasks = []
        self.task_managers_shm = dict()
        self.manager = multiprocessing.Manager()

    def _run_process_monitor(self,task_manager_address, cmd):
        pm = ProcessMonitor(task_manager_address, cmd)
        pm.start()

    def create_process_monitor(self):
        # run process_monitor process
        # TODO today
        process_monitor_list = []
        for task_manager in self.task_managers_address:
            self.task_managers_shm[task_manager] = self.manager.list()
            p = Process(target=self._run_process_monitor, args=(task_manager, self.task_managers_shm[task_manager]))
            process_monitor_list.append(p)
        return process_monitor_list

    def get_task_managers(self):
        return ["localhost"]

    def select_task_manager(self, selected=-1):
        """
        Process Monitor automatically provide task that is able to run task
        :return:
        """
        # need convention later
        return self.task_managers[0] if selected < 0 else self.task_managers[selected]

    def check_task_manager_health(self, task_manager):
        # Should get this message from queue
        pass

    def request_experiments(self, request, context):
        experiment_id = request.name + '-' + str(uuid.uuid1())
        response_status = master_pb2.Response.ResponseStatus

        #1. submitter 에서 실험 요청을 함 (tasks보냄)
        #2. request_experiments 돈다
        #3. 실험이 다 끝나서 응답을 주는게 아니라, task_manager 에 등록이 되었다고 얘기해주는거
        #4. success = 실험 이제 돌릴거임
        #5. fail = 지금 task_manager가 뭐가 잘 안됨

        for task in request.tasks:
            response = self.request_experiment(task, context)
            if (response.response != 0):
                response = response_status.Fail
                # if fail, send msg to submitter that some ask failed to register
                # Or, send msg to submitter that something wrong with task_manager
                # One task failure should not fail all tasks
            else:
                self.tasks.append(response.experiment_id)
                response = response_status.SUCCESS
        return master_pb2.Response(experiment_id=experiment_id, response=response)

    def request_experiment(self, request, context):
        self.task_managers_shm[self.select_task_manager()].append(request.condition.gpuidx, request.command, request.name)
        time.sleep(1)

        # 작업 완료 후 response도 sharedMem으로
        # 원래 : Class, 지금 : Process Object
        # Run Task 를 Call 하느
        # need change here.

        # 파이프
        # message queue
        # shared memory

        task_id = self.task_managers_shm[self.select_task_manager()].pop()
        response_status = master_pb2.Response.ResponseStatus
        response = response_status.SUCCESS if task_id < 0 else response_status.FAIL
        return master_pb2.Response(experiment_id=task_id, response=response)


if __name__ == "__main__":
    master = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_MasterServicer_to_server(Master(), master)
    master.add_insecure_port('[::]:50050')
    master.start()
    master.wait_for_termination()
