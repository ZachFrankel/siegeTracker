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
    
    return {
        'user_id': user_id,
        'rank': ranked_profile.rank,
        'rank_points': ranked_profile.rank_points,
        'max_rank': ranked_profile.max_rank,
        'max_rank_points': ranked_profile.max_rank_points,
        'wins': ranked_profile.wins,
        'losses': ranked_profile.losses
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
                    
                    logger.info(f'User {user_id} rank points changed: {change:+} '
                               f'({prev_data['rank_points']} → {current_data['rank_points']})')
                    
                    if callback:
                        await callback(user_id, prev_data, current_data, change)
            
            updated_data[user_id] = current_data
            
        except Exception as e:
            logger.error(f'Error checking user {user_id}: {str(e)}')
    
    return updated_data