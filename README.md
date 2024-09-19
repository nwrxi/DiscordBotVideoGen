
# README

## Discord Bot Setup Guide

This guide will help you set up the Discord bot and SadTalker environments using Conda.

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

It's recommended to create separate Conda environments for the Discord bot and SadTalker to manage dependencies efficiently.

### 1. Discord Bot Environment

#### Create and Activate the Environment

`conda create -n DiscordBot python=3.11
conda activate DiscordBot`

#### Install Required Packages

Install the necessary Python packages:

`pip install discord.py TTS openai anthropic python-dotenv`

### 2. SadTalker Environment

Follow the [SadTalker installation instructions](https://github.com/Winfredy/SadTalker#installation) to install all required dependencies.
