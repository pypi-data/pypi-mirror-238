import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProcessOptions(_message.Message):
    __slots__ = ["streaming", "llm_name", "input_token_limit", "output_token_limit", "timeout"]
    STREAMING_FIELD_NUMBER: _ClassVar[int]
    LLM_NAME_FIELD_NUMBER: _ClassVar[int]
    INPUT_TOKEN_LIMIT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_TOKEN_LIMIT_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    streaming: bool
    llm_name: str
    input_token_limit: int
    output_token_limit: int
    timeout: int
    def __init__(self, streaming: bool = ..., llm_name: _Optional[str] = ..., input_token_limit: _Optional[int] = ..., output_token_limit: _Optional[int] = ..., timeout: _Optional[int] = ...) -> None: ...

class ProcessTaskRequest(_message.Message):
    __slots__ = ["input_files", "task", "context_id", "options"]
    INPUT_FILES_FIELD_NUMBER: _ClassVar[int]
    TASK_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_ID_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    input_files: _containers.RepeatedScalarFieldContainer[str]
    task: str
    context_id: str
    options: ProcessOptions
    def __init__(self, input_files: _Optional[_Iterable[str]] = ..., task: _Optional[str] = ..., context_id: _Optional[str] = ..., options: _Optional[_Union[ProcessOptions, _Mapping]] = ...) -> None: ...

class OnStepActionStart(_message.Message):
    __slots__ = ["input", "tool"]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    TOOL_FIELD_NUMBER: _ClassVar[int]
    input: str
    tool: str
    def __init__(self, input: _Optional[str] = ..., tool: _Optional[str] = ...) -> None: ...

class OnStepActionEnd(_message.Message):
    __slots__ = ["output", "output_files", "has_error"]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FILES_FIELD_NUMBER: _ClassVar[int]
    HAS_ERROR_FIELD_NUMBER: _ClassVar[int]
    output: str
    output_files: _containers.RepeatedScalarFieldContainer[str]
    has_error: bool
    def __init__(self, output: _Optional[str] = ..., output_files: _Optional[_Iterable[str]] = ..., has_error: bool = ...) -> None: ...

class FinalAnswer(_message.Message):
    __slots__ = ["answer"]
    ANSWER_FIELD_NUMBER: _ClassVar[int]
    answer: str
    def __init__(self, answer: _Optional[str] = ...) -> None: ...

class ContextState(_message.Message):
    __slots__ = ["output_token_count", "input_token_count", "llm_name", "total_duration", "llm_response_duration"]
    OUTPUT_TOKEN_COUNT_FIELD_NUMBER: _ClassVar[int]
    INPUT_TOKEN_COUNT_FIELD_NUMBER: _ClassVar[int]
    LLM_NAME_FIELD_NUMBER: _ClassVar[int]
    TOTAL_DURATION_FIELD_NUMBER: _ClassVar[int]
    LLM_RESPONSE_DURATION_FIELD_NUMBER: _ClassVar[int]
    output_token_count: int
    input_token_count: int
    llm_name: str
    total_duration: int
    llm_response_duration: int
    def __init__(self, output_token_count: _Optional[int] = ..., input_token_count: _Optional[int] = ..., llm_name: _Optional[str] = ..., total_duration: _Optional[int] = ..., llm_response_duration: _Optional[int] = ...) -> None: ...

