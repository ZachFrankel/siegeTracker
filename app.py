import discord
import asyncio
import os
import logging

from dotenv import load_dotenv
from datetime import datetime
from utils import track_uids

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('TRACKER')

load_dotenv()

intents = discord.Intents.default()
client = discord.Client(intents=intents)
player_data = {}

TRACKED_USERS = [
    '5282a1e6-cae1-414d-82f8-ace0a8e24841',

]
INTERVAL = 300

async def handle_change(user_id, prev_data, current_data, change):
    logger.info("handleChange func called")

async def background_tracker():
    global player_data
    
    await client.wait_until_ready()
    
    while not client.is_closed():
        if TRACKED_USERS:
            logger.info(f'Checking rank changes for {len(TRACKED_USERS)} users')
            player_data = await track_uids(TRACKED_USERS, player_data, handle_change)
        
        await asyncio.sleep(INTERVAL)

@client.event
async def on_ready():
    logger.info(f'Bot logged in as {client.user}')
    
    client.loop.create_task(background_tracker())

client.run(os.getenv('DISCORD_TOKEN'))