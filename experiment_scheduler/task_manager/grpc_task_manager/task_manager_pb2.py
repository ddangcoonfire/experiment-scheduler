# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: task_manager.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12task_manager.proto\x1a\x1bgoogle/protobuf/empty.proto\"4\n\x0cServerStatus\x12\r\n\x05\x61live\x18\x01 \x01(\x08\x12\x15\n\rtask_id_array\x18\x02 \x03(\t\"\x1f\n\rIdleResources\x12\x0e\n\x06\x65xists\x18\x01 \x01(\x08\"\xab\x01\n\rTaskStatement\x12\x0f\n\x07task_id\x18\x01 \x01(\t\x12\x0f\n\x07\x63ommand\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12-\n\x08task_env\x18\x04 \x03(\x0b\x32\x1b.TaskStatement.TaskEnvEntry\x12\x0b\n\x03\x63wd\x18\x05 \x01(\t\x1a.\n\x0cTaskEnvEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xa9\x01\n\nTaskStatus\x12\x0f\n\x07task_id\x18\x01 \x01(\t\x12\"\n\x06status\x18\x02 \x01(\x0e\x32\x12.TaskStatus.Status\"f\n\x06Status\x12\x0c\n\x08NOTSTART\x10\x00\x12\x0b\n\x07RUNNING\x10\x01\x12\x08\n\x04\x44ONE\x10\x02\x12\n\n\x06KILLED\x10\x03\x12\x0c\n\x08\x41\x42NORMAL\x10\x04\x12\x0c\n\x08NOTFOUND\x10\x05\x12\x0f\n\x0bNO_RESOURCE\x10\x06\"\x17\n\x04Task\x12\x0f\n\x07task_id\x18\x01 \x01(\t\":\n\x1cTaskManagerFileUploadRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04\x66ile\x18\x02 \x01(\x0c\",\n\x1cTaskManagerFileDeleteRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"5\n\x0bTaskLogInfo\x12\x0f\n\x07task_id\x18\x01 \x01(\t\x12\x15\n\rlog_file_path\x18\x02 \x01(\t\"8\n\x0e\x41llTasksStatus\x12&\n\x11task_status_array\x18\x01 \x03(\x0b\x32\x0b.TaskStatus\"6\n\x0bTaskLogFile\x12\x10\n\x08log_file\x18\x01 \x01(\x0c\x12\x15\n\rerror_message\x18\x02 \x01(\x0c\">\n\x08Progress\x12\x10\n\x08progress\x18\x01 \x01(\x02\x12\x13\n\x0bleap_second\x18\x02 \x01(\x01\x12\x0b\n\x03pid\x18\x03 \x01(\x05\"v\n\x10ProgressResponse\x12\x39\n\x0freceived_status\x18\x01 \x01(\x0e\x32 .ProgressResponse.ReceivedStatus\"\'\n\x0eReceivedStatus\x12\x0b\n\x07SUCCESS\x10\x00\x12\x08\n\x04\x46\x41IL\x10\x01\x32\xa3\x04\n\x0bTaskManager\x12\x37\n\x0chealth_check\x12\x16.google.protobuf.Empty\x1a\r.ServerStatus\"\x00\x12)\n\x08run_task\x12\x0e.TaskStatement\x1a\x0b.TaskStatus\"\x00\x12.\n\x0cget_task_log\x12\x0c.TaskLogInfo\x1a\x0c.TaskLogFile\"\x00\x30\x01\x12!\n\tkill_task\x12\x05.Task\x1a\x0b.TaskStatus\"\x00\x12\'\n\x0fget_task_status\x12\x05.Task\x1a\x0b.TaskStatus\"\x00\x12:\n\rget_all_tasks\x12\x16.google.protobuf.Empty\x1a\x0f.AllTasksStatus\"\x00\x12=\n\x11has_idle_resource\x12\x16.google.protobuf.Empty\x1a\x0e.IdleResources\"\x00\x12\x31\n\x0freport_progress\x12\t.Progress\x1a\x11.ProgressResponse\"\x00\x12\x43\n\x0bupload_file\x12\x1d.TaskManagerFileUploadRequest\x1a\x11.ProgressResponse\"\x00(\x01\x12\x41\n\x0b\x64\x65lete_file\x12\x1d.TaskManagerFileDeleteRequest\x1a\x11.ProgressResponse\"\x00\x42\x06\xa2\x02\x03RTGb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'task_manager_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\242\002\003RTG'
  _TASKSTATEMENT_TASKENVENTRY._options = None
  _TASKSTATEMENT_TASKENVENTRY._serialized_options = b'8\001'
  _SERVERSTATUS._serialized_start=51
  _SERVERSTATUS._serialized_end=103
  _IDLERESOURCES._serialized_start=105
  _IDLERESOURCES._serialized_end=136
  _TASKSTATEMENT._serialized_start=139
  _TASKSTATEMENT._serialized_end=310
  _TASKSTATEMENT_TASKENVENTRY._serialized_start=264
  _TASKSTATEMENT_TASKENVENTRY._serialized_end=310
  _TASKSTATUS._serialized_start=313
  _TASKSTATUS._serialized_end=482
  _TASKSTATUS_STATUS._serialized_start=380
  _TASKSTATUS_STATUS._serialized_end=482
  _TASK._serialized_start=484
  _TASK._serialized_end=507
  _TASKMANAGERFILEUPLOADREQUEST._serialized_start=509
  _TASKMANAGERFILEUPLOADREQUEST._serialized_end=567
  _TASKMANAGERFILEDELETEREQUEST._serialized_start=569
  _TASKMANAGERFILEDELETEREQUEST._serialized_end=613
  _TASKLOGINFO._serialized_start=615
  _TASKLOGINFO._serialized_end=668
  _ALLTASKSSTATUS._serialized_start=670
  _ALLTASKSSTATUS._serialized_end=726
  _TASKLOGFILE._serialized_start=728
  _TASKLOGFILE._serialized_end=782
  _PROGRESS._serialized_start=784
  _PROGRESS._serialized_end=846
  _PROGRESSRESPONSE._serialized_start=848
  _PROGRESSRESPONSE._serialized_end=966
  _PROGRESSRESPONSE_RECEIVEDSTATUS._serialized_start=927
  _PROGRESSRESPONSE_RECEIVEDSTATUS._serialized_end=966
  _TASKMANAGER._serialized_start=969
  _TASKMANAGER._serialized_end=1516
# @@protoc_insertion_point(module_scope)
