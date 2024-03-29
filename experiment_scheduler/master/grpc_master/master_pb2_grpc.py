# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
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
                '/experiment_scheduler.task_manager.grpc_task_manager.Master/request_experiments',
                request_serializer=master__pb2.ExperimentStatement.SerializeToString,
                response_deserializer=master__pb2.MasterResponse.FromString,
                )
        self.kill_task = channel.unary_unary(
                '/experiment_scheduler.task_manager.grpc_task_manager.Master/kill_task',
                request_serializer=master__pb2.Task.SerializeToString,
                response_deserializer=master__pb2.TaskStatus.FromString,
                )
        self.kill_experiment = channel.unary_unary(
                '/experiment_scheduler.task_manager.grpc_task_manager.Master/kill_experiment',
                request_serializer=master__pb2.Experiment.SerializeToString,
                response_deserializer=master__pb2.ExperimentsStatus.FromString,
                )
        self.get_task_status = channel.unary_unary(
                '/experiment_scheduler.task_manager.grpc_task_manager.Master/get_task_status',
                request_serializer=master__pb2.Task.SerializeToString,
                response_deserializer=master__pb2.TaskStatus.FromString,
                )
        self.get_task_log = channel.unary_stream(
                '/experiment_scheduler.task_manager.grpc_task_manager.Master/get_task_log',
                request_serializer=master__pb2.Task.SerializeToString,
                response_deserializer=master__pb2.TaskLogFile.FromString,
                )
        self.get_all_tasks = channel.unary_unary(
                '/experiment_scheduler.task_manager.grpc_task_manager.Master/get_all_tasks',
                request_serializer=master__pb2.Experiment.SerializeToString,
                response_deserializer=master__pb2.AllExperimentsStatus.FromString,
                )
        self.halt_process_monitor = channel.unary_unary(
                '/experiment_scheduler.task_manager.grpc_task_manager.Master/halt_process_monitor',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.edit_task = channel.unary_unary(
                '/experiment_scheduler.task_manager.grpc_task_manager.Master/edit_task',
                request_serializer=master__pb2.EditTask.SerializeToString,
                response_deserializer=master__pb2.MasterResponse.FromString,
                )
        self.request_abnormal_exited_tasks = channel.unary_unary(
                '/experiment_scheduler.task_manager.grpc_task_manager.Master/request_abnormal_exited_tasks',
                request_serializer=master__pb2.TaskList.SerializeToString,
                response_deserializer=master__pb2.RequestAbnormalExitedTasksResponse.FromString,
                )
        self.upload_file = channel.stream_unary(
                '/experiment_scheduler.task_manager.grpc_task_manager.Master/upload_file',
                request_serializer=master__pb2.MasterFileUploadRequest.SerializeToString,
                response_deserializer=master__pb2.MasterFileUploadResponse.FromString,
                )
        self.delete_file = channel.unary_unary(
                '/experiment_scheduler.task_manager.grpc_task_manager.Master/delete_file',
                request_serializer=master__pb2.MasterFileDeleteRequest.SerializeToString,
                response_deserializer=master__pb2.MasterFileDeleteResponse.FromString,
                )


class MasterServicer(object):
    """Interface exported by the server.
    """

    def request_experiments(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def kill_task(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def kill_experiment(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_task_status(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_task_log(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_all_tasks(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def halt_process_monitor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def edit_task(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def request_abnormal_exited_tasks(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def upload_file(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def delete_file(self, request, context):
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
            'kill_task': grpc.unary_unary_rpc_method_handler(
                    servicer.kill_task,
                    request_deserializer=master__pb2.Task.FromString,
                    response_serializer=master__pb2.TaskStatus.SerializeToString,
            ),
            'kill_experiment': grpc.unary_unary_rpc_method_handler(
                    servicer.kill_experiment,
                    request_deserializer=master__pb2.Experiment.FromString,
                    response_serializer=master__pb2.ExperimentsStatus.SerializeToString,
            ),
            'get_task_status': grpc.unary_unary_rpc_method_handler(
                    servicer.get_task_status,
                    request_deserializer=master__pb2.Task.FromString,
                    response_serializer=master__pb2.TaskStatus.SerializeToString,
            ),
            'get_task_log': grpc.unary_stream_rpc_method_handler(
                    servicer.get_task_log,
                    request_deserializer=master__pb2.Task.FromString,
                    response_serializer=master__pb2.TaskLogFile.SerializeToString,
            ),
            'get_all_tasks': grpc.unary_unary_rpc_method_handler(
                    servicer.get_all_tasks,
                    request_deserializer=master__pb2.Experiment.FromString,
                    response_serializer=master__pb2.AllExperimentsStatus.SerializeToString,
            ),
            'halt_process_monitor': grpc.unary_unary_rpc_method_handler(
                    servicer.halt_process_monitor,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'edit_task': grpc.unary_unary_rpc_method_handler(
                    servicer.edit_task,
                    request_deserializer=master__pb2.EditTask.FromString,
                    response_serializer=master__pb2.MasterResponse.SerializeToString,
            ),
            'request_abnormal_exited_tasks': grpc.unary_unary_rpc_method_handler(
                    servicer.request_abnormal_exited_tasks,
                    request_deserializer=master__pb2.TaskList.FromString,
                    response_serializer=master__pb2.RequestAbnormalExitedTasksResponse.SerializeToString,
            ),
            'upload_file': grpc.stream_unary_rpc_method_handler(
                    servicer.upload_file,
                    request_deserializer=master__pb2.MasterFileUploadRequest.FromString,
                    response_serializer=master__pb2.MasterFileUploadResponse.SerializeToString,
            ),
            'delete_file': grpc.unary_unary_rpc_method_handler(
                    servicer.delete_file,
                    request_deserializer=master__pb2.MasterFileDeleteRequest.FromString,
                    response_serializer=master__pb2.MasterFileDeleteResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'experiment_scheduler.task_manager.grpc_task_manager.Master', rpc_method_handlers)
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
        return grpc.experimental.unary_unary(request, target, '/experiment_scheduler.task_manager.grpc_task_manager.Master/request_experiments',
            master__pb2.ExperimentStatement.SerializeToString,
            master__pb2.MasterResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def kill_task(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/experiment_scheduler.task_manager.grpc_task_manager.Master/kill_task',
            master__pb2.Task.SerializeToString,
            master__pb2.TaskStatus.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def kill_experiment(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/experiment_scheduler.task_manager.grpc_task_manager.Master/kill_experiment',
            master__pb2.Experiment.SerializeToString,
            master__pb2.ExperimentsStatus.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_task_status(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/experiment_scheduler.task_manager.grpc_task_manager.Master/get_task_status',
            master__pb2.Task.SerializeToString,
            master__pb2.TaskStatus.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_task_log(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/experiment_scheduler.task_manager.grpc_task_manager.Master/get_task_log',
            master__pb2.Task.SerializeToString,
            master__pb2.TaskLogFile.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_all_tasks(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/experiment_scheduler.task_manager.grpc_task_manager.Master/get_all_tasks',
            master__pb2.Experiment.SerializeToString,
            master__pb2.AllExperimentsStatus.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def halt_process_monitor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/experiment_scheduler.task_manager.grpc_task_manager.Master/halt_process_monitor',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def edit_task(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/experiment_scheduler.task_manager.grpc_task_manager.Master/edit_task',
            master__pb2.EditTask.SerializeToString,
            master__pb2.MasterResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def request_abnormal_exited_tasks(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/experiment_scheduler.task_manager.grpc_task_manager.Master/request_abnormal_exited_tasks',
            master__pb2.TaskList.SerializeToString,
            master__pb2.RequestAbnormalExitedTasksResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def upload_file(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/experiment_scheduler.task_manager.grpc_task_manager.Master/upload_file',
            master__pb2.MasterFileUploadRequest.SerializeToString,
            master__pb2.MasterFileUploadResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def delete_file(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/experiment_scheduler.task_manager.grpc_task_manager.Master/delete_file',
            master__pb2.MasterFileDeleteRequest.SerializeToString,
            master__pb2.MasterFileDeleteResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
