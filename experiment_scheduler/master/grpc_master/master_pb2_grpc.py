# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import experiment_scheduler.master.grpc_master.master_pb2 as master__pb2


class MasterStub(object):
    """Interface exported by the server.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.request_experiments = channel.unary_unary(
                '/Master/request_experiments',
                request_serializer=master__pb2.ExperimentStatement.SerializeToString,
                response_deserializer=master__pb2.MasterResponse.FromString,
                )


class MasterServicer(object):
    """Interface exported by the server.
    """

    def request_experiments(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MasterServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'request_experiments': grpc.unary_unary_rpc_method_handler(
                    servicer.request_experiments,
                    request_deserializer=master__pb2.ExperimentStatement.FromString,
                    response_serializer=master__pb2.MasterResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Master', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Master(object):
    """Interface exported by the server.
    """

    @staticmethod
    def request_experiments(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Master/request_experiments',
            master__pb2.ExperimentStatement.SerializeToString,
            master__pb2.MasterResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
