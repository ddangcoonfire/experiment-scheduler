from common.grpc_server import GrpcServer
from master.experiment_executor import ExperimentExecutor
from master.process_monitor import ProcessMonitor


class Master(GrpcServer):
    """
    Inherit GrpcServer to run Grpc Socket ( get request from submitter )
    """
    def __init__(self, max_workers=10):
        """
        Init GrpcServer.
        """
        super(max_workers).__init__()
        # something.add ... to server ( , server )
        self.task_managers_address = self.get_task_managers()
        self.process_monitor = ProcessMonitor(self.task_managers_address)
        self.submitter_socket = None  # something


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


if __name__ == "__main__":
    master = Master()
    master.start_server()
