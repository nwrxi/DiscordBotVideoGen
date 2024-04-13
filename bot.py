import discord
import asyncio
from discord.ext import commands
from queue_handler import QueueHandler
from config import TOKEN
import logging

class MyClient(discord.Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.handler = QueueHandler(2)

    async def on_ready(self):
        logging.info(f'Logged on as {self.user}!')
        self.loop.create_task(self.handler.handle_queue())

    async def on_message(self, message):
        if message.author == self.user:
            return  # Avoid the bot responding to its own messages

        if message.author.id in self.handler.users_in_queue:
            await message.reply('You already have a message in the queue!', mention_author=True)
            return  # Prevent adding multiple messages from the same user

        if self.handler.queue.full():
            await message.reply('Queue is full!', mention_author=True)
        else:
            await self.handler.queue.put(message)
            async with self.handler.lock:
                self.handler.users_in_queue.add(message.author.id)
            # Correct position reporting immediately after adding to queue
            position = self.handler.queue.qsize()  # This should reflect the new addition
            await message.reply(f'Your position in the queue: {position}', mention_author=True)


# Configure global logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Bot setup and running
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)
