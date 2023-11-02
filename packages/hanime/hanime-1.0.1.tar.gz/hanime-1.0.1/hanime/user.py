from dataclasses import dataclass
from typing import List
import requests
import time

class HanimeUser:
    def __init__(self, data):
        self.data = data

    def __getattr__(self, name):
        if name in self.data:
            return self.data[name]
        else:
            raise AttributeError(f"'HanimeUser' object has no attribute '{name}'")

@dataclass
class UserClient:
    BASE_URL = 'https://hanime.tv/rapi/v7'

    def __init__(self, cookies={'in_d4': '1', 'in_m4': '1'}, headers={}):
        self.cookies = cookies
        self.headers = headers

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

    def get_channel_info(self, channel_id):
        url = f'{self.BASE_URL}/channels/{channel_id}'
        try:
            response = requests.get(url, cookies=self.cookies, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data 
        except requests.RequestException as e:
            print(f"Error getting channel info: {e}")
            return None
    

        
