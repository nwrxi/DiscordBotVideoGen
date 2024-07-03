from abc import ABC, abstractmethod
import os
import logging
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic

# Common system message
SYSTEM_MESSAGE = "You are a comedic version of Satan. Do not ask questions, only answer to them. Write only your dialogue. Do not write descriptions of actions."

class BaseApiHandler(ABC):
    @abstractmethod
    async def chat_completion(self, user_message):
        pass

class ChatGPTHandler(BaseApiHandler):
    def __init__(self, api_key=None, model='gpt-3.5-turbo'):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("An API key must be provided or set in the 'OPENAI_API_KEY' environment variable.")
        self.model = model
        self.client = AsyncOpenAI(api_key=self.api_key)
        self.system_message = {
            "role": "system",
            "content": SYSTEM_MESSAGE
        }

    async def chat_completion(self, user_message):
        messages = [self.system_message, {"role": "user", "content": user_message}]
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            if response.choices:
                return response.choices[0].message.content
            else:
                logging.warning('Received an empty response from the OpenAI API.')
                return None
        except Exception as e:
            logging.error(f'Unexpected error in OpenAI API call: {e}')
            return None

class ClaudeHandler(BaseApiHandler):
    def __init__(self, api_key=None, model='claude-3-5-sonnet-20240620'):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("An API key must be provided or set in the 'ANTHROPIC_API_KEY' environment variable.")
        self.model = model
        self.client = AsyncAnthropic(api_key=self.api_key)

    async def chat_completion(self, user_message):
        try:
            message = await self.client.messages.create(
                model=self.model,
                max_tokens=200,
                temperature=0,
                system=SYSTEM_MESSAGE,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": user_message
                            }
                        ]
                    }
                ]
            )
            if message.content:
                return message.content[0].text
            else:
                logging.warning('Received an empty response from the Anthropic API.')
                return None
        except Exception as e:
            logging.error(f'Unexpected error in Anthropic API call: {e}')
            return None

def get_api_handler(handler_type='claude'):
    if handler_type.lower() == 'chatgpt':
        return ChatGPTHandler()
    elif handler_type.lower() == 'claude':
        return ClaudeHandler()
    else:
        raise ValueError(f"Unsupported handler type: {handler_type}")