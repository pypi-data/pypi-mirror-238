from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Base class for all agent types. Defines a consistent interface that all agent types must implement.
    """

    @abstractmethod
    def generate_response(self, model=None):
        """
        Generates a response to the last message in memory
        :param model: optional model override to use for generating the response
        :return:
        """
        pass
