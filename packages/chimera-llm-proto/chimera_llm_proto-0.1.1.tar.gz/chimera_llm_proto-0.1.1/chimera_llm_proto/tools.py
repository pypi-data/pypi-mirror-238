import json
import uuid
from functools import wraps

from chimera_llm_proto import chimera_llm_pb2


def get_inference_args(inference_args: chimera_llm_pb2.InferenceArgs) -> dict:
    args = {}
    for field in inference_args.DESCRIPTOR.fields:
        v = getattr(inference_args, field.name)
        if v and field.name != "json_extra_args":
            args[field.name] = v
    if inference_args.json_extra_args:
        extra_args = json.loads(inference_args.json_extra_args)
        for k, v in extra_args.items():
            args[k] = v
    return args


def get_uuid() -> str:
    return str(uuid.uuid4())
