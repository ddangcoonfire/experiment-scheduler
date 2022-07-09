import grpc
from common.master_task_manager_pb2_grpc import SubmitterCommandServiceStub as scss
from common import master_task_manager_pb2 as pb2


class GrpcServer:
    def __init__(self):
        """init grpc socket"""
        pass

    def start_server(self):
        pass

    def run(self):
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = scss(channel)
            response = stub.run_experiments(pb2.SubmitterRequest(name="abc"))
            print(response.message)

