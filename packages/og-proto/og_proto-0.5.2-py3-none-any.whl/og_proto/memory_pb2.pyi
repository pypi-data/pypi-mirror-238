import prompt_pb2 as _prompt_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GuideMemory(_message.Message):
    __slots__ = ["name", "what_it_can_do", "how_to_use", "recall_time"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    WHAT_IT_CAN_DO_FIELD_NUMBER: _ClassVar[int]
    HOW_TO_USE_FIELD_NUMBER: _ClassVar[int]
    RECALL_TIME_FIELD_NUMBER: _ClassVar[int]
    name: str
    what_it_can_do: str
    how_to_use: str
    recall_time: int
    def __init__(self, name: _Optional[str] = ..., what_it_can_do: _Optional[str] = ..., how_to_use: _Optional[str] = ..., recall_time: _Optional[int] = ...) -> None: ...

class Feedback(_message.Message):
    __slots__ = ["is_correct", "feedback_time"]
    IS_CORRECT_FIELD_NUMBER: _ClassVar[int]
    FEEDBACK_TIME_FIELD_NUMBER: _ClassVar[int]
    is_correct: bool
    feedback_time: int
    def __init__(self, is_correct: bool = ..., feedback_time: _Optional[int] = ...) -> None: ...

class ChatMessage(_message.Message):
    __slots__ = ["role_name", "content", "function_name", "function_call", "chat_time", "feedback"]
    ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_NAME_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_CALL_FIELD_NUMBER: _ClassVar[int]
    CHAT_TIME_FIELD_NUMBER: _ClassVar[int]
    FEEDBACK_FIELD_NUMBER: _ClassVar[int]
    role_name: str
    content: str
    function_name: str
    function_call: str
    chat_time: int
    feedback: Feedback
    def __init__(self, role_name: _Optional[str] = ..., content: _Optional[str] = ..., function_name: _Optional[str] = ..., function_call: _Optional[str] = ..., chat_time: _Optional[int] = ..., feedback: _Optional[_Union[Feedback, _Mapping]] = ...) -> None: ...

class AgentMemory(_message.Message):
    __slots__ = ["instruction", "user_id", "user_name", "guide_memory", "chat_memory", "memory_id"]
    INSTRUCTION_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    USER_NAME_FIELD_NUMBER: _ClassVar[int]
    GUIDE_MEMORY_FIELD_NUMBER: _ClassVar[int]
    CHAT_MEMORY_FIELD_NUMBER: _ClassVar[int]
    MEMORY_ID_FIELD_NUMBER: _ClassVar[int]
    instruction: _prompt_pb2.AgentPrompt
    user_id: str
    user_name: str
    guide_memory: _containers.RepeatedCompositeFieldContainer[GuideMemory]
    chat_memory: _containers.RepeatedCompositeFieldContainer[ChatMessage]
    memory_id: str
    def __init__(self, instruction: _Optional[_Union[_prompt_pb2.AgentPrompt, _Mapping]] = ..., user_id: _Optional[str] = ..., user_name: _Optional[str] = ..., guide_memory: _Optional[_Iterable[_Union[GuideMemory, _Mapping]]] = ..., chat_memory: _Optional[_Iterable[_Union[ChatMessage, _Mapping]]] = ..., memory_id: _Optional[str] = ...) -> None: ...
