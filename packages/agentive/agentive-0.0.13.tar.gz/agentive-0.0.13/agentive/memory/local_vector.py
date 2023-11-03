from agentive.utils.schema import Message
from agentive.utils.storage import LocalVectorStorage
from agentive.embeddings import Embeddings
from agentive.memory import BaseMemory

from datetime import datetime
from typing import List, Union, Any


class LocalVectorMemory(BaseMemory):
    """
    This class is responsible for managing and interacting with local storage for messages.

    Attributes:
    -----------
    - storage: LocalVectorStorage
        An instance of LocalVectorStorage to handle the underlying storage operations.

    Methods:
    --------
    - __init__(embed_model: Embeddings) -> None:
        Initializes the local storage using an Embeddings model.
    - add_message(message: Message) -> None:
        Adds a message to the local storage.
    - add_messages(messages: List[Message]) -> None:
        Adds multiple messages to the local storage.
    - get_message(_id: str, **kwargs) -> Message:
        Retrieves a specific message by its ID.
    - get_messages(**kwargs) -> List[Message]:
        Retrieves all messages in the local storage.
    - clear() -> None:
        Clears the local storage.
    - search_messages(query: str, n: int = 5) -> List[Message]:
        Searches for messages based on a query, returning the top 'n' matches.
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

    def add_message(self, message: Union[str, dict, Message]) -> None:
        """
        Adds a message to the local storage.

        Parameters:
        -----------
        message : Message
            The message to add. Must inherit from Message.
        """
        message = self._validate_message(message)
        message.timestamp = datetime.now()

        self.storage.add(**message.model_dump())

    def add_messages(self, messages: List[Union[str, dict, Message]]) -> None:
        """
        Adds multiple messages to the local storage.

        Parameters:
        -----------
        messages : List[Message]
            The messages to add. Must inherit from Message.
        """
        for message in messages:
            self.add_message(message)

    @staticmethod
    def _validate_message(message: Union[str, dict, Message]) -> Message:
        """
        Validates a message object.

        Parameters:
        -----------
        message : Message
            The message to validate.
        """
        if isinstance(message, str):
            message = Message(content=message)
        elif isinstance(message, dict):
            print(message)
            message = Message(**message)
        elif not isinstance(message, Message):
            raise ValueError("Message must be a string, dict, or Message object")

        return message

    def get_message(self, _id: str, **kwargs) -> Message:
        """
        Retrieves a specific message by its ID.

        Parameters:
        -----------
        _id : str
            The ID of the message to retrieve.
        **kwargs : Any
            Additional keyword arguments.

        Returns:
        --------
        Message
            The message object.
        """
        message = self.storage.get(_id, **kwargs)
        if message is None:
            raise ValueError(f"Message with ID {_id} not found.")
        return self._validate_message(message)

    def get_messages(self, **kwargs) -> List[Message]:
        """
        Retrieves all messages in the local storage.

        Parameters:
        -----------
        **kwargs : Any
            Additional keyword arguments.

        Returns:
        --------
        List[Message]
            The list of messages.
        """
        return [self._validate_message(message) for message in self.storage.get_all(**kwargs)]

    def clear(self) -> None:
        """
        Clears the local storage.
        """
        self.storage.clear()

    def search_messages(self, query: str, n: int = 5) -> List[Message]:
        """
        Searches for messages based on a query, returning the top 'n' matches.
        :param query:
        :param n:
        :return:
        """
        results = self.storage.search(query, n=n)
        return [self._validate_message(message) for message in results]

    def get_most_recent_messages(self, n: int = 5) -> List[Message]:
        """
        Retrieves the most recent messages.

        Parameters:
        -----------
        n : int, optional (default is 5)
            The number of messages to retrieve.
        """
        messages = self.storage.storage.sort_values(by='timestamp', ascending=False).head(n)
        return [self._validate_message(message) for message in messages]

    def update_message(self, _id: str, **kwargs: Any) -> None:
        """
        Update a message in the storage.

        Args:
            _id (str): The ID of the message to update.
            **kwargs (Any): Additional keyword arguments.
        """
        self.storage.update(_id, **kwargs)

    def delete_message(self, _id: str) -> None:
        """
        Delete a message from the storage.

        Args:
            _id (str): The ID of the message to delete.
        """
        self.storage.delete(_id)
