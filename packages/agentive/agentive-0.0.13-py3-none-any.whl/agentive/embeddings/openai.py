from __future__ import annotations
from pydantic import BaseModel, Extra
from tenacity import retry
from typing import Any, List, Optional, Tuple, Union
from tqdm import tqdm

from agentive.embeddings.base import Embeddings
from agentive.utils.common import common_retry_settings

import numpy as np

import openai
import tiktoken


def perform_embedding(client: Any, model: str, input: Any, skip_empty: bool, request_timeout: Optional[Union[float, Tuple[float, float]]] = None) -> Any:
    if not input and skip_empty:
        return {'data': []}

    response = client.create(model=model, input=input, request_timeout=request_timeout)
    if any(len(d["embedding"]) == 1 for d in response["data"]) and not skip_empty:
        raise openai.error.APIError("OpenAI returned an empty embedding")
    return response


def sync_embed_with_retry(embeddings: Any, **kwargs: Any) -> Any:
    @retry(**common_retry_settings(kwargs['max_retries']))
    def _embed_with_retry() -> Any:
        return perform_embedding(kwargs['client'], kwargs['model'], embeddings, kwargs['skip_empty'])
    return _embed_with_retry()


class OpenAIEmbeddings(BaseModel, Embeddings):
    """
    OpenAIEmbeddings Class

    This class is responsible for generating embeddings for a list of texts
    using OpenAI's text embedding API.

    Attributes:
    ------------
    - embedding_ctx_length: int
        Maximum context length for the embeddings (default is 8191)

    - model: str
        Model name to use for generating embeddings (default is 'text-embedding-ada-002')

    - openai_api_key: Optional[str]
        API key for OpenAI. If None, the default key from the environment will be used.

    - chunk_size: int
        Number of tokens to process in a single batch (default is 512)

    - max_retries: int
        Maximum number of retries in case of failure (default is 6)

    - request_timeout: Optional[Union[float, Tuple[float, float]]]
        Timeout settings for the request to OpenAI's API

    - show_progress_bar: bool
        Whether to display a progress bar during processing (default is False)

    - skip_empty: bool
        Whether to skip embedding generation for empty texts (default is False)

    - client: Any
        Client for interacting with OpenAI's API (auto-generated during initialization)

    Methods:
    ---------
    __init__(self, **kwargs: Any)
        Class constructor. Initializes the OpenAI client and sets up other configurations.

    _prepare_tokens_and_indices(self, texts: List[str]) -> Tuple[List[Any], List[int]]
        Tokenizes the texts and prepares the corresponding indices.

    _compute_average_embedding(self, results, num_tokens_in_batch) -> List[List[float]]
        Computes the average embedding for each text in the list.

    _get_embeddings_core(self, tokens, indices, embed_func) -> List[List[float]]
        Core function to get the embeddings for each tokenized text.

    _get_len_safe_embeddings(self, texts) -> List[List[float]]
        Wrapper around _get_embeddings_core to handle texts with varying lengths.

    embed_bulk(self, texts: List[str], chunk_size: Optional[int] = 0) -> List[List[float]]
        Generates embeddings for a list of texts and returns them.

    embed(self, text: str) -> List[float]
        Generates an embedding for a single text string.

    Example:
    --------
    >>> embeddings = OpenAIEmbeddings(openai_api_key="your-api-key")
    >>> result = embeddings.embed("Hello, world!")
    """

    embedding_ctx_length: int = 8191
    model: str = 'text-embedding-ada-002'
    openai_api_key: Optional[str] = None
    chunk_size: int = 1000
    max_retries: int = 6
    request_timeout: Optional[Union[float, Tuple[float, float]]] = None
    show_progress_bar: bool = False
    skip_empty: bool = False
    client: Any = None
    verbose: bool = False

    class Config:
        extra = Extra.forbid

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        openai.api_key = self.openai_api_key
        self.client = openai.Embedding

    @staticmethod
    def _get_tokenizer():
        return tiktoken.get_encoding('p50k_base')

    def _prepare_tokens_and_indices(self, texts: List[str]) -> Tuple[List[Any], List[int]]:
        tokenizer = self._get_tokenizer()
        tokens, indices = [], []
        for i, text in enumerate(tqdm(texts, disable=not self.show_progress_bar)):
            token = tokenizer.encode(text)
            for j in range(0, len(token), self.embedding_ctx_length):
                tokens.append(tokenizer.decode(token[j:j + self.embedding_ctx_length]))
                indices.append(i)
        return tokens, indices

    @staticmethod
    def _compute_average_embedding(results, num_tokens_in_batch) -> List[List[float]]:
        embeddings = []
        for i, result in enumerate(results):
            average = np.average(result, axis=0, weights=num_tokens_in_batch[i]) if result else []
            embeddings.append((average / np.linalg.norm(average)).tolist())
        return embeddings

    def _get_embeddings_core(self, tokens, indices, embed_func) -> List[List[float]]:
        if not tokens:
            return []

        batched_embeddings, results, num_tokens_in_batch = (
            [],
            [[] for _ in range(max(indices) + 1)],
            [[] for _ in range(max(indices) + 1)]
        )

        for i in range(0, len(tokens), self.chunk_size):
            response = embed_func(tokens[i:i + self.chunk_size], **{
                'model': self.model,
                'client': self.client,
                'skip_empty': self.skip_empty,
                'max_retries': self.max_retries,
                'request_timeout': self.request_timeout,
                'verbose': self.verbose
            })
            batched_embeddings.extend(r["embedding"] for r in response["data"])

        for i, embedding in enumerate(batched_embeddings):
            idx = indices[i]
            if not (self.skip_empty and len(embedding) == 1):
                results[idx].append(embedding)
                num_tokens_in_batch[idx].append(len(tokens[i]))

        return self._compute_average_embedding(results, num_tokens_in_batch)

    def _get_len_safe_embeddings(self, texts) -> List[List[float]]:
        tokens, indices = self._prepare_tokens_and_indices(texts)
        return self._get_embeddings_core(tokens, indices, sync_embed_with_retry)

    def embed_bulk(self, texts: List[str], chunk_size: Optional[int] = 0) -> List[List[float]]:
        return self._get_len_safe_embeddings(texts)

    def embed(self, text: str) -> List[float]:
        return self.embed_bulk([text])[0] if text else []