class TypingContent(_message.Message):
    __slots__ = ["content", "language"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    content: str
    language: str
    def __init__(self, content: _Optional[str] = ..., language: _Optional[str] = ...) -> None: ...

class TaskResponse(_message.Message):
    __slots__ = ["state", "response_type", "on_step_action_start", "on_step_action_end", "final_answer", "console_stdout", "console_stderr", "error_msg", "typing_content"]
    class ResponseType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        OnStepActionStart: _ClassVar[TaskResponse.ResponseType]
        OnStepActionStreamStdout: _ClassVar[TaskResponse.ResponseType]
        OnStepActionStreamStderr: _ClassVar[TaskResponse.ResponseType]
        OnStepActionEnd: _ClassVar[TaskResponse.ResponseType]
        OnFinalAnswer: _ClassVar[TaskResponse.ResponseType]
        OnModelTypeText: _ClassVar[TaskResponse.ResponseType]
        OnModelTypeCode: _ClassVar[TaskResponse.ResponseType]
        OnModelOutputError: _ClassVar[TaskResponse.ResponseType]
        OnInputTokenLimitExceed: _ClassVar[TaskResponse.ResponseType]
        OnOutputTokenLimitExceed: _ClassVar[TaskResponse.ResponseType]
        OnSystemError: _ClassVar[TaskResponse.ResponseType]
    OnStepActionStart: TaskResponse.ResponseType
    OnStepActionStreamStdout: TaskResponse.ResponseType
    OnStepActionStreamStderr: TaskResponse.ResponseType
    OnStepActionEnd: TaskResponse.ResponseType
    OnFinalAnswer: TaskResponse.ResponseType
    OnModelTypeText: TaskResponse.ResponseType
    OnModelTypeCode: TaskResponse.ResponseType
    OnModelOutputError: TaskResponse.ResponseType
    OnInputTokenLimitExceed: TaskResponse.ResponseType
    OnOutputTokenLimitExceed: TaskResponse.ResponseType
    OnSystemError: TaskResponse.ResponseType
    STATE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ON_STEP_ACTION_START_FIELD_NUMBER: _ClassVar[int]
    ON_STEP_ACTION_END_FIELD_NUMBER: _ClassVar[int]
    FINAL_ANSWER_FIELD_NUMBER: _ClassVar[int]
    CONSOLE_STDOUT_FIELD_NUMBER: _ClassVar[int]
    CONSOLE_STDERR_FIELD_NUMBER: _ClassVar[int]
    ERROR_MSG_FIELD_NUMBER: _ClassVar[int]
    TYPING_CONTENT_FIELD_NUMBER: _ClassVar[int]
    state: ContextState
    response_type: TaskResponse.ResponseType
    on_step_action_start: OnStepActionStart
    on_step_action_end: OnStepActionEnd
    final_answer: FinalAnswer
    console_stdout: str
    console_stderr: str
    error_msg: str
    typing_content: TypingContent
    def __init__(self, state: _Optional[_Union[ContextState, _Mapping]] = ..., response_type: _Optional[_Union[TaskResponse.ResponseType, str]] = ..., on_step_action_start: _Optional[_Union[OnStepActionStart, _Mapping]] = ..., on_step_action_end: _Optional[_Union[OnStepActionEnd, _Mapping]] = ..., final_answer: _Optional[_Union[FinalAnswer, _Mapping]] = ..., console_stdout: _Optional[str] = ..., console_stderr: _Optional[str] = ..., error_msg: _Optional[str] = ..., typing_content: _Optional[_Union[TypingContent, _Mapping]] = ...) -> None: ...

class AddKernelRequest(_message.Message):
    __slots__ = ["endpoint", "key"]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    endpoint: str
    key: str
    def __init__(self, endpoint: _Optional[str] = ..., key: _Optional[str] = ...) -> None: ...

class AddKernelResponse(_message.Message):
    __slots__ = ["code", "msg"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    code: int
    msg: str
    def __init__(self, code: _Optional[int] = ..., msg: _Optional[str] = ...) -> None: ...

class AssembleAppRequest(_message.Message):
    __slots__ = ["name", "language", "code", "saved_filenames", "desc"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    SAVED_FILENAMES_FIELD_NUMBER: _ClassVar[int]
    DESC_FIELD_NUMBER: _ClassVar[int]
    name: str
    language: str
    code: str
    saved_filenames: _containers.RepeatedScalarFieldContainer[str]
    desc: str
    def __init__(self, name: _Optional[str] = ..., language: _Optional[str] = ..., code: _Optional[str] = ..., saved_filenames: _Optional[_Iterable[str]] = ..., desc: _Optional[str] = ...) -> None: ...

class AssembleAppResponse(_message.Message):
    __slots__ = ["code", "msg"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    code: int
    msg: str
    def __init__(self, code: _Optional[int] = ..., msg: _Optional[str] = ...) -> None: ...

class RunAppRequest(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class AppInfo(_message.Message):
    __slots__ = ["name", "language", "ctime", "desc"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    CTIME_FIELD_NUMBER: _ClassVar[int]
    DESC_FIELD_NUMBER: _ClassVar[int]
    name: str
    language: str
    ctime: int
    desc: str
    def __init__(self, name: _Optional[str] = ..., language: _Optional[str] = ..., ctime: _Optional[int] = ..., desc: _Optional[str] = ...) -> None: ...

class QueryAppsRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class QueryAppsResponse(_message.Message):
    __slots__ = ["apps"]
    APPS_FIELD_NUMBER: _ClassVar[int]
    apps: _containers.RepeatedCompositeFieldContainer[AppInfo]
    def __init__(self, apps: _Optional[_Iterable[_Union[AppInfo, _Mapping]]] = ...) -> None: ...

class PingRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class PongResponse(_message.Message):
    __slots__ = ["code", "msg"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    code: int
    msg: str
    def __init__(self, code: _Optional[int] = ..., msg: _Optional[str] = ...) -> None: ...
