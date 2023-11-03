from functools import wraps
from pydantic import BaseModel
from agentive.utils.function_calling.common import remove_key_recursive
import json


class FunctionCallSchema(BaseModel):
    @classmethod
    def _generate_schema_parameters(cls):
        schema = cls.model_json_schema()
        relevant_properties = {
            k: v for k, v in schema.items() if k not in ("title", "description")
        }
        required_keys = sorted(
            k for k, v in relevant_properties.items() if "default" not in v
        )
        remove_key_recursive(relevant_properties, "additionalProperties")
        remove_key_recursive(relevant_properties, "title")
        return relevant_properties, required_keys

    @classmethod
    @property
    def function_call_schema(cls):
        relevant_properties, required_keys = cls._generate_schema_parameters()
        schema = {
            "name": cls.__name__,
            "description": cls.__doc__,
            "parameters": relevant_properties,
            "required": required_keys
        }
        return schema

    @classmethod
    def _validate_function_call(cls, message, throw_error=True):
        if throw_error:
            assert "function_call" in message, "No function call detected"
            assert message["function_call"]["name"] == cls.function_call_schema["name"], "Function name does not match"

    @classmethod
    def from_response(cls, completion, throw_error=True):
        message = completion.choices[0].message
        cls._validate_function_call(message, throw_error)
        arguments = json.loads(message["function_call"]["arguments"], strict=False)
        return cls(**arguments)


def function_call_schema(cls):
    if not issubclass(cls, FunctionCallSchema):
        raise TypeError("Class must be a subclass of FunctionCallSchema")

    @wraps(cls, updated=())
    class Wrapper(cls, FunctionCallSchema):
        pass

    return Wrapper
