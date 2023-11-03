from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """
    Base class for all LLMs. Defines the interface that all LLMs must implement.

    This is intended to be extensible as we add more foundational models.

    Notes:
    - Function calls are currently only available on certain models (e.g. GPT-3.5-turbo), but we may want to
    create a facsimile of this functionality for other models (e.g. GPT-3, Claude2, etc.) by using the outlines
    library: https://github.com/normal-computing/outlines
    """
    @abstractmethod
    def count_tokens(self, text):
        pass

    @abstractmethod
    def validate(self, text, max_tokens):
        pass

    @abstractmethod
    def chat(self, messages, max_tokens, **kwargs):
        pass

