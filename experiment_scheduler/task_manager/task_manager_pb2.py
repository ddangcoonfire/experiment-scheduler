# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: task_manager.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12task_manager.proto\x1a\x1bgoogle/protobuf/empty.proto\">\n\rTaskStatement\x12\x0e\n\x06gpuidx\x18\x01 \x01(\x05\x12\x0f\n\x07\x63ommand\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\"\x95\x01\n\x08Response\x12\x0f\n\x07task_id\x18\x01 \x01(\t\x12*\n\x08response\x18\x02 \x01(\x0e\x32\x18.Response.ResponseStatus\"L\n\x0eResponseStatus\x12\t\n\x05READY\x10\x00\x12\x0b\n\x07RUNNING\x10\x01\x12\x08\n\x04\x44ONE\x10\x02\x12\n\n\x06KILLED\x10\x03\x12\x0c\n\x08\x41\x42NORMAL\x10\x04\"\x17\n\x04Task\x12\x0f\n\x07task_id\x18\x01 \x01(\t\"3\n\x0e\x41llTasksStatus\x12!\n\x0eresponse_array\x18\x01 \x03(\x0b\x32\t.Response2\xb4\x01\n\x0bTaskManager\x12&\n\x07RunTask\x12\x0e.TaskStatement\x1a\t.Response\"\x00\x12\x1e\n\x08KillTask\x12\x05.Task\x1a\t.Response\"\x00\x12#\n\rGetTaskStatus\x12\x05.Task\x1a\t.Response\"\x00\x12\x38\n\x0bGetAllTasks\x12\x16.google.protobuf.Empty\x1a\x0f.AllTasksStatus\"\x00\x42\x06\xa2\x02\x03RTGb\x06proto3')



_TASKSTATEMENT = DESCRIPTOR.message_types_by_name['TaskStatement']
_RESPONSE = DESCRIPTOR.message_types_by_name['Response']
_TASK = DESCRIPTOR.message_types_by_name['Task']
_ALLTASKSSTATUS = DESCRIPTOR.message_types_by_name['AllTasksStatus']
_RESPONSE_RESPONSESTATUS = _RESPONSE.enum_types_by_name['ResponseStatus']
TaskStatement = _reflection.GeneratedProtocolMessageType('TaskStatement', (_message.Message,), {
  'DESCRIPTOR' : _TASKSTATEMENT,
  '__module__' : 'task_manager_pb2'
  # @@protoc_insertion_point(class_scope:TaskStatement)
  })
_sym_db.RegisterMessage(TaskStatement)

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), {
  'DESCRIPTOR' : _RESPONSE,
  '__module__' : 'task_manager_pb2'
  # @@protoc_insertion_point(class_scope:Response)
  })
_sym_db.RegisterMessage(Response)

Task = _reflection.GeneratedProtocolMessageType('Task', (_message.Message,), {
  'DESCRIPTOR' : _TASK,
  '__module__' : 'task_manager_pb2'
  # @@protoc_insertion_point(class_scope:Task)
  })
_sym_db.RegisterMessage(Task)

AllTasksStatus = _reflection.GeneratedProtocolMessageType('AllTasksStatus', (_message.Message,), {
  'DESCRIPTOR' : _ALLTASKSSTATUS,
  '__module__' : 'task_manager_pb2'
  # @@protoc_insertion_point(class_scope:AllTasksStatus)
  })
_sym_db.RegisterMessage(AllTasksStatus)

_TASKMANAGER = DESCRIPTOR.services_by_name['TaskManager']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\242\002\003RTG'
  _TASKSTATEMENT._serialized_start=51
  _TASKSTATEMENT._serialized_end=113
  _RESPONSE._serialized_start=116
  _RESPONSE._serialized_end=265
  _RESPONSE_RESPONSESTATUS._serialized_start=189
  _RESPONSE_RESPONSESTATUS._serialized_end=265
  _TASK._serialized_start=267
  _TASK._serialized_end=290
  _ALLTASKSSTATUS._serialized_start=292
  _ALLTASKSSTATUS._serialized_end=343
  _TASKMANAGER._serialized_start=346
  _TASKMANAGER._serialized_end=526
# @@protoc_insertion_point(module_scope)
