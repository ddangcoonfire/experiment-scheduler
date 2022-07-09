import grpc
from common.master_task_manager_pb2_grpc import SubmitterCommandServiceStub as scss
from common import master_task_manager_pb2 as pb2
from common import master_task_manager_pb2_grpc as pb2_grpc

class GrpcServer:
    def __init__(self):
        """init grpc socket"""
        pass

    def start_server(self):
        pass

    def run_command(self):
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = scss(channel)
            response = stub.run_experiments(pb2.SubmitterRequest(name="abc"))
            print(response.message)

    def run_server(self):
        server = grpc.server(4)
        pb2_grpc.add_SubmitterCommandServiceServicer_to_server(pb2_grpc.SubmitterCommandServiceServicer(),server)
        server.add_insecure_port()
        server.start()
        server.wait_for_termination()
