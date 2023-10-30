from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ActionDesc(_message.Message):
    __slots__ = ["name", "desc", "external_script"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESC_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_SCRIPT_FIELD_NUMBER: _ClassVar[int]
    name: str
    desc: str
    external_script: str
    def __init__(self, name: _Optional[str] = ..., desc: _Optional[str] = ..., external_script: _Optional[str] = ...) -> None: ...

class AgentPrompt(_message.Message):
    __slots__ = ["role", "rules", "actions", "output_format", "role_name"]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    RULES_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FORMAT_FIELD_NUMBER: _ClassVar[int]
    ROLE_NAME_FIELD_NUMBER: _ClassVar[int]
    role: str
    rules: _containers.RepeatedScalarFieldContainer[str]
    actions: _containers.RepeatedCompositeFieldContainer[ActionDesc]
    output_format: str
    role_name: str
    def __init__(self, role: _Optional[str] = ..., rules: _Optional[_Iterable[str]] = ..., actions: _Optional[_Iterable[_Union[ActionDesc, _Mapping]]] = ..., output_format: _Optional[str] = ..., role_name: _Optional[str] = ...) -> None: ...
