from openai import AsyncOpenAI
import logging
import os
import asyncio

class OpenAiApiHandler:
    def __init__(self, api_key=None, model='gpt-3.5-turbo'):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("An API key must be provided or set in the 'OPENAI_API_KEY' environment variable.")
        self.model = model
        self.__client = AsyncOpenAI(api_key=self.api_key)
        self.system_message = {
            "role": "system",
            "content": "You are a Satan from South Park. Do not ask questions, only answer to them."
        }

    async def chat_completion(self, user_message):
        messages = [self.system_message, {"role": "user", "content": user_message}]
        try:
            response = await self.__client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            if response.choices:
                return response.choices[0].message.content
            else:
                logging.warning('Received an empty response from the OpenAI API.')
                return None
        except asyncio.TimeoutError:
            logging.error('Timeout error when calling OpenAI API.')
            return None
        except Exception as e:
            logging.error(f'Unexpected error in OpenAI API call: {e}')
            return None
        return None
