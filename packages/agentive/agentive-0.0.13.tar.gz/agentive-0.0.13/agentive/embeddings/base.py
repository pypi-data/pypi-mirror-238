from abc import ABC, abstractmethod
from typing import List


class Embeddings(ABC):
    """Interface for embedding models."""

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """Embed text"""

    @abstractmethod
    def embed_bulk(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of text"""

    # TODO: add async methods