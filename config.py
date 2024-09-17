import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    DISCORD_TOKEN: str = os.getenv('DISCORD_TOKEN', '').strip()
    MAX_QUEUE_SIZE: int = int(os.getenv('MAX_QUEUE_SIZE', '10'))
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO').strip()
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY').strip()
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY').strip()
    AI_HANDLER_TYPE: str = os.getenv('AI_HANDLER_TYPE', '').strip().lower()

    # Validate required configurations
    if not DISCORD_TOKEN:
        raise ValueError("DISCORD_TOKEN must be set in the .env file.")

    if AI_HANDLER_TYPE not in ['chatgpt', 'claude']:
        raise ValueError("AI_HANDLER_TYPE must be either 'chatgpt' or 'claude'.")

    if AI_HANDLER_TYPE == 'chatgpt' and not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY must be set for ChatGPT handler.")

    if AI_HANDLER_TYPE == 'claude' and not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY must be set for Claude handler.")

    SYSTEM_MESSAGE: str = os.getenv(
        'SYSTEM_MESSAGE',
        "You are a comedic version of Satan. Do not ask questions, only answer to them. Write only your dialogue. Do not write descriptions of actions."
    ).strip()
