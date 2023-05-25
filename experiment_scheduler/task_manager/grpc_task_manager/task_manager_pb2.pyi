from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class AllTasksStatus(_message.Message):
    __slots__ = ["task_status_array"]
    TASK_STATUS_ARRAY_FIELD_NUMBER: _ClassVar[int]
    task_status_array: _containers.RepeatedCompositeFieldContainer[TaskStatus]
    def __init__(
        self,
        task_status_array: _Optional[_Iterable[_Union[TaskStatus, _Mapping]]] = ...,
    ) -> None: ...

class IdleResources(_message.Message):
    __slots__ = ["exists"]
    EXISTS_FIELD_NUMBER: _ClassVar[int]
    exists: bool
    def __init__(self, exists: bool = ...) -> None: ...

class Progress(_message.Message):
    __slots__ = ["leap_second", "pid", "progress"]
    LEAP_SECOND_FIELD_NUMBER: _ClassVar[int]
    PID_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    leap_second: float
    pid: int
    progress: float
    def __init__(
        self,
        progress: _Optional[float] = ...,
        leap_second: _Optional[float] = ...,
        pid: _Optional[int] = ...,
    ) -> None: ...

class ProgressResponse(_message.Message):
    __slots__ = ["received_status"]

    class ReceivedStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    FAIL: ProgressResponse.ReceivedStatus
    RECEIVED_STATUS_FIELD_NUMBER: _ClassVar[int]
    SUCCESS: ProgressResponse.ReceivedStatus
    received_status: ProgressResponse.ReceivedStatus
    def __init__(
        self,
        received_status: _Optional[_Union[ProgressResponse.ReceivedStatus, str]] = ...,
    ) -> None: ...

class ServerStatus(_message.Message):
    __slots__ = ["alive", "task_id_array"]
    ALIVE_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_ARRAY_FIELD_NUMBER: _ClassVar[int]
    alive: bool
    task_id_array: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self, alive: bool = ..., task_id_array: _Optional[_Iterable[str]] = ...
    ) -> None: ...

class Task(_message.Message):
    __slots__ = ["task_id"]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    def __init__(self, task_id: _Optional[str] = ...) -> None: ...

class TaskLogFile(_message.Message):
    __slots__ = ["error_message", "log_file"]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LOG_FILE_FIELD_NUMBER: _ClassVar[int]
    error_message: bytes
    log_file: bytes
    def __init__(
        self, log_file: _Optional[bytes] = ..., error_message: _Optional[bytes] = ...
    ) -> None: ...

class TaskLogInfo(_message.Message):
    __slots__ = ["log_file_path", "task_id"]
    LOG_FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    log_file_path: str
    task_id: str
    def __init__(
        self, task_id: _Optional[str] = ..., log_file_path: _Optional[str] = ...
    ) -> None: ...

class TaskManagerFileDeleteRequest(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class TaskManagerFileUploadRequest(_message.Message):
    __slots__ = ["file", "name"]
    FILE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    file: bytes
    name: str
    def __init__(
        self, name: _Optional[str] = ..., file: _Optional[bytes] = ...
    ) -> None: ...

class TaskStatement(_message.Message):
    __slots__ = ["command", "cwd", "name", "task_env", "task_id"]

    class TaskEnvEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[str] = ...
        ) -> None: ...
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    CWD_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TASK_ENV_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    command: str
    cwd: str
    name: str
    task_env: _containers.ScalarMap[str, str]
    task_id: str
    def __init__(
        self,
        task_id: _Optional[str] = ...,
        command: _Optional[str] = ...,
        name: _Optional[str] = ...,
        task_env: _Optional[_Mapping[str, str]] = ...,
        cwd: _Optional[str] = ...,
    ) -> None: ...

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
    def __init__(
        self,
        task_id: _Optional[str] = ...,
        status: _Optional[_Union[TaskStatus.Status, str]] = ...,
    ) -> None: ...
