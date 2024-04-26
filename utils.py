from random_string_generator import RandomStringGenerator
import asyncio
import discord
from gtts import gTTS
import tempfile
import os

def generate_random_string():
    return RandomStringGenerator.generate_random_string()

async def send_voice_reply(msg, response):
    loop = asyncio.get_event_loop()  # Get the current event loop
    
    # Create a temporary file to save the TTS output
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
        tts = gTTS(response)
        await loop.run_in_executor(None, tts.save, fp.name)  # Save TTS in an executor
        fp.close()  # Close the file descriptor

    # Send the speech file as an attachment
    try:
        with open(fp.name, 'rb') as audio:
            await msg.reply(file=discord.File(audio, 'response.mp3'))
    finally:
        # Clean up: remove the temporary file
        os.unlink(fp.name)  # Ensure the file is deleted after sending