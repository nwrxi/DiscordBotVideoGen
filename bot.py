import discord
import logging


import torch
from TTS.api import TTS

from queue_handler import QueueHandler
from config import Config
from logger import setup_logging

class MyClient(discord.Client):
    def __init__(self, handler: QueueHandler, processing_limit: int = 100, **kwargs):
        intents = kwargs.pop('intents', discord.Intents.default())
        intents.messages = True
        intents.message_content = True
        super().__init__(intents=intents, **kwargs)

        self.handler = handler
        self.processing = set()
        self.processing_limit = processing_limit

        logging.info("Discord client initialized.")

    async def on_ready(self):
        """
        Event handler called when the bot is ready.
        """
        logging.info(f'Logged in as {self.user} (ID: {self.user.id})')
        self.loop.create_task(self.handler.handle_queue())

    async def on_message(self, message: discord.Message):
        """
        Event handler for incoming messages.

        Args:
            message (discord.Message): The message object.
        """
        if message.author == self.user:
            return  # Avoid responding to own messages

        if message.id in self.processing:
            logging.debug(f"Message {message.id} is already being processed.")
            return

        # Limit the number of tracked messages to prevent memory leaks
        if len(self.processing) >= self.processing_limit:
            logging.warning("Processing limit reached. Ignoring new messages.")
            return

        self.processing.add(message.id)
        try:
            await self._handle_message(message)
        except Exception as e:
            logging.error(f"Error handling message {message.id}: {e}", exc_info=True)
            await message.reply("An unexpected error occurred while processing your message.", mention_author=True)
        finally:
            self.processing.remove(message.id)

    async def _handle_message(self, message: discord.Message):
        """
        Handles the logic for processing incoming messages.

        Args:
            message (discord.Message): The message object.
        """
        async with self.handler.lock:
            if message.author.id in self.handler.users_in_queue:
                await message.reply('You already have a message in the queue!', mention_author=True)
                logging.info(f"User {message.author} attempted to queue multiple messages.")
                return
            elif self.handler.queue.full():
                await message.reply('Queue is full! Please try again later.', mention_author=True)
                logging.info("Queue is full. Message rejected.")
                return
            else:
                await self.handler.queue.put(message)
                self.handler.users_in_queue.add(message.author.id)
                position = self.handler.queue.qsize()
                await message.reply(f'Your position in the queue: {position}', mention_author=True)
                logging.info(f"Message {message.id} from {message.author} added to queue at position {position}.")

def main():
    """
    Main function to set up and run the Discord bot.
    """
    setup_logging()

    # Initialize TTS
    device = "cuda" if torch.cuda.is_available() else "cpu"
    try:
        tts = TTS(model_name='tts_models/en/vctk/vits', progress_bar=False).to(device)
        logging.info(f"TTS initialized on device: {device}")
    except Exception as e:
        logging.error(f"Failed to initialize TTS: {e}", exc_info=True)
        return

    # Initialize QueueHandler
    handler = QueueHandler(max_queue_size=Config.MAX_QUEUE_SIZE, tts=tts)
    logging.info("QueueHandler initialized.")

    # Initialize and run the client
    client = MyClient(handler=handler)
    try:
        client.run(Config.DISCORD_TOKEN)
    except Exception as e:
        logging.error(f"Failed to run Discord client: {e}", exc_info=True)

if __name__ == "__main__":
    main()
