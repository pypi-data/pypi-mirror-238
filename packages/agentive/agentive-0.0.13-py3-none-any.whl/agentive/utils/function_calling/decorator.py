from typing import Callable, Any
from functools import wraps
import json
from pydantic import validate_arguments
from agentive.utils.function_calling.common import remove_key_recursive


class function_call:
    """
    INSPIRED BY JASON LIU'S OPENAI_FUNCTION_CALL PACKAGE

    Decorator to convert a function into a function call for an LLM.

    This decorator will convert a function into a function call for an LLM. The
    function will be validated using pydantic and the schema will be
    generated from the function signature.

    Example:
        ```python
        @function_call
        def sum(a: int, b: int) -> int:
            return a + b

        completion = openai.ChatCompletion.create(
            ...
            messages=[{
                "content": "What is 1 + 1?",
                "role": "user"
            }]
        )
        sum.from_response(completion)
        # 2
        ```
    """

    def __init__(self, func: Callable) -> None:
        self.func = func
        self.validate_func = validate_arguments(func)
        self.function_call_schema = self._generate_function_call_schema()
        self.model = self.validate_func.model

    def _generate_function_call_schema(self):
        schema = self.validate_func.model.model_json_schema()
        relevant_properties = {
            k: v for k, v in schema["properties"].items()
            if k not in ("v__duplicate_kwargs", "args", "kwargs")
        }

        schema["properties"] = relevant_properties

        schema["required"] = sorted(
            k for k, v in relevant_properties.items() if "default" not in v
        )
        remove_key_recursive(schema, "additionalProperties")
        remove_key_recursive(schema, "title")

        return {
            "name": self.func.__name__,
            "description": self.func.__doc__,
            "parameters": schema,
        }

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        @wraps(self.func)
        def wrapper(*args, **kwargs):
            return self.validate_func(*args, **kwargs).dict()

        return wrapper(*args, **kwargs)

    def _validate_function_call(self, message, throw_error=True):
        if throw_error:
            assert "function_call" in message, "No function call detected"
            assert message["function_call"]["name"] == self.function_call_schema[
                "name"], "Function name does not match"

    def from_response(self, completion, throw_error=True):
        message = completion.choices[0].message
        self._validate_function_call(message, throw_error)
        arguments = json.loads(message["function_call"]["arguments"], strict=False)
        return self.validate_func(**arguments).dict()
