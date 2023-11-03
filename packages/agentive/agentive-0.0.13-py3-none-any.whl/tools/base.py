from abc import ABC, abstractmethod


class BaseTools(ABC):
    """
    Base class for all tools. Defines a consistent interface that all tools must implement.
    """

    @abstractmethod
    def add_tool(self, name: str, description: str, parameters: dict):
        pass

    @abstractmethod
    def get_tools(self, **kwargs):
        pass

    @abstractmethod
    def get_tool(self, name: str, **kwargs):
        pass

    @abstractmethod
    def execute(self, name: str, arguments: dict, **kwargs):
        pass
