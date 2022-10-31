# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
import experiment_scheduler.master.grpc_master.master_pb2 as master__pb2


class MasterStub(object):
    """Interface exported by the server."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.request_experiments = channel.unary_unary(
            "/experiment_scheduler.task_manager.grpc_task_manager.Master/request_experiments",
            request_serializer=master__pb2.ExperimentStatement.SerializeToString,
            response_deserializer=master__pb2.MasterResponse.FromString,
        )
        self.kill_task = channel.unary_unary(
            "/experiment_scheduler.task_manager.grpc_task_manager.Master/kill_task",
            request_serializer=master__pb2.Task.SerializeToString,
            response_deserializer=master__pb2.TaskStatus.FromString,
        )
        self.get_task_status = channel.unary_unary(
            "/experiment_scheduler.task_manager.grpc_task_manager.Master/get_task_status",
            request_serializer=master__pb2.Task.SerializeToString,
            response_deserializer=master__pb2.TaskStatus.FromString,
        )
        self.get_task_log = channel.unary_unary(
            "/experiment_scheduler.task_manager.grpc_task_manager.Master/get_task_log",
            request_serializer=master__pb2.Task.SerializeToString,
            response_deserializer=master__pb2.TaskLog.FromString,
        )
        self.get_all_tasks = channel.unary_unary(
            "/experiment_scheduler.task_manager.grpc_task_manager.Master/get_all_tasks",
            request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            response_deserializer=master__pb2.AllTasksStatus.FromString,
        )
        self.halt_process_monitor = channel.unary_unary(
            "/experiment_scheduler.task_manager.grpc_task_manager.Master/halt_process_monitor",
            request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )


class MasterServicer(object):
    """Interface exported by the server."""

    def request_experiments(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def kill_task(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def get_task_status(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def get_task_log(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def get_all_tasks(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def halt_process_monitor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_MasterServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "request_experiments": grpc.unary_unary_rpc_method_handler(
            servicer.request_experiments,
            request_deserializer=master__pb2.ExperimentStatement.FromString,
            response_serializer=master__pb2.MasterResponse.SerializeToString,
        ),
        "kill_task": grpc.unary_unary_rpc_method_handler(
            servicer.kill_task,
            request_deserializer=master__pb2.Task.FromString,
            response_serializer=master__pb2.TaskStatus.SerializeToString,
        ),
        "get_task_status": grpc.unary_unary_rpc_method_handler(
            servicer.get_task_status,
            request_deserializer=master__pb2.Task.FromString,
            response_serializer=master__pb2.TaskStatus.SerializeToString,
        ),
        "get_task_log": grpc.unary_unary_rpc_method_handler(
            servicer.get_task_log,
            request_deserializer=master__pb2.Task.FromString,
            response_serializer=master__pb2.TaskLog.SerializeToString,
        ),
        "get_all_tasks": grpc.unary_unary_rpc_method_handler(
            servicer.get_all_tasks,
            request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            response_serializer=master__pb2.AllTasksStatus.SerializeToString,
        ),
        "halt_process_monitor": grpc.unary_unary_rpc_method_handler(
            servicer.halt_process_monitor,
            request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "experiment_scheduler.task_manager.grpc_task_manager.Master",
        rpc_method_handlers,
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class Master(object):
    """Interface exported by the server."""

    @staticmethod
    def request_experiments(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/experiment_scheduler.task_manager.grpc_task_manager.Master/request_experiments",
            master__pb2.ExperimentStatement.SerializeToString,
            master__pb2.MasterResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def kill_task(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/experiment_scheduler.task_manager.grpc_task_manager.Master/kill_task",
            master__pb2.Task.SerializeToString,
            master__pb2.TaskStatus.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def get_task_status(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/experiment_scheduler.task_manager.grpc_task_manager.Master/get_task_status",
            master__pb2.Task.SerializeToString,
            master__pb2.TaskStatus.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def get_task_log(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/experiment_scheduler.task_manager.grpc_task_manager.Master/get_task_log",
            master__pb2.Task.SerializeToString,
            master__pb2.TaskLog.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def get_all_tasks(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/experiment_scheduler.task_manager.grpc_task_manager.Master/get_all_tasks",
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            master__pb2.AllTasksStatus.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def halt_process_monitor(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/experiment_scheduler.task_manager.grpc_task_manager.Master/halt_process_monitor",
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
