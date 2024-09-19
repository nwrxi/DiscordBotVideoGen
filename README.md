
# README

## Discord Bot Setup Guide

IMPORTANT: This repo is used for testing only and may or may not work and is in no way finished and probably will never be finished.

### Prerequisites

- Conda installed on your system.

----------

## Repository Setup

Clone the repository and initialize the submodules:

`git clone <repository-url>
cd <repository-directory>
git submodule update --init --recursive`

----------

## Environment Setup

It's required to create separate Conda environments for the Discord bot and SadTalker.

### 1. Discord Bot Environment

#### Create and Activate the Environment

`conda create -n DiscordBot python=3.11
conda activate DiscordBot`

#### Install Required Packages

Install the necessary Python packages:

`pip install discord.py TTS openai anthropic python-dotenv`

### 2. SadTalker Environment

Follow the [SadTalker installation instructions](https://github.com/Winfredy/SadTalker#installation) to install all required dependencies.

#### Configuration

Create .env file in root directory of the project. Following fields can be added:

`ANTHROPIC_API_KEY=
OPENAI_API_KEY=
DISCORD_TOKEN=
AI_HANDLER_TYPE=`

Where AI_HANDLER_TYPE can be either chatgpt or claude
