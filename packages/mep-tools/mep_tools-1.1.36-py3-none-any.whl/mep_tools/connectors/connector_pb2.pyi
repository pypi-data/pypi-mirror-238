from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DispatcherRequest(_message.Message):
    __slots__ = ["payload"]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    payload: str
    def __init__(self, payload: _Optional[str] = ...) -> None: ...

class DispatcherResponse(_message.Message):
    __slots__ = ["payload"]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    payload: str
    def __init__(self, payload: _Optional[str] = ...) -> None: ...
