# from .process_monitor import ProcessMonitor
from grpc_repo.master_pb2_grpc import MasterServicer, add_MasterServicer_to_server
from grpc_repo import master_pb2
import grpc
from concurrent import futures
import uuid

class Master(MasterServicer):
    """
    Inherit GrpcServer to run Grpc Socket ( get request from submitter )
    Class that runs on server
    """

    def __init__(self, max_workers=10):
        """
        Init GrpcServer.
        """
        # something.add ... to server ( , server )
        self.task_managers_address = self.get_task_managers()
        # self.process_monitor = ProcessMonitor(self.task_managers_address)
        self.submitter_socket = None  # something

    def execute(self):
        pass

    def get_task_managers(self):
        return ["localhost"]

    def check_task_manager_health(self, task_managers):
        # grpc_repo request to all task_manageres
        pass

    def run_submitter_command(self, command):
        pass
        # self.process_monitor.new_experiment(experiment)

    def request_experiment(self, request, context):
        # task가 여러개인데 id는 한개만 받음
        # 이를 exp에 대한 response는 한개만 실패해도 실패 response를 보내는게 맞는가?
        # 각각의 task에 대한 response가 필요하다면 .proto의 Response가
        # repeated로 바뀌거나 다른 방안이 필요
        # 위와 같은 방향으로 우선 수정해봄

        experiment_id = request.name + '-' + str(uuid.uuid1())
        response_status = master_pb2.Response.ResponseStatus
        for task in request.tasks:
            task_id = self.process_monitor.run_task(task.condition.gpuidx, task.command, task.name)
            if (task_id >= 0):
                response = response_status.Fail
                break
            else:
                response = response_status.SUCCESS

        # task_id = self.process_monitor.run_task(request)
        # response_status = master_pb2.Response.ResponseStatus
        # response = response_status.SUCCESS if task_id < 0 else response_status.FAIL
        return master_pb2.Response(experiment_id=experiment_id, response=response)


if __name__ == "__main__":
    master = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_MasterServicer_to_server(Master(), master)
    master.add_insecure_port('[::]:50049')
    master.start()
    master.wait_for_termination()
