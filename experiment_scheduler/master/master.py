from master.experiment_executor import ExperimentExecutor
from master.process_monitor import ProcessMonitor
from master.master_pb2_grpc import MasterServicer
import grpc

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
    def start_server(self):
        self.server.start()
        self.server.wait_for_termination()

if __name__ == "__main__":
    master = Master()
    master.start_server()
