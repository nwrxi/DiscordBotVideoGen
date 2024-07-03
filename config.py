import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
AI_HANDLER_TYPE = os.getenv('AI_HANDLER_TYPE', 'claude')  # Default to Claude if not specified

# Validate required environment variables
if not DISCORD_TOKEN or DISCORD_TOKEN.strip() == "":
    raise ValueError("DISCORD_TOKEN must be set and non-empty in the .env file.")

if AI_HANDLER_TYPE.lower() == 'chatgpt':
    if not OPENAI_API_KEY or OPENAI_API_KEY.strip() == "":
        raise ValueError("OPENAI_API_KEY must be set and non-empty in the .env file when using ChatGPT.")

if AI_HANDLER_TYPE.lower() == 'claude':
    if not ANTHROPIC_API_KEY or ANTHROPIC_API_KEY.strip() == "":
        raise ValueError("ANTHROPIC_API_KEY must be set and non-empty in the .env file when using Claude.")

# Validate AI_HANDLER_TYPE
if AI_HANDLER_TYPE.lower() not in ['chatgpt', 'claude']:
    raise ValueError("AI_HANDLER_TYPE must be either 'chatgpt' or 'claude'.")