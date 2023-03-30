# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: master.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0cmaster.proto\x12\x33\x65xperiment_scheduler.task_manager.grpc_task_manager\x1a\x1bgoogle/protobuf/empty.proto"\xab\x01\n\x13\x45xperimentStatement\x12\x0c\n\x04name\x18\x01 \x01(\t\x12W\n\x05tasks\x18\x02 \x03(\x0b\x32H.experiment_scheduler.task_manager.grpc_task_manager.MasterTaskStatement"-\n\x06Status\x12\x0b\n\x07RUNNING\x10\x00\x12\x08\n\x04\x44ONE\x10\x01\x12\x0c\n\x08\x41\x42NORMAL\x10\x02"\xcd\x01\n\x13MasterTaskStatement\x12\x0f\n\x07\x63ommand\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12g\n\x08task_env\x18\x04 \x03(\x0b\x32U.experiment_scheduler.task_manager.grpc_task_manager.MasterTaskStatement.TaskEnvEntry\x1a.\n\x0cTaskEnvEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01"\xb6\x01\n\x0eMasterResponse\x12\x15\n\rexperiment_id\x18\x01 \x01(\t\x12\x64\n\x08response\x18\x02 \x01(\x0e\x32R.experiment_scheduler.task_manager.grpc_task_manager.MasterResponse.ResponseStatus"\'\n\x0eResponseStatus\x12\x0b\n\x07SUCCESS\x10\x00\x12\x08\n\x04\x46\x41IL\x10\x01"\xcc\x01\n\nTaskStatus\x12\x0f\n\x07task_id\x18\x01 \x01(\t\x12V\n\x06status\x18\x02 \x01(\x0e\x32\x46.experiment_scheduler.task_manager.grpc_task_manager.TaskStatus.Status"U\n\x06Status\x12\x0c\n\x08NOTSTART\x10\x00\x12\x0b\n\x07RUNNING\x10\x01\x12\x08\n\x04\x44ONE\x10\x02\x12\n\n\x06KILLED\x10\x03\x12\x0c\n\x08\x41\x42NORMAL\x10\x04\x12\x0c\n\x08NOTFOUND\x10\x05"\x17\n\x04Task\x12\x0f\n\x07task_id\x18\x01 \x01(\t"#\n\nExperiment\x12\x15\n\rexperiment_id\x18\x01 \x01(\t"l\n\x0e\x41llTasksStatus\x12Z\n\x11task_status_array\x18\x01 \x03(\x0b\x32?.experiment_scheduler.task_manager.grpc_task_manager.TaskStatus"\x8a\x01\n\x11\x45xperimentsStatus\x12\x15\n\rexperiment_id\x18\x01 \x01(\t\x12^\n\x11task_status_array\x18\x02 \x01(\x0b\x32\x43.experiment_scheduler.task_manager.grpc_task_manager.AllTasksStatus"\x7f\n\x14\x41llExperimentsStatus\x12g\n\x17\x65xperiment_status_array\x18\x01 \x03(\x0b\x32\x46.experiment_scheduler.task_manager.grpc_task_manager.ExperimentsStatus"\x1f\n\x07TaskLog\x12\x14\n\x0clogfile_path\x18\x01 \x01(\t2\xc5\x06\n\x06Master\x12\xa6\x01\n\x13request_experiments\x12H.experiment_scheduler.task_manager.grpc_task_manager.ExperimentStatement\x1a\x43.experiment_scheduler.task_manager.grpc_task_manager.MasterResponse"\x00\x12\x89\x01\n\tkill_task\x12\x39.experiment_scheduler.task_manager.grpc_task_manager.Task\x1a?.experiment_scheduler.task_manager.grpc_task_manager.TaskStatus"\x00\x12\x8f\x01\n\x0fget_task_status\x12\x39.experiment_scheduler.task_manager.grpc_task_manager.Task\x1a?.experiment_scheduler.task_manager.grpc_task_manager.TaskStatus"\x00\x12\x89\x01\n\x0cget_task_log\x12\x39.experiment_scheduler.task_manager.grpc_task_manager.Task\x1a<.experiment_scheduler.task_manager.grpc_task_manager.TaskLog"\x00\x12\x9d\x01\n\rget_all_tasks\x12?.experiment_scheduler.task_manager.grpc_task_manager.Experiment\x1aI.experiment_scheduler.task_manager.grpc_task_manager.AllExperimentsStatus"\x00\x12H\n\x14halt_process_monitor\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty"\x00\x42\x06\xa2\x02\x03RTGb\x06proto3'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "master_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b"\242\002\003RTG"
    _MASTERTASKSTATEMENT_TASKENVENTRY._options = None
    _MASTERTASKSTATEMENT_TASKENVENTRY._serialized_options = b"8\001"
    _EXPERIMENTSTATEMENT._serialized_start = 99
    _EXPERIMENTSTATEMENT._serialized_end = 270
    _EXPERIMENTSTATEMENT_STATUS._serialized_start = 225
    _EXPERIMENTSTATEMENT_STATUS._serialized_end = 270
    _MASTERTASKSTATEMENT._serialized_start = 273
    _MASTERTASKSTATEMENT._serialized_end = 478
    _MASTERTASKSTATEMENT_TASKENVENTRY._serialized_start = 432
    _MASTERTASKSTATEMENT_TASKENVENTRY._serialized_end = 478
    _MASTERRESPONSE._serialized_start = 481
    _MASTERRESPONSE._serialized_end = 663
    _MASTERRESPONSE_RESPONSESTATUS._serialized_start = 624
    _MASTERRESPONSE_RESPONSESTATUS._serialized_end = 663
    _TASKSTATUS._serialized_start = 666
    _TASKSTATUS._serialized_end = 870
    _TASKSTATUS_STATUS._serialized_start = 785
    _TASKSTATUS_STATUS._serialized_end = 870
    _TASK._serialized_start = 872
    _TASK._serialized_end = 895
    _EXPERIMENT._serialized_start = 897
    _EXPERIMENT._serialized_end = 932
    _ALLTASKSSTATUS._serialized_start = 934
    _ALLTASKSSTATUS._serialized_end = 1042
    _EXPERIMENTSSTATUS._serialized_start = 1045
    _EXPERIMENTSSTATUS._serialized_end = 1183
    _ALLEXPERIMENTSSTATUS._serialized_start = 1185
    _ALLEXPERIMENTSSTATUS._serialized_end = 1312
    _TASKLOG._serialized_start = 1314
    _TASKLOG._serialized_end = 1345
    _MASTER._serialized_start = 1348
    _MASTER._serialized_end = 2185
# @@protoc_insertion_point(module_scope)
