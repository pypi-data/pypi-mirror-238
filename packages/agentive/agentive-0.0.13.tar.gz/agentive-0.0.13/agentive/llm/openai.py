from __future__ import annotations
from pydantic import BaseModel, Extra
from tenacity import retry
from typing import Any, List, Optional, Union, Dict

from agentive.llm.base import BaseLLM
from agentive.utils.common import common_retry_settings
from agentive.utils.schema import Message

import openai
import tiktoken


class OpenAISession(BaseModel, BaseLLM):
    """
    OpenAISession class is responsible for managing sessions with OpenAI's API.

    Attributes:
    -----------
    openai_api_key: Optional[str]
        The API key to use for authenticating requests to OpenAI.
    default_model: str
        Default model to use if no model is specified in the API call.
    available_models: Dict[str, Dict[str, Any]]
        Information on the available models and their limitations.
    client: Any
        Client object for interacting with the OpenAI API.
    max_retries: int
        Maximum number of retries for failed API requests.
    verbose: bool
        Verbosity setting for retry mechanism.

    Methods:
    --------
    __init__(**kwargs: Any):
        Initializes the OpenAISession object.
    _initialize_openai():
        Initialize OpenAI client.
    _get_tokenizer():
        Get a tokenizer object.
    _validate_text(text: str, max_length: int = None) -> None:
        Validates that the text is a non-empty string and does not exceed the max token length.
    _validate_messages(messages: Union[str, dict, Message, List[Union[str, dict, Message]]]) -> List[Message]:
        Validates and converts messages into a standardized format (List[Message]).
    count_tokens(text: str) -> int:
        Count the number of tokens in a given text.
    tokenize(text: str) -> List[int]:
        Tokenizes a given text and returns a list of integers.
    detokenize(tokens: List[int]) -> str:
        Converts a list of integer tokens back to a string.
    chat(messages: Union[str, Dict[str, Any], Message, List[Union[str, Dict[str, Any], Message]]], max_tokens: int = 256, model: str = None, **kwargs) -> Union[Message, Dict[str, Any]]:
        Sends messages to OpenAI API and receives a reply.
    """
    openai_api_key: Optional[str] = None
    default_model: str = 'gpt-3.5-turbo'
    available_models: Dict[str, Dict[str, Any]] = {
        'gpt-3.5-turbo': {
            'max_tokens': 4096,
        },
        'gpt-3.5-turbo-16k': {
            'max_tokens': 16384,
        },
        'gpt-4': {
            'max_tokens': 8192,
        },
        'gpt-4-32k': {
            'max_tokens': 32768,
        }
    }
    client: Any = None
    max_retries: int = 6
    verbose: bool = False

    class Config:
        extra = Extra.forbid

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self._initialize_openai()

    def _initialize_openai(self):
        openai.api_key = self.openai_api_key
        self.client = openai

    @staticmethod
    def _get_tokenizer():
        return tiktoken.get_encoding('p50k_base')

    @staticmethod
    def _validate_text(text: str, max_length: int = None) -> None:
        if not text or not isinstance(text, str):
            raise ValueError("Text must be a non-empty string")
        if max_length and len(text) > max_length:
            raise ValueError(f"Text exceeds max token length of {max_length}")

    @staticmethod
    def _validate_messages(messages: Union[str, dict, Message, List[Union[str, dict, Message]]]) -> List[Message]:
        # Ensure messages is a list
        if not isinstance(messages, list):
            messages = [messages]

        # Convert all messages to Message objects
        validated_messages = []
        for message in messages:
            if isinstance(message, str):
                validated_messages.append(Message(content=message))
            elif isinstance(message, dict):
                validated_messages.append(Message(**message))
            elif isinstance(message, Message):
                validated_messages.append(message)
            else:
                raise ValueError("Messages must be a string, dict, or Message object")

        return validated_messages

    def count_tokens(self, text: str) -> int:
        self._validate_text(text)
        return len(self._get_tokenizer().encode(text))

    def tokenize(self, text: str) -> List[int]:
        self._validate_text(text)
        return self._get_tokenizer().encode(text)

    def detokenize(self, tokens: Union[List[int], List[str]]) -> str:
        return self._get_tokenizer().decode(tokens)

    @retry(**common_retry_settings(max_retries=max_retries, verbose=verbose))
    def chat(self,
             messages: Union[str, Dict[str, Any], Message, List[Union[str, Dict[str, Any], Message]]],
             max_tokens: int = 256,
             model: str = None,
             **kwargs) -> Union[Message, Dict[str, Any]]:

        model = model or self.default_model
        messages = self._validate_messages(messages)

        self._validate_text(
            '\n\n'.join([message.content for message in messages]),
            max_length=self.available_models[model]['max_tokens']
        )

        try:
            completion = self.client.ChatCompletion.create(
                model=model,
                messages=[message.to_message() for message in messages],
                max_tokens=max_tokens,
                **kwargs
            )
        except openai.error.InvalidRequestError as e:
            raise ValueError(f"Invalid request to OpenAI API: {e}")
        except Exception as e:
            raise ValueError(f"Error chatting with OpenAI API: {e}")

        if kwargs.get('return_response'):
            return completion

        return Message(**completion['choices'][0]['message'])
