from abc import ABC, abstractmethod
from typing import Any, Dict
from agentive.utils.schema import BaseTool, Message


class BaseToolkit(ABC):
    """
    Base class for all tools. Defines a consistent interface that all tools must implement.
    """

    def add_tool(self, tool: BaseTool):
        pass

    def add_tools(self, tools: list[BaseTool]):
        for tool in tools:
            self.add_tool(tool)

    @abstractmethod
    def get_tools(self, **kwargs):
        pass

    @abstractmethod
    def get_tool(self, name: str, **kwargs):
        pass

    @abstractmethod
    def execute_from_message(self, message: Message) -> Any:
        pass

    @abstractmethod
    def execute(self, name: str, arguments: Dict[str, Any]) -> Any:
        pass
