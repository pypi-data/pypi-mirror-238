from dataclasses import dataclass
from typing import List
import requests
import time

@dataclass
class HanimeImage:
    id: int
    channel_name: str
    username: str
    url: str
    proxy_url: str
    extension: str
    width: int
    height: int
    filesize: int
    created_at_unix: int
    updated_at_unix: int
    discord_user_id: str
    user_avatar_url: str
    canonical_url: str
        
@dataclass
class ImageClient:
    BASE_URL = 'https://community-uploads.highwinds-cdn.com/api/v9/community_uploads'
    
    
    @staticmethod
    def create_default_headers() -> dict:
        return {
            'authority': 'hanime.tv',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Chrome OS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'x-directive': 'api',
            'x-session-token': '',
            'x-signature': None,
            'x-time': str(time.time()),
        }
    
    @staticmethod
    def build_query(channel_names: List[str], offset: int) -> dict:
        query = {
            'query_method': 'offset',
            '_offet': offset,
            'loc': 'https://hanime.tv',
        }
        for name in channel_names:
            query[f'channel_name__in[]'] = name
        return query

    @staticmethod
    def parse_community_uploads(data: dict) -> List[HanimeImage]:
        uploads = data.get('data', [])
        return [HanimeImage(
            id=upload['id'],
            channel_name=upload['channel_name'],
            username=upload['username'],
            url=upload['url'],
            proxy_url=upload['proxy_url'],
            extension=upload['extension'],
            width=upload['width'],
            height=upload['height'],
            filesize=upload['filesize'],
            created_at_unix=upload['created_at_unix'],
            updated_at_unix=upload['updated_at_unix'],
            discord_user_id=upload['discord_user_id'],
            user_avatar_url=upload['user_avatar_url'],
            canonical_url=upload['canonical_url'],
        ) for upload in uploads]
    
    @classmethod
    def get_community_uploads(cls, channel_names: List[str], offset: int):
        url = cls.BASE_URL
        headers = cls.create_default_headers()
        query = cls.build_query(channel_names, offset)
        
        try:
            response = requests.get(url, headers=headers, params=query)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error getting community uploads: {e}")
            return None
