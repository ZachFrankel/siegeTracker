import discord
import asyncio
import os

from dotenv import load_dotenv

load_dotenv()

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    pass

client.run(os.getenv('DISCORD_TOKEN'))