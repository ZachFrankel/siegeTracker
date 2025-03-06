import os

from dotenv import load_dotenv
from siegeapi import Auth

load_dotenv()

async def track(user: str):
    auth = Auth(os.getenv('UBI_AUTH_EMAIL'), os.getenv('UBI_AUTH_PASSWORD'))
    player = await auth.get_player(uid=user)