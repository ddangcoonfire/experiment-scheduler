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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cmaster.proto\"B\n\x13\x45xperimentStatement\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x1d\n\x05tasks\x18\x02 \x03(\x0b\x32\x0e.TaskStatement\"Q\n\rTaskStatement\x12\x0f\n\x07\x63ommand\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12!\n\tcondition\x18\x03 \x01(\x0b\x32\x0e.TaskCondition\"\x1f\n\rTaskCondition\x12\x0e\n\x06gpuidx\x18\x01 \x01(\x03\"v\n\x08Response\x12\x15\n\rexperiment_id\x18\x01 \x01(\t\x12*\n\x08response\x18\x02 \x01(\x0e\x32\x18.Response.ResponseStatus\"\'\n\x0eResponseStatus\x12\x0b\n\x07SUCCESS\x10\x00\x12\x08\n\x04\x46\x41IL\x10\x01\x32\x42\n\x06Master\x12\x38\n\x13request_experiments\x12\x14.ExperimentStatement\x1a\t.Response\"\x00\x42\x06\xa2\x02\x03RTGb\x06proto3')



_EXPERIMENTSTATEMENT = DESCRIPTOR.message_types_by_name['ExperimentStatement']
_TASKSTATEMENT = DESCRIPTOR.message_types_by_name['TaskStatement']
_TASKCONDITION = DESCRIPTOR.message_types_by_name['TaskCondition']
_RESPONSE = DESCRIPTOR.message_types_by_name['Response']
_RESPONSE_RESPONSESTATUS = _RESPONSE.enum_types_by_name['ResponseStatus']
ExperimentStatement = _reflection.GeneratedProtocolMessageType('ExperimentStatement', (_message.Message,), {
  'DESCRIPTOR' : _EXPERIMENTSTATEMENT,
  '__module__' : 'master_pb2'
  # @@protoc_insertion_point(class_scope:ExperimentStatement)
  })
_sym_db.RegisterMessage(ExperimentStatement)

TaskStatement = _reflection.GeneratedProtocolMessageType('TaskStatement', (_message.Message,), {
  'DESCRIPTOR' : _TASKSTATEMENT,
  '__module__' : 'master_pb2'
  # @@protoc_insertion_point(class_scope:TaskStatement)
  })
_sym_db.RegisterMessage(TaskStatement)

TaskCondition = _reflection.GeneratedProtocolMessageType('TaskCondition', (_message.Message,), {
  'DESCRIPTOR' : _TASKCONDITION,
  '__module__' : 'master_pb2'
  # @@protoc_insertion_point(class_scope:TaskCondition)
  })
_sym_db.RegisterMessage(TaskCondition)

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), {
  'DESCRIPTOR' : _RESPONSE,
  '__module__' : 'master_pb2'
  # @@protoc_insertion_point(class_scope:Response)
  })
_sym_db.RegisterMessage(Response)

_MASTER = DESCRIPTOR.services_by_name['Master']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\242\002\003RTG'
  _EXPERIMENTSTATEMENT._serialized_start=16
  _EXPERIMENTSTATEMENT._serialized_end=82
  _TASKSTATEMENT._serialized_start=84
  _TASKSTATEMENT._serialized_end=165
  _TASKCONDITION._serialized_start=167
  _TASKCONDITION._serialized_end=198
  _RESPONSE._serialized_start=200
  _RESPONSE._serialized_end=318
  _RESPONSE_RESPONSESTATUS._serialized_start=279
  _RESPONSE_RESPONSESTATUS._serialized_end=318
  _MASTER._serialized_start=320
  _MASTER._serialized_end=386
# @@protoc_insertion_point(module_scope)
