import asyncio
from utils import generate_random_string, send_voice_reply
import logging
from api_handlers import get_api_handler
from config import AI_HANDLER_TYPE

class QueueHandler:
    def __init__(self, queue_size):
        self.queue = asyncio.Queue(queue_size)
        self.users_in_queue = set()
        self.lock = asyncio.Lock()
        self.handler = get_api_handler(AI_HANDLER_TYPE)

    async def handle_queue(self):
        while True:
            msg = await self.queue.get()
            try:
                #test
                # await asyncio.sleep(5)  # Simulate external API call
                #response = generate_random_string()
                #test
                response = await self.handler.chat_completion(msg.content)
                if not response:
                    response = "Couldn't process your message. Please try again later."

                #test
                await send_voice_reply(msg, response)
                #test
                await msg.reply(response, mention_author=True)
                logging.info(f'Message from {msg.author}: {msg.content}')
                logging.info(f'Reply to {msg.author}: {response}')
            except Exception as e:
                logging.error(f"Failed to process message: {e}")
                #test
                raise e
                #test
            finally:
                async with self.lock:
                    self.users_in_queue.discard(msg.author.id)
