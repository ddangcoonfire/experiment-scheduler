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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cmaster.proto\"H\n\x13\x45xperimentStatement\x12\x0c\n\x04name\x18\x01 \x01(\t\x12#\n\x05tasks\x18\x02 \x03(\x0b\x32\x14.MasterTaskStatement\"\x99\x01\n\x13MasterTaskStatement\x12\x0f\n\x07\x63ommand\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x33\n\x08task_env\x18\x04 \x03(\x0b\x32!.MasterTaskStatement.TaskEnvEntry\x1a.\n\x0cTaskEnvEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x82\x01\n\x0eMasterResponse\x12\x15\n\rexperiment_id\x18\x01 \x01(\t\x12\x30\n\x08response\x18\x02 \x01(\x0e\x32\x1e.MasterResponse.ResponseStatus\"\'\n\x0eResponseStatus\x12\x0b\n\x07SUCCESS\x10\x00\x12\x08\n\x04\x46\x41IL\x10\x01\x32H\n\x06Master\x12>\n\x13request_experiments\x12\x14.ExperimentStatement\x1a\x0f.MasterResponse\"\x00\x42\x06\xa2\x02\x03RTGb\x06proto3')



_EXPERIMENTSTATEMENT = DESCRIPTOR.message_types_by_name['ExperimentStatement']
_MASTERTASKSTATEMENT = DESCRIPTOR.message_types_by_name['MasterTaskStatement']
_MASTERTASKSTATEMENT_TASKENVENTRY = _MASTERTASKSTATEMENT.nested_types_by_name['TaskEnvEntry']
_MASTERRESPONSE = DESCRIPTOR.message_types_by_name['MasterResponse']
_MASTERRESPONSE_RESPONSESTATUS = _MASTERRESPONSE.enum_types_by_name['ResponseStatus']
ExperimentStatement = _reflection.GeneratedProtocolMessageType('ExperimentStatement', (_message.Message,), {
  'DESCRIPTOR' : _EXPERIMENTSTATEMENT,
  '__module__' : 'master_pb2'
  # @@protoc_insertion_point(class_scope:ExperimentStatement)
  })
_sym_db.RegisterMessage(ExperimentStatement)

MasterTaskStatement = _reflection.GeneratedProtocolMessageType('MasterTaskStatement', (_message.Message,), {

  'TaskEnvEntry' : _reflection.GeneratedProtocolMessageType('TaskEnvEntry', (_message.Message,), {
    'DESCRIPTOR' : _MASTERTASKSTATEMENT_TASKENVENTRY,
    '__module__' : 'master_pb2'
    # @@protoc_insertion_point(class_scope:MasterTaskStatement.TaskEnvEntry)
    })
  ,
  'DESCRIPTOR' : _MASTERTASKSTATEMENT,
  '__module__' : 'master_pb2'
  # @@protoc_insertion_point(class_scope:MasterTaskStatement)
  })
_sym_db.RegisterMessage(MasterTaskStatement)
_sym_db.RegisterMessage(MasterTaskStatement.TaskEnvEntry)

MasterResponse = _reflection.GeneratedProtocolMessageType('MasterResponse', (_message.Message,), {
  'DESCRIPTOR' : _MASTERRESPONSE,
  '__module__' : 'master_pb2'
  # @@protoc_insertion_point(class_scope:MasterResponse)
  })
_sym_db.RegisterMessage(MasterResponse)

_MASTER = DESCRIPTOR.services_by_name['Master']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\242\002\003RTG'
  _MASTERTASKSTATEMENT_TASKENVENTRY._options = None
  _MASTERTASKSTATEMENT_TASKENVENTRY._serialized_options = b'8\001'
  _EXPERIMENTSTATEMENT._serialized_start=16
  _EXPERIMENTSTATEMENT._serialized_end=88
  _MASTERTASKSTATEMENT._serialized_start=91
  _MASTERTASKSTATEMENT._serialized_end=244
  _MASTERTASKSTATEMENT_TASKENVENTRY._serialized_start=198
  _MASTERTASKSTATEMENT_TASKENVENTRY._serialized_end=244
  _MASTERRESPONSE._serialized_start=247
  _MASTERRESPONSE._serialized_end=377
  _MASTERRESPONSE_RESPONSESTATUS._serialized_start=338
  _MASTERRESPONSE_RESPONSESTATUS._serialized_end=377
  _MASTER._serialized_start=379
  _MASTER._serialized_end=451
# @@protoc_insertion_point(module_scope)