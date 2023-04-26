from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AllExperimentsStatus(_message.Message):
    __slots__ = ["experiment_status_array"]
    EXPERIMENT_STATUS_ARRAY_FIELD_NUMBER: _ClassVar[int]
    experiment_status_array: _containers.RepeatedCompositeFieldContainer[ExperimentsStatus]
    def __init__(self, experiment_status_array: _Optional[_Iterable[_Union[ExperimentsStatus, _Mapping]]] = ...) -> None: ...

class AllTasksStatus(_message.Message):
    __slots__ = ["task_status_array"]
    TASK_STATUS_ARRAY_FIELD_NUMBER: _ClassVar[int]
    task_status_array: _containers.RepeatedCompositeFieldContainer[TaskStatus]
    def __init__(self, task_status_array: _Optional[_Iterable[_Union[TaskStatus, _Mapping]]] = ...) -> None: ...

class EditTask(_message.Message):
    __slots__ = ["cmd", "task_env", "task_id"]
    class TaskEnvEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CMD_FIELD_NUMBER: _ClassVar[int]
    TASK_ENV_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    cmd: str
    task_env: _containers.ScalarMap[str, str]
    task_id: str
    def __init__(self, task_id: _Optional[str] = ..., cmd: _Optional[str] = ..., task_env: _Optional[_Mapping[str, str]] = ...) -> None: ...

class Experiment(_message.Message):
    __slots__ = ["experiment_id"]
    EXPERIMENT_ID_FIELD_NUMBER: _ClassVar[int]
    experiment_id: str
    def __init__(self, experiment_id: _Optional[str] = ...) -> None: ...

class ExperimentStatement(_message.Message):
    __slots__ = ["name", "tasks"]
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    ABNORMAL: ExperimentStatement.Status
    DONE: ExperimentStatement.Status
    KILLED: ExperimentStatement.Status
    NAME_FIELD_NUMBER: _ClassVar[int]
    NOTFOUND: ExperimentStatement.Status
    NOTSTART: ExperimentStatement.Status
    NO_RESOURCE: ExperimentStatement.Status
    RUNNING: ExperimentStatement.Status
    TASKS_FIELD_NUMBER: _ClassVar[int]
    name: str
    tasks: _containers.RepeatedCompositeFieldContainer[MasterTaskStatement]
    def __init__(self, name: _Optional[str] = ..., tasks: _Optional[_Iterable[_Union[MasterTaskStatement, _Mapping]]] = ...) -> None: ...

class ExperimentsStatus(_message.Message):
    __slots__ = ["experiment_id", "task_status_array"]
    EXPERIMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TASK_STATUS_ARRAY_FIELD_NUMBER: _ClassVar[int]
    experiment_id: str
    task_status_array: AllTasksStatus
    def __init__(self, experiment_id: _Optional[str] = ..., task_status_array: _Optional[_Union[AllTasksStatus, _Mapping]] = ...) -> None: ...

class MasterResponse(_message.Message):
    __slots__ = ["experiment_id", "response"]
    class ResponseStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    EXPERIMENT_ID_FIELD_NUMBER: _ClassVar[int]
    FAIL: MasterResponse.ResponseStatus
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS: MasterResponse.ResponseStatus
    experiment_id: str
    response: MasterResponse.ResponseStatus
    def __init__(self, experiment_id: _Optional[str] = ..., response: _Optional[_Union[MasterResponse.ResponseStatus, str]] = ...) -> None: ...

class MasterTaskStatement(_message.Message):
    __slots__ = ["command", "name", "task_env"]
    class TaskEnvEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TASK_ENV_FIELD_NUMBER: _ClassVar[int]
    command: str
    name: str
    task_env: _containers.ScalarMap[str, str]
    def __init__(self, command: _Optional[str] = ..., name: _Optional[str] = ..., task_env: _Optional[_Mapping[str, str]] = ...) -> None: ...

class RequestAbnormalExitedTasksResponse(_message.Message):
    __slots__ = ["not_running_tasks", "response"]
    class ResponseStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    FAIL: RequestAbnormalExitedTasksResponse.ResponseStatus
    NOT_RUNNING_TASKS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS: RequestAbnormalExitedTasksResponse.ResponseStatus
    not_running_tasks: TaskList
    response: RequestAbnormalExitedTasksResponse.ResponseStatus
    def __init__(self, not_running_tasks: _Optional[_Union[TaskList, _Mapping]] = ..., response: _Optional[_Union[RequestAbnormalExitedTasksResponse.ResponseStatus, str]] = ...) -> None: ...

class Task(_message.Message):
    __slots__ = ["task_id"]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    def __init__(self, task_id: _Optional[str] = ...) -> None: ...

class TaskList(_message.Message):
    __slots__ = ["task_list"]
    TASK_LIST_FIELD_NUMBER: _ClassVar[int]
    task_list: _containers.RepeatedCompositeFieldContainer[Task]
    def __init__(self, task_list: _Optional[_Iterable[_Union[Task, _Mapping]]] = ...) -> None: ...

class TaskLog(_message.Message):
    __slots__ = ["logfile_path"]
    LOGFILE_PATH_FIELD_NUMBER: _ClassVar[int]
    logfile_path: str
    def __init__(self, logfile_path: _Optional[str] = ...) -> None: ...

class TaskLogFile(_message.Message):
    __slots__ = ["error_message", "log_file"]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LOG_FILE_FIELD_NUMBER: _ClassVar[int]
    error_message: bytes
    log_file: bytes
    def __init__(self, log_file: _Optional[bytes] = ..., error_message: _Optional[bytes] = ...) -> None: ...

class TaskStatus(_message.Message):
    __slots__ = ["status", "task_id"]
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    ABNORMAL: TaskStatus.Status
    DONE: TaskStatus.Status
    KILLED: TaskStatus.Status
    NOTFOUND: TaskStatus.Status
    NOTSTART: TaskStatus.Status
    NO_RESOURCE: TaskStatus.Status
    RUNNING: TaskStatus.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    status: TaskStatus.Status
    task_id: str
    def __init__(self, task_id: _Optional[str] = ..., status: _Optional[_Union[TaskStatus.Status, str]] = ...) -> None: ...
