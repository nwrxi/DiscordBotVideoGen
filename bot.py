import discord
import asyncio
from queue_handler import QueueHandler
from config import DISCORD_TOKEN
import logging

class MyClient(discord.Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.handler = QueueHandler(2)
        self.processing = set()  # Set to track messages being processed

    async def on_ready(self):
        logging.info(f'Logged on as {self.user}!')
        self.loop.create_task(self.handler.handle_queue())

    async def on_message(self, message):
        if message.author == self.user:
            return  # Avoid the bot responding to its own messages

        # Check if this message is already being processed
        if message.id in self.processing:
            return
        
        self.processing.add(message.id)
        try:
            async with self.handler.lock:
                if message.author.id in self.handler.users_in_queue:
                    await message.reply('You already have a message in the queue!', mention_author=True)
                elif self.handler.queue.full():
                    await message.reply('Queue is full!', mention_author=True)
                else:
                    await self.handler.queue.put(message)
                    self.handler.users_in_queue.add(message.author.id)
                    position = self.handler.queue.qsize()
                    await message.reply(f'Your position in the queue: {position}', mention_author=True)
        finally:
            self.processing.remove(message.id)

# Configure global logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Bot setup and running
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = MyClient(intents=intents)
client.run(DISCORD_TOKEN)