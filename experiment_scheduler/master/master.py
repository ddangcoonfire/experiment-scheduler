from master.process_monitor import ProcessMonitor
from master.grpc.master_pb2_grpc import MasterServicer,add_MasterServicer_to_server
import grpc
from concurrent import futures


class Master(MasterServicer):
    """
    Inherit GrpcServer to run Grpc Socket ( get request from submitter )
    """
    def __init__(self, max_workers=10):
        """
        Init GrpcServer.
        """
        # something.add ... to server ( , server )
        self.task_managers_address = self.get_task_managers()
        self.process_monitor = ProcessMonitor(self.task_managers_address)
        self.submitter_socket = None  # something
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
        # self.server.add_insecure_port('[::]:50050')

    def execute(self):
        pass

    def get_task_managers(self):
        return ["localhost"]

    def check_task_manager_health(self,task_managers):
        # grpc request to all task_manageres
        pass

    def run_submitter_command(self,command):
        pass
        # self.process_monitor.new_experiment(experiment)

    def request_experiment(self, request, context):
        task_id = self.process_monitor.run_task()
        return task_id


if __name__ == "__main__":
    master = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_MasterServicer_to_server(Master(), master)
    master.add_insecure_port('[::]:50050')
    master.start()
    master.wait_for_termination()

