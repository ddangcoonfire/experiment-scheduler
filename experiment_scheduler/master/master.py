from experiment_scheduler.master.process_monitor import ProcessMonitor
from grpc_master.master_pb2_grpc import MasterServicer, add_MasterServicer_to_server
from grpc_master import master_pb2
import grpc
from concurrent import futures
import uuid

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
        self.process_monitor = ProcessMonitor(self.task_managers_address)
        self.submitter_socket = None  # something
        self.tasks = []

    def execute(self):
        pass

    def get_task_managers(self):
        return ["localhost"]

    def check_task_manager_health(self, task_managers):
        # grpc request to all task_manageres
        # grpc_master request to all task_manageres
        pass

    def run_submitter_command(self, command):
        pass
        # self.process_monitor.new_experiment(experiment)

    def request_experiments(self, request, context):
        experiment_id = request.name + '-' + str(uuid.uuid1())
        response_status = master_pb2.Response.ResponseStatus
        for task in request.tasks:
            response = self.request_experiment(task, context)
            if (response.response != 0):
                response = response_status.Fail
                # 논의필요
                break
            else:
                self.tasks.append(response.experiment_id)
                response = response_status.SUCCESS
        return master_pb2.Response(experiment_id=experiment_id, response=response)

    def request_experiment(self, request, context):
        task_id = self.process_monitor.run_task(request.condition.gpuidx, request.command, request.name)
        response_status = master_pb2.Response.ResponseStatus
        response = response_status.SUCCESS if task_id < 0 else response_status.FAIL
        return master_pb2.Response(experiment_id=task_id, response=response)


if __name__ == "__main__":
    master = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_MasterServicer_to_server(Master(), master)
    master.add_insecure_port('[::]:50050')
    master.start()
    master.wait_for_termination()
