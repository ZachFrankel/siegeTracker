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
intents.messages = True
client = discord.Client(intents=intents)
player_data = {}

DISCORD_USERS = [
    '516663612870492161'
]

TRACKED_USERS = [
    '4514f17d-c096-4e38-ae88-67693eb7b182', #bdos
    '69cb3be0-9d63-4be5-bfc6-0915e6285c68', #charlie
    'fccd4a88-bd5a-47d7-bb65-0c27d22bd045', #jole
    '3929bca3-9018-4a80-b1e1-851a953ba7be' #shane
]

INTERVAL = 300

async def handle_change(prev_data, current_data, change):
    kills = current_data['kills'] - prev_data['kills']
    deaths = current_data['deaths'] - prev_data['deaths']
    
    # match_result = "Win" if change > 0 else "Loss" if change < 0 else "Unknown"
    
    kd = round(kills/deaths, 1) if deaths > 0 else kills

    embed = discord.Embed(
        title=f"{current_data['username']}"
    )
    
    embed.set_thumbnail(url=current_data['pfp'])
    
    embed.add_field(
        name="Old MMR", 
        value=f"{prev_data['rank_points']}", 
        inline=False
    )

    embed.add_field(
        name="New MMR", 
        value=f"{current_data['rank_points']} ({change:+})", 
        inline=False
    )

    embed.add_field(
        name="Rank", 
        value=f"{current_data['rank']}", 
        inline=False
    )
    
    embed.add_field(
        name="KD", 
        value=f"{kills} - {deaths} ({kd})", 
        inline=False
    )

    embed.add_field(
        name="Overall KD",
        value=f"{round(current_data['kills']/current_data['deaths'], 1)}",
        inline=False
    )
    
    for discord_id in DISCORD_USERS:
        try:
            user = await client.fetch_user(int(discord_id))
            await user.send(embed=embed)
        except Exception as e:
            logger.error(f"Failed to send DM to Discord user {discord_id}: {str(e)}")

async def background_tracker():
    global player_data
    
    await client.wait_until_ready()
    
    while not client.is_closed():
        if TRACKED_USERS:
            player_data = await track_uids(TRACKED_USERS, player_data, handle_change)
        
        await asyncio.sleep(INTERVAL)

@client.event
async def on_ready():
    logger.info(f'Bot logged in as {client.user}')
    
    client.loop.create_task(background_tracker())

client.run(os.getenv('DISCORD_TOKEN'))