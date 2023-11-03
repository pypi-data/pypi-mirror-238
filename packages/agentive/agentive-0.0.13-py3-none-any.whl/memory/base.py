from abc import ABC, abstractmethod


class BaseMemory(ABC):
    """
    Base class for all memory types. Defines a consistent interface that all memory types must implement.
    """

    @abstractmethod
    def add_message(self, message, **kwargs):
        """
        Adds a message to memory
        :param message: message content
        :param kwargs: optional fields for messages being added to memory
        :return:
        """
        pass

    @abstractmethod
    def get_messages(self, n, **kwargs):
        pass
