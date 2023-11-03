from agentive.llm import BaseLLM

import openai
import tiktoken

from tenacity import retry, stop_after_attempt, wait_fixed


class OpenAISession(BaseLLM):
    def __init__(self, api_key, tokenizer=None):
        self.api_key = api_key
        self.default_model = 'gpt-3.5-turbo'
        self.available_models = {
            'gpt-3.5-turbo': {
                'max_tokens': 4096,
                'chat_model': True,
                'native_function_call': True,
            },
            'gpt-3-turbo-16k': {
                'max_tokens': 16384,
                'chat_model': True,
                'native_function_call': True,
            },
            'gpt-4': {
                'max_tokens': 8192,
                'chat_model': True,
                'native_function_call': True,
            },
            'gpt-4-32k': {
                'max_tokens': 32768,
                'chat_model': True,
                'native_function_call': True
            }
        }
        self.tokenizer = self.init_tokenizer() if tokenizer is None else tokenizer
        self.init_openai()

    def init_openai(self):
        openai.api_key = self.api_key

    @staticmethod
    def init_tokenizer():
        return tiktoken.get_encoding('p50k_base')

    def get_available_models(self):
        return self.available_models

    @staticmethod
    def validate_text(text):
        if not isinstance(text, str):
            raise ValueError('Text must be a string')
        if not text:
            raise ValueError('Text cannot be empty')

    def count_tokens(self, text, disallowed_special=()):
        self.validate_text(text)

        tokens = self.tokenizer.encode(text, disallowed_special=disallowed_special)

        return len(tokens)

    def validate_token_length(self, text, max_length):
        if self.count_tokens(text) > max_length:
            raise ValueError(f'Text exceeds max token length of {max_length}')

    def tokenize(self, text, disallowed_special=()):
        self.validate_text(text)
        return self.tokenizer.encode(text, disallowed_special=disallowed_special)

    def detokenize(self, tokens):
        return self.tokenizer.decode(tokens)

    def chat(self, messages, max_tokens=256, model=None, **kwargs):
        if not model:
            model = self.default_model

        if not self.available_models[model]['chat_model']:
            raise ValueError(f'{model} is not a chat model')

        if kwargs.get('function_call', False) and not self.available_models[model]['native_function_call']:
            raise ValueError(f'{model} does not support native function calls')

        text = '\n\n'.join([message['content'] for message in messages])

        self.validate_text(text)
        self.validate_token_length(text, self.available_models[model]['max_tokens'])

        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                **kwargs
            )
        except openai.error.InvalidRequestError as e:
            raise ValueError("Invalid request to OpenAI API: ", e)
        except Exception as e:
            raise ValueError("Error chatting with OpenAI API: ", e)

        return response

    @retry(stop=stop_after_attempt(5), wait=wait_fixed(1))
    def embed(self, text):
        self.validate_text(text)
        try:
            response = openai.Embedding.create(
                input=text,
                model="text-embedding-ada-002"
            )
        except openai.error.InvalidRequestError as e:
            raise ValueError("Invalid request to OpenAI API: ", e)
        except Exception as e:
            raise ValueError("Error generating embeddings with OpenAI API: ", e)

        return response['data'][0]['embedding']











