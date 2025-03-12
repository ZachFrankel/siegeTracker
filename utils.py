import os
import logging

from dotenv import load_dotenv
from siegeapi import Auth

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('TRACKER')

async def get_ranked_data(user_id: str):
    auth = Auth(os.getenv('UBI_AUTH_EMAIL'), os.getenv('UBI_AUTH_PASSWORD'))
    player = await auth.get_player(uid=user_id)

    await player.load_ranked_v2()
    ranked_profile = player.ranked_profile

    await auth.close()
    
    return {
        'username': player.name,
        'pfp': player.profile_pic_url_256,
        'rank': ranked_profile.rank,
        'rank_points': ranked_profile.rank_points,
        'kills': ranked_profile.kills,
        'deaths': ranked_profile.deaths
    }

async def track_uids(tracked_users, player_data, callback=None):
    updated_data = player_data.copy()
    
    for user_id in tracked_users:
        try:
            current_data = await get_ranked_data(user_id)
            
            if user_id in player_data:
                prev_data = player_data[user_id]
                
                if current_data['rank_points'] != prev_data['rank_points']:
                    change = current_data['rank_points'] - prev_data['rank_points']
                    
                    if callback:
                        await callback(user_id, prev_data, current_data, change)
            
            updated_data[user_id] = current_data
            
        except Exception as e:
            logger.error(f'Error checking user {user_id}: {str(e)}')
    
    return updated_data