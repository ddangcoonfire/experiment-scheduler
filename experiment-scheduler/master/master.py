from common.grpc_server import GrpcServer
from master.experiment_executor import ExperimentExecutor
from master.process_monitor import ProcessMonitor


class Master(GrpcServer):
    """
    Inherit GrpcServer to run Grpc Socket ( get request from submitter )
    """
    def __init__(self):
        """
        Init GrpcServer.
        """
        self.process_monitor = ProcessMonitor()
        self.submitter_socket = None  # something

    def execute(self):
        pass

    def run_new_experiment(self,experiment):
        pass
        # self.process_monitor.new_experiment(experiment)
    