from abc import ABC, abstractmethod
import logging
from typing import Optional

from openai import AsyncOpenAI
from anthropic import AsyncAnthropic

from config import Config

SYSTEM_MESSAGE = "You are Stan and you are insuferrable Tech Bro. Be very bro and techy in you replies. Do not ask questions, only answer to them. Write only your dialogue. Do not write descriptions of actions. Write only one sentence max."

# Get the module-specific logger
logger = logging.getLogger(__name__)

class BaseApiHandler(ABC):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    async def chat_completion(self, user_message: str) -> Optional[str]:
        pass


class ChatGPTHandler(BaseApiHandler):
    def __init__(self, model: str = 'gpt-3.5-turbo'):
        super().__init__()
        self.api_key = Config.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY must be set for ChatGPT handler.")
        self.model = model
        self.client = AsyncOpenAI(api_key=self.api_key)
        self.system_message = {
            "role": "system",
            "content": SYSTEM_MESSAGE
        }
        self.logger.debug(f"Initialized ChatGPTHandler with model: {self.model}")

    async def chat_completion(self, user_message: str) -> Optional[str]:
        messages = [self.system_message, {"role": "user", "content": user_message}]
        try:
            self.logger.debug(f"Sending request to OpenAI with messages: {messages}")
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            if response.choices:
                reply = response.choices[0].message.content.strip()
                self.logger.debug(f"Received response from OpenAI: {reply}")
                return reply
            else:
                self.logger.warning('Received an empty response from the OpenAI API.')
                return None
        except Exception as e:
            self.logger.error(f"Unexpected error in OpenAI API call: {e}", exc_info=True)
            return None


class ClaudeHandler(BaseApiHandler):
    def __init__(self, model: str = 'claude-3-5-sonnet-20240620'):
        super().__init__()
        self.api_key = Config.ANTHROPIC_API_KEY
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY must be set for Claude handler.")
        self.model = model
        self.client = AsyncAnthropic(api_key=self.api_key)
        self.logger.debug(f"Initialized ClaudeHandler with model: {self.model}")

    async def chat_completion(self, user_message: str) -> Optional[str]:
        try:
            messages = [{"role": "user", "content": [{"type": "text", "text": user_message}]}]
            self.logger.debug(f"Sending request to Anthropic with messages: {messages}")
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=200,
                temperature=0,
                system=SYSTEM_MESSAGE,
                messages=messages
            )
            if response.completion:
                reply = response.completion.strip()
                self.logger.debug(f"Received response from Anthropic: {reply}")
                return reply
            else:
                self.logger.warning('Received an empty response from the Anthropic API.')
                return None
        except Exception as e:
            self.logger.error(f"Unexpected error in Anthropic API call: {e}", exc_info=True)
            return None


def get_api_handler(handler_type: str) -> BaseApiHandler:
    handler_type = handler_type.lower()
    logger.debug(f"Requested handler type: {handler_type}")

    if handler_type == 'chatgpt':
        return ChatGPTHandler()
    elif handler_type == 'claude':
        return ClaudeHandler()
    else:
        error_msg = f"Unsupported handler type: {handler_type}"
        logger.error(error_msg)
        raise ValueError(error_msg)
