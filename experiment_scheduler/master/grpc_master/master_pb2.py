# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: master.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cmaster.proto\x12\x33\x65xperiment_scheduler.task_manager.grpc_task_manager\x1a\x1bgoogle/protobuf/empty.proto\"|\n\x13\x45xperimentStatement\x12\x0c\n\x04name\x18\x01 \x01(\t\x12W\n\x05tasks\x18\x02 \x03(\x0b\x32H.experiment_scheduler.task_manager.grpc_task_manager.MasterTaskStatement\"\xcd\x01\n\x13MasterTaskStatement\x12\x0f\n\x07\x63ommand\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12g\n\x08task_env\x18\x04 \x03(\x0b\x32U.experiment_scheduler.task_manager.grpc_task_manager.MasterTaskStatement.TaskEnvEntry\x1a.\n\x0cTaskEnvEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xb6\x01\n\x0eMasterResponse\x12\x15\n\rexperiment_id\x18\x01 \x01(\t\x12\x64\n\x08response\x18\x02 \x01(\x0e\x32R.experiment_scheduler.task_manager.grpc_task_manager.MasterResponse.ResponseStatus\"\'\n\x0eResponseStatus\x12\x0b\n\x07SUCCESS\x10\x00\x12\x08\n\x04\x46\x41IL\x10\x01\"\xcc\x01\n\nTaskStatus\x12\x0f\n\x07task_id\x18\x01 \x01(\t\x12V\n\x06status\x18\x02 \x01(\x0e\x32\x46.experiment_scheduler.task_manager.grpc_task_manager.TaskStatus.Status\"U\n\x06Status\x12\x0c\n\x08NOTSTART\x10\x00\x12\x0b\n\x07RUNNING\x10\x01\x12\x08\n\x04\x44ONE\x10\x02\x12\n\n\x06KILLED\x10\x03\x12\x0c\n\x08\x41\x42NORMAL\x10\x04\x12\x0c\n\x08NOTFOUND\x10\x05\"\x17\n\x04Task\x12\x0f\n\x07task_id\x18\x01 \x01(\t\"#\n\nExperiment\x12\x15\n\rexperiment_id\x18\x01 \x01(\t\"l\n\x0e\x41llTasksStatus\x12Z\n\x11task_status_array\x18\x01 \x03(\x0b\x32?.experiment_scheduler.task_manager.grpc_task_manager.TaskStatus\"\x8a\x01\n\x11\x45xperimentsStatus\x12\x15\n\rexperiment_id\x18\x01 \x01(\t\x12^\n\x11task_status_array\x18\x02 \x01(\x0b\x32\x43.experiment_scheduler.task_manager.grpc_task_manager.AllTasksStatus\"\x7f\n\x14\x41llExperimentsStatus\x12g\n\x17\x65xperiment_status_array\x18\x01 \x03(\x0b\x32\x46.experiment_scheduler.task_manager.grpc_task_manager.ExperimentsStatus\"\x1f\n\x07TaskLog\x12\x14\n\x0clogfile_path\x18\x01 \x01(\t\"\x1f\n\x0bTaskLogFile\x12\x10\n\x08log_file\x18\x01 \x01(\x0c\x32\xcb\x06\n\x06Master\x12\xa6\x01\n\x13request_experiments\x12H.experiment_scheduler.task_manager.grpc_task_manager.ExperimentStatement\x1a\x43.experiment_scheduler.task_manager.grpc_task_manager.MasterResponse\"\x00\x12\x89\x01\n\tkill_task\x12\x39.experiment_scheduler.task_manager.grpc_task_manager.Task\x1a?.experiment_scheduler.task_manager.grpc_task_manager.TaskStatus\"\x00\x12\x8f\x01\n\x0fget_task_status\x12\x39.experiment_scheduler.task_manager.grpc_task_manager.Task\x1a?.experiment_scheduler.task_manager.grpc_task_manager.TaskStatus\"\x00\x12\x8f\x01\n\x0cget_task_log\x12\x39.experiment_scheduler.task_manager.grpc_task_manager.Task\x1a@.experiment_scheduler.task_manager.grpc_task_manager.TaskLogFile\"\x00\x30\x01\x12\x9d\x01\n\rget_all_tasks\x12?.experiment_scheduler.task_manager.grpc_task_manager.Experiment\x1aI.experiment_scheduler.task_manager.grpc_task_manager.AllExperimentsStatus\"\x00\x12H\n\x14halt_process_monitor\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x42\x06\xa2\x02\x03RTGb\x06proto3')



