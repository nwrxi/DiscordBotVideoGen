import asyncio
import logging
import io
import tempfile
import os
import discord

from api_handlers import get_api_handler
from config import Config

class QueueHandler:
    def __init__(self, max_queue_size: int, tts: 'TTS'):
        self.tts = tts
        self.queue: asyncio.Queue = asyncio.Queue(maxsize=max_queue_size)
        self.users_in_queue: set = set()
        self.lock = asyncio.Lock()
        self.handler = get_api_handler(Config.AI_HANDLER_TYPE)
        self.logger = logging.getLogger(self.__class__.__name__)

    async def handle_queue(self):
        """
        Continuously processes messages from the queue.
        """
        self.logger.info("Queue handler started.")
        while True:
            message: discord.Message = await self.queue.get()
            try:
                user_message = message.content
                #test
                # await asyncio.sleep(5)  # Simulate external API call
                #response = generate_random_string()
                #test
                self.logger.debug(f"Processing message from {message.author}: {user_message}")

                # Get AI response
                response = await self.handler.chat_completion(user_message)
                if not response:
                    response = "Couldn't process your message. Please try again later."
                else:
                    # Send voice reply if response was received
                    await self.send_voice_reply(message, response)

                # Send text reply
                await message.reply(response, mention_author=True)
                self.logger.info(f"Replied to {message.author}: {response}")
            except Exception as e:
                self.logger.error(f"Failed to process message {message.id}: {e}", exc_info=True)
                await message.reply("An error occurred while processing your message.", mention_author=True)
            finally:
                async with self.lock:
                    self.users_in_queue.discard(message.author.id)
                self.queue.task_done()

    async def send_voice_reply(self, msg: discord.Message, response: str):
        try:
            loop = asyncio.get_running_loop()

            # Create a temporary file to store the TTS output
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                temp_file_path = tmp_file.name

            # Run the TTS conversion in an executor to avoid blocking the event loop
            await loop.run_in_executor(
                None,
                lambda: self.tts.tts_to_file(
                    text=response,
                    speaker="p230",
                    file_path=temp_file_path
                )
            )

            # Open the generated audio file in binary read mode and send it as a Discord attachment
            with open(temp_file_path, 'rb') as audio_file:
                discord_file = discord.File(fp=audio_file, filename='response.wav')
                await msg.reply(file=discord_file)
                self.logger.debug("Voice reply sent.")

        except Exception as e:
            self.logger.error(f"Failed to send voice reply: {e}", exc_info=True)
            await msg.reply("Failed to generate voice reply.", mention_author=True)

        finally:
            # Clean up: remove the temporary file
            try:
                os.unlink(temp_file_path)
                self.logger.debug(f"Temporary file {temp_file_path} deleted.")
            except Exception as cleanup_error:
                self.logger.warning(f"Failed to delete temporary file {temp_file_path}: {cleanup_error}")
