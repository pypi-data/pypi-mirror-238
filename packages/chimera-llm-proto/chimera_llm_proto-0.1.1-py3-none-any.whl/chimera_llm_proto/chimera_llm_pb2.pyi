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

class ModelTag(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    MODEL_TYPE_UNKNOWN: _ClassVar[ModelTag]
    GENERAL: _ClassVar[ModelTag]
    CHAT: _ClassVar[ModelTag]
    TEXT: _ClassVar[ModelTag]
    CODE: _ClassVar[ModelTag]

class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    STATUS_UNKNOWN: _ClassVar[Status]
    INITLIZING: _ClassVar[Status]
    READY: _ClassVar[Status]
    ERROR: _ClassVar[Status]

class Role(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    ROLE_UNKNOWN: _ClassVar[Role]
    SYSTEM: _ClassVar[Role]
    USER: _ClassVar[Role]
    ASSISTANT: _ClassVar[Role]

MODEL_TYPE_UNKNOWN: ModelTag
GENERAL: ModelTag
CHAT: ModelTag
TEXT: ModelTag
CODE: ModelTag
STATUS_UNKNOWN: Status
INITLIZING: Status
READY: Status
ERROR: Status
ROLE_UNKNOWN: Role
SYSTEM: Role
USER: Role
ASSISTANT: Role

class InspectRequest(_message.Message):
    __slots__ = ["report_duration"]
    REPORT_DURATION_FIELD_NUMBER: _ClassVar[int]
    report_duration: int
    def __init__(self, report_duration: _Optional[int] = ...) -> None: ...

class AvaliableModel(_message.Message):
    __slots__ = ["model_tagas", "model_id", "model_name", "size", "model_description"]
    MODEL_TAGAS_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    MODEL_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    model_tagas: _containers.RepeatedScalarFieldContainer[ModelTag]
    model_id: int
    model_name: str
    size: str
    model_description: str
    def __init__(
        self,
        model_tagas: _Optional[_Iterable[_Union[ModelTag, str]]] = ...,
        model_id: _Optional[int] = ...,
        model_name: _Optional[str] = ...,
        size: _Optional[str] = ...,
        model_description: _Optional[str] = ...,
    ) -> None: ...

class InspectResponse(_message.Message):
    __slots__ = ["avaliable_models", "current_status", "current_model"]
    AVALIABLE_MODELS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_STATUS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_MODEL_FIELD_NUMBER: _ClassVar[int]
    avaliable_models: _containers.RepeatedCompositeFieldContainer[AvaliableModel]
    current_status: Status
    current_model: AvaliableModel
    def __init__(
        self,
        avaliable_models: _Optional[_Iterable[_Union[AvaliableModel, _Mapping]]] = ...,
        current_status: _Optional[_Union[Status, str]] = ...,
        current_model: _Optional[_Union[AvaliableModel, _Mapping]] = ...,
    ) -> None: ...

class LoadModelRequest(_message.Message):
    __slots__ = ["model_id", "json_model_param"]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    JSON_MODEL_PARAM_FIELD_NUMBER: _ClassVar[int]
    model_id: int
    json_model_param: str
    def __init__(
        self, model_id: _Optional[int] = ..., json_model_param: _Optional[str] = ...
    ) -> None: ...

class LoadModelResponse(_message.Message):
    __slots__ = ["current_status", "current_model"]
    CURRENT_STATUS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_MODEL_FIELD_NUMBER: _ClassVar[int]
    current_status: Status
    current_model: AvaliableModel
    def __init__(
        self,
        current_status: _Optional[_Union[Status, str]] = ...,
        current_model: _Optional[_Union[AvaliableModel, _Mapping]] = ...,
    ) -> None: ...

class InferenceArgs(_message.Message):
    __slots__ = ["temperature", "top_p", "max_gen_len", "repetition_penalty", "json_extra_args"]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    TOP_P_FIELD_NUMBER: _ClassVar[int]
    MAX_GEN_LEN_FIELD_NUMBER: _ClassVar[int]
    REPETITION_PENALTY_FIELD_NUMBER: _ClassVar[int]
    JSON_EXTRA_ARGS_FIELD_NUMBER: _ClassVar[int]
    temperature: float
    top_p: float
    max_gen_len: int
    repetition_penalty: int
    json_extra_args: str
    def __init__(
        self,
        temperature: _Optional[float] = ...,
        top_p: _Optional[float] = ...,
        max_gen_len: _Optional[int] = ...,
        repetition_penalty: _Optional[int] = ...,
        json_extra_args: _Optional[str] = ...,
    ) -> None: ...

class CompletionRequest(_message.Message):
    __slots__ = ["request_id", "prompt", "inference_args"]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    INFERENCE_ARGS_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    prompt: str
    inference_args: InferenceArgs
    def __init__(
        self,
        request_id: _Optional[str] = ...,
        prompt: _Optional[str] = ...,
        inference_args: _Optional[_Union[InferenceArgs, _Mapping]] = ...,
    ) -> None: ...

class CompletionPrediction(_message.Message):
    __slots__ = ["request_id", "response_id", "generation"]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_ID_FIELD_NUMBER: _ClassVar[int]
    GENERATION_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    response_id: str
    generation: str
    def __init__(
        self,
        request_id: _Optional[str] = ...,
        response_id: _Optional[str] = ...,
        generation: _Optional[str] = ...,
    ) -> None: ...

class ChatMessage(_message.Message):
    __slots__ = ["role", "content"]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    role: Role
    content: str
    def __init__(
        self, role: _Optional[_Union[Role, str]] = ..., content: _Optional[str] = ...
    ) -> None: ...

class ChatRequest(_message.Message):
    __slots__ = ["request_id", "messages", "inference_args"]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    INFERENCE_ARGS_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    messages: _containers.RepeatedCompositeFieldContainer[ChatMessage]
    inference_args: InferenceArgs
    def __init__(
        self,
        request_id: _Optional[str] = ...,
        messages: _Optional[_Iterable[_Union[ChatMessage, _Mapping]]] = ...,
        inference_args: _Optional[_Union[InferenceArgs, _Mapping]] = ...,
    ) -> None: ...

class ChatPrediction(_message.Message):
    __slots__ = ["request_id", "response_id", "message"]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    response_id: str
    message: ChatMessage
    def __init__(
        self,
        request_id: _Optional[str] = ...,
        response_id: _Optional[str] = ...,
        message: _Optional[_Union[ChatMessage, _Mapping]] = ...,
    ) -> None: ...
