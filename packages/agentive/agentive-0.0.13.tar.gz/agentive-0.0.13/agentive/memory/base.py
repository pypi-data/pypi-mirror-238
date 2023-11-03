from abc import ABC, abstractmethod
from typing import Union, Any, Dict, List
from agentive.utils.schema.message import Message


class BaseMemory(ABC):
    """
    Base class for all memory types. Defines a consistent interface that all memory types must implement.
    """

    def add_message(self, message: Union[str, Dict[str, Any], Message]) -> None:
        pass

    def add_messages(self, messages: List[Union[str, Dict[str, Any], Message]]) -> None:
        pass

    @abstractmethod
    def get_message(self, _id: str, **kwargs) -> Message:
        pass

    @abstractmethod
    def get_messages(self, **kwargs) -> List[Message]:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass
