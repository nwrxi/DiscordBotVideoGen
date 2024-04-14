import asyncio
from utils import generate_random_string
import logging
from open_ai_handler import OpenAiApiHandler

class QueueHandler:
    def __init__(self, queue_size):
        self.queue = asyncio.Queue(queue_size)
        self.users_in_queue = set()
        self.lock = asyncio.Lock()
        self.handler = OpenAiApiHandler()

    async def handle_queue(self):
        while True:
            msg = await self.queue.get()
            try:
                # await asyncio.sleep(5)  # Simulate external API call
                # await msg.reply(generate_random_string(), mention_author=True)
                response = await self.handler.chat_completion(msg.content)
                if not response:
                    response = "Couldn't process your message. Please try again later."
                await msg.reply(response, mention_author=True)
                logging.info(f'Message from {msg.author}: {msg.content}')
                logging.info(f'Reply to {msg.author}: {response}')
            except Exception as e:
                logging.error(f"Failed to process message: {e}")
            finally:
                async with self.lock:
                    self.users_in_queue.discard(msg.author.id)