_EXPERIMENTSTATEMENT = DESCRIPTOR.message_types_by_name['ExperimentStatement']
_MASTERTASKSTATEMENT = DESCRIPTOR.message_types_by_name['MasterTaskStatement']
_MASTERTASKSTATEMENT_TASKENVENTRY = _MASTERTASKSTATEMENT.nested_types_by_name['TaskEnvEntry']
_MASTERRESPONSE = DESCRIPTOR.message_types_by_name['MasterResponse']
_TASKSTATUS = DESCRIPTOR.message_types_by_name['TaskStatus']
_TASK = DESCRIPTOR.message_types_by_name['Task']
_EXPERIMENT = DESCRIPTOR.message_types_by_name['Experiment']
_ALLTASKSSTATUS = DESCRIPTOR.message_types_by_name['AllTasksStatus']
_EXPERIMENTSSTATUS = DESCRIPTOR.message_types_by_name['ExperimentsStatus']
_ALLEXPERIMENTSSTATUS = DESCRIPTOR.message_types_by_name['AllExperimentsStatus']
_TASKLOG = DESCRIPTOR.message_types_by_name['TaskLog']
_TASKLOGFILE = DESCRIPTOR.message_types_by_name['TaskLogFile']
_MASTERRESPONSE_RESPONSESTATUS = _MASTERRESPONSE.enum_types_by_name['ResponseStatus']
_TASKSTATUS_STATUS = _TASKSTATUS.enum_types_by_name['Status']
ExperimentStatement = _reflection.GeneratedProtocolMessageType('ExperimentStatement', (_message.Message,), {
  'DESCRIPTOR' : _EXPERIMENTSTATEMENT,
  '__module__' : 'master_pb2'
  # @@protoc_insertion_point(class_scope:experiment_scheduler.task_manager.grpc_task_manager.ExperimentStatement)
  })
_sym_db.RegisterMessage(ExperimentStatement)

MasterTaskStatement = _reflection.GeneratedProtocolMessageType('MasterTaskStatement', (_message.Message,), {

  'TaskEnvEntry' : _reflection.GeneratedProtocolMessageType('TaskEnvEntry', (_message.Message,), {
    'DESCRIPTOR' : _MASTERTASKSTATEMENT_TASKENVENTRY,
    '__module__' : 'master_pb2'
    # @@protoc_insertion_point(class_scope:experiment_scheduler.task_manager.grpc_task_manager.MasterTaskStatement.TaskEnvEntry)
    })
  ,
  'DESCRIPTOR' : _MASTERTASKSTATEMENT,
  '__module__' : 'master_pb2'
  # @@protoc_insertion_point(class_scope:experiment_scheduler.task_manager.grpc_task_manager.MasterTaskStatement)
  })
_sym_db.RegisterMessage(MasterTaskStatement)
_sym_db.RegisterMessage(MasterTaskStatement.TaskEnvEntry)

MasterResponse = _reflection.GeneratedProtocolMessageType('MasterResponse', (_message.Message,), {
  'DESCRIPTOR' : _MASTERRESPONSE,
  '__module__' : 'master_pb2'
  # @@protoc_insertion_point(class_scope:experiment_scheduler.task_manager.grpc_task_manager.MasterResponse)
  })
_sym_db.RegisterMessage(MasterResponse)

TaskStatus = _reflection.GeneratedProtocolMessageType('TaskStatus', (_message.Message,), {
  'DESCRIPTOR' : _TASKSTATUS,
  '__module__' : 'master_pb2'
  # @@protoc_insertion_point(class_scope:experiment_scheduler.task_manager.grpc_task_manager.TaskStatus)
  })
_sym_db.RegisterMessage(TaskStatus)

Task = _reflection.GeneratedProtocolMessageType('Task', (_message.Message,), {
  'DESCRIPTOR' : _TASK,
  '__module__' : 'master_pb2'
  # @@protoc_insertion_point(class_scope:experiment_scheduler.task_manager.grpc_task_manager.Task)
  })
_sym_db.RegisterMessage(Task)

Experiment = _reflection.GeneratedProtocolMessageType('Experiment', (_message.Message,), {
  'DESCRIPTOR' : _EXPERIMENT,
  '__module__' : 'master_pb2'
  # @@protoc_insertion_point(class_scope:experiment_scheduler.task_manager.grpc_task_manager.Experiment)
  })
