from agentive.utils.schema import BaseTool, Message
from agentive.utils.storage import LocalVectorStorage
from agentive.embeddings import Embeddings
from agentive.toolkit import BaseToolkit

from typing import List, Dict, Any


class LocalVectorToolkit(BaseToolkit):
    """
    This class is responsible for managing and interacting with local storage for various 'tools',
    where each tool is described by a name, a description, and some parameters.

    Attributes:
    -----------
    - storage: LocalVectorStorage
        An instance of LocalVectorStorage to handle the underlying storage operations.

    Methods:
    --------
    - __init__(embed_model: Embeddings) -> None:
        Initializes the local storage using an Embeddings model.
    - add_tool(tool: BaseTool) -> None:
        Adds a tool to the local storage.
    - add_tools(tools: List[BaseTool]) -> None:
        Adds multiple tools to the local storage.
    - get_tools(return_function=False) -> List[Dict[str, Any]]:
        Retrieves all tools as a list of dictionaries. Optionally returns function objects.
    - get_tool(name: str, return_function=False) -> Dict[str, Any]:
        Retrieves a specific tool by its name. Optionally returns function objects.
    - search_tools(query: str, n: int = 5, return_function=False) -> List[Dict[str, Any]]:
        Searches for tools based on a query, returning the top 'n' matches.
    - execute_from_message(message: BaseMessage) -> Any:
        Executes a tool using a BaseMessage object.
    - execute_from_response(completion: Dict) -> Any:
        Executes a tool using a completion object (deprecated).
    - execute(name: str, arguments: Dict[str, Any]) -> Any:
        Executes a tool by its name, using the supplied arguments.
    """

    def __init__(self, embed_model: Embeddings):
        """
        Initialize the local storage based on an Embeddings model.

        Parameters:
        -----------
        embed_model : Embeddings
            The embeddings model to initialize the LocalVectorStorage instance.
        """
        self.storage = LocalVectorStorage(embed_model)

    def add_tool(self, tool: BaseTool):
        """
        Adds a tool to the local storage.

        Parameters:
        -----------
        tool : BaseTool
            The tool to add. Must inherit from BaseTool.
        """

        tool_schema = tool.function_call_schema

        tool_dict = {
            'name': tool_schema['name'],
            'description': tool_schema['description'],
            'parameters': tool_schema['parameters'],
            'type': 'local_tool',
            'tool': tool
        }

        self.storage.add(content=f"{tool_dict['name']} {tool_dict['description']}", **tool_dict)

    def add_tools(self, tools: List[BaseTool]):
        """
        Adds multiple tools to the local storage.

        Parameters:
        -----------
        tools : List[BaseTool]
            The list of tools to add.
        """

        for tool in tools:
            self.add_tool(tool)

    def get_tools(self, return_function=False) -> List[Dict[str, Any]]:
        """
        Retrieves all tools as a list of dictionaries.

        Parameters:
        -----------
        return_function : bool, optional (default is False)
            If True, the method will also return the function objects.

        Returns:
        --------
        List[Dict[str, Any]]
            A list of tools, each represented as a dictionary.
        """
        if return_function:
            self.storage.get_all()

        return [tool['tool'].function_call_schema for tool in self.storage.get_all()]

    def get_tool(self, name: str, return_function=False) -> Dict[str, Any]:
        """
        Retrieves a specific tool by its name.

        Parameters:
        -----------
        name : str
            The name of the tool to retrieve.
        return_function : bool, optional (default is False)
            If True, the method will also return the function object.

        Returns:
        --------
        Dict[str, Any]
            The tool represented as a dictionary.
        """
        result = self.storage.search(filters={'name': name})

        if len(result) == 0:
            return {}

        if return_function:
            return result[0]

        return result[0]['tool']

    def search_tools(self, query: str, n=5, return_function=False) -> List[Dict[str, Any]]:
        """
        Searches for tools based on a query, returning the top 'n' matches.

        Parameters:
        -----------
        query : str
            The search query string.
        n : int, optional (default is 5)
            The number of top matches to return.
        return_function : bool, optional (default is False)
            If True, the method will also return the function objects associated with each tool.

        Returns:
        --------
        List[Dict[str, Any]]
            A list of matching tools, each represented as a dictionary.
        """
        tools = self.storage.search(query=query, n=n)

        if return_function:
            return tools

        return [tool['tool'].function_call_schema for tool in tools]

    def execute_from_message(self, message: Message) -> Any:
        """
        Executes a tool based on a given BaseMessage object.

        Parameters:
        -----------
        message : BaseMessage
            The message object that contains the name of the tool and other relevant data.

        Returns:
        --------
        Any
            The result of executing the tool, or None if the tool could not be found.
        """
        if not message.function_call:
            return None

        tool = self.get_tool(name=message.function_call.name, return_function=True)

        if tool is None:
            return None

        return tool['tool'].from_message(message=message)

    def execute_from_response(self, completion: Any) -> Any:
        """
        Executes a tool based on a given completion dictionary. Deprecated.

        Parameters:
        -----------
        completion : Dict
            The completion object that contains the name of the tool and other relevant data.

        Returns:
        --------
        Any
            The result of executing the tool, or None if the tool could not be found.

        Warning:
        --------
        This method is deprecated and will likely be removed in the future.
        """

        import warnings
        warnings.warn("This method is deprecated and will be removed in the future. Please use execute_from_message instead.", DeprecationWarning)

        message = completion.choices[0].message
        tool = self.get_tool(name=message.function_call.name, return_function=True)

        if tool is None:
            return None

        return tool['tool'].from_response(completion=completion)

    def execute(self, name: str, arguments: Dict[str, Any]) -> Any:
        """
        Executes a tool by its name, using the supplied arguments.

        Parameters:
        -----------
        name : str
            The name of the tool to execute.
        arguments : Dict[str, Any]
            The arguments to pass to the tool when executing it.

        Returns:
        --------
        Any
            The result of executing the tool, or None if the tool could not be found.
        """

        tool = self.get_tool(name, return_function=True)

        if tool is None:
            return None

        return tool['tool'].run(arguments)
