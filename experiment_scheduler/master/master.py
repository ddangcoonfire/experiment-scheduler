from .process_monitor import ProcessMonitor
from grpc.master_pb2_grpc import MasterServicer, add_MasterServicer_to_server
from grpc import master_pb2
import grpc
from concurrent import futures


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
        self.process_monitor = ProcessMonitor(self.task_managers_address)
        self.submitter_socket = None  # something

    def execute(self):
        pass

    def get_task_managers(self):
        return ["localhost"]

    def check_task_manager_health(self, task_managers):
        # grpc request to all task_manageres
        pass

    def run_submitter_command(self, command):
        pass
        # self.process_monitor.new_experiment(experiment)

    def request_experiment(self, request, context):
        """
            override this method
            call task manager through process_monitor
            get task_id, success from task_manager if succeed
            else return -1 , error
        """
        task_id = self.process_monitor.run_task()
        response_status = master_pb2.Response.ResponseStatus
        response = response_status.SUCCESS if task_id < 0 else response_status.FAIL
        return master_pb2.Response(experiment_id=task_id, response= response)


if __name__ == "__main__":
    master = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_MasterServicer_to_server(Master(), master)
    master.add_insecure_port('[::]:50050')
    master.start()
    master.wait_for_termination()