_sym_db.RegisterMessage(Experiment)

AllTasksStatus = _reflection.GeneratedProtocolMessageType('AllTasksStatus', (_message.Message,), {
  'DESCRIPTOR' : _ALLTASKSSTATUS,
  '__module__' : 'master_pb2'
  # @@protoc_insertion_point(class_scope:experiment_scheduler.task_manager.grpc_task_manager.AllTasksStatus)
  })
_sym_db.RegisterMessage(AllTasksStatus)

ExperimentsStatus = _reflection.GeneratedProtocolMessageType('ExperimentsStatus', (_message.Message,), {
  'DESCRIPTOR' : _EXPERIMENTSSTATUS,
  '__module__' : 'master_pb2'
  # @@protoc_insertion_point(class_scope:experiment_scheduler.task_manager.grpc_task_manager.ExperimentsStatus)
  })
_sym_db.RegisterMessage(ExperimentsStatus)

AllExperimentsStatus = _reflection.GeneratedProtocolMessageType('AllExperimentsStatus', (_message.Message,), {
  'DESCRIPTOR' : _ALLEXPERIMENTSSTATUS,
  '__module__' : 'master_pb2'
  # @@protoc_insertion_point(class_scope:experiment_scheduler.task_manager.grpc_task_manager.AllExperimentsStatus)
  })
_sym_db.RegisterMessage(AllExperimentsStatus)

TaskLog = _reflection.GeneratedProtocolMessageType('TaskLog', (_message.Message,), {
  'DESCRIPTOR' : _TASKLOG,
  '__module__' : 'master_pb2'
  # @@protoc_insertion_point(class_scope:experiment_scheduler.task_manager.grpc_task_manager.TaskLog)
  })
_sym_db.RegisterMessage(TaskLog)

TaskLogFile = _reflection.GeneratedProtocolMessageType('TaskLogFile', (_message.Message,), {
  'DESCRIPTOR' : _TASKLOGFILE,
  '__module__' : 'master_pb2'
  # @@protoc_insertion_point(class_scope:experiment_scheduler.task_manager.grpc_task_manager.TaskLogFile)
  })
_sym_db.RegisterMessage(TaskLogFile)

_MASTER = DESCRIPTOR.services_by_name['Master']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\242\002\003RTG'
  _MASTERTASKSTATEMENT_TASKENVENTRY._options = None
  _MASTERTASKSTATEMENT_TASKENVENTRY._serialized_options = b'8\001'
  _EXPERIMENTSTATEMENT._serialized_start=98
  _EXPERIMENTSTATEMENT._serialized_end=222
  _MASTERTASKSTATEMENT._serialized_start=225
  _MASTERTASKSTATEMENT._serialized_end=430
  _MASTERTASKSTATEMENT_TASKENVENTRY._serialized_start=384
  _MASTERTASKSTATEMENT_TASKENVENTRY._serialized_end=430
  _MASTERRESPONSE._serialized_start=433
  _MASTERRESPONSE._serialized_end=615
  _MASTERRESPONSE_RESPONSESTATUS._serialized_start=576
  _MASTERRESPONSE_RESPONSESTATUS._serialized_end=615
  _TASKSTATUS._serialized_start=618
  _TASKSTATUS._serialized_end=822
  _TASKSTATUS_STATUS._serialized_start=737
  _TASKSTATUS_STATUS._serialized_end=822
  _TASK._serialized_start=824
  _TASK._serialized_end=847
  _EXPERIMENT._serialized_start=849
  _EXPERIMENT._serialized_end=884
  _ALLTASKSSTATUS._serialized_start=886
  _ALLTASKSSTATUS._serialized_end=994
  _EXPERIMENTSSTATUS._serialized_start=997
  _EXPERIMENTSSTATUS._serialized_end=1135
  _ALLEXPERIMENTSSTATUS._serialized_start=1137
  _ALLEXPERIMENTSSTATUS._serialized_end=1264
  _TASKLOG._serialized_start=1266
  _TASKLOG._serialized_end=1297
  _TASKLOGFILE._serialized_start=1299
  _TASKLOGFILE._serialized_end=1330
  _MASTER._serialized_start=1333
  _MASTER._serialized_end=2176
# @@protoc_insertion_point(module_scope)
