from typing import Optional, List
from bs4 import BeautifulSoup
from .search import *
import requests
import random
import time

class InvalidTagsError(Exception):
    pass

class HanimeVideo:
    def __init__(self, data):
        self.data = data

    def __getattr__(self, name):
        if name in self.data:
            return self.data[name]
        else:
            raise AttributeError(f"'HanimeVideo' object has no attribute '{name}'")
    
    @property
    def description(self):
        if 'description' in self.data:
            html_description = self.data['description']
            soup = BeautifulSoup(html_description, 'html.parser')
            return soup.get_text()
        else:
            return None


class VideoClient:
    BASE_URL = 'https://hanime.tv/api/v8'
    TAGS = [
        "3d", 
        "ahegao", 
        "anal", 
        "bdsm", 
        "big boobs",
        "blow job",
        "bondage",
        "boob job",
        "censored",
        "comedy",
        "cosplay",
        "creampie",
        "dark skin",
        "facial",
        "fantasy",
        "filmed",
        "foot job",
        "futanari",
        "gangbang",
        "glasses",
        "hand job",
        "harem",
        "hd",
        "horror",
        "incest",
        "inflation",
        "lactation",
        "loli",
        "maid",
        "masturbation",
        "milf",
        "mind break",
        "mind control",
        "monster",
        "nekomimi",
        "ntr",
        "nurse",
        "orgy",
        "plot",
        "pov",
        "pregnant",
        "public sex",
        "rape",
        "reverse rape",
        "rimjob",
        "scat",
        "school girl",
        "shota",
        "softcore",
        "swimsuit",
        "teacher",
        "tentacle",
        "threesome",
        "toys",
        "trap",
        "tsundere",
        "ugly bastard",
        "uncensored",
        "vanilla",
        "virgin",
        "watersports",
        "x-ray",
        "yaoi",
        "yuri"
    ]

    def __init__(self, cookies={'in_d4': '1', 'in_m4': '1',}, client_identifier=None):
        self.cookies = cookies or {}
        self.headers = self.create_default_headers(client_identifier)

    @staticmethod
    def create_default_headers(client_identifier: str = None) -> dict:
        headers = {
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
        }

        if client_identifier:
            headers['x-directive'] = 'api'
            headers['user-agent'] = f'HanimeWrapper ({client_identifier})'
            headers['x-time'] = str(time.time())

        return headers

    def get_video_info(self, video_id):
        url = f'{self.BASE_URL}/video?id={video_id}'
        try:
            response = requests.get(url, cookies=self.cookies, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return HanimeVideo(data['hentai_video'])
        except requests.RequestException as e:
            print(f"Error getting video info: {e}")
            return None
    
    def get_random_video(self):
        url = f'{self.BASE_URL}/hentai_videos'
        params = {
            'source': 'randomize',
            'r': str(int(time.time() * 1000)), 
        }

        try:
            response = requests.get(url, cookies=self.cookies, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            if 'hentai_videos' in data:
                return HanimeVideo(data['hentai_videos'][0])
            else:
                return None
        except requests.RequestException as e:
            print(f"Error getting random video: {e}")
            return None
    
    def get_random_video_tag(self, num_tags: int = 1, include_tags: Optional[List[str]] = None, exclude_tags: Optional[List[str]] = None, page: int = 0) -> List[ParsedData]:
        is_valid_tag = lambda tag: tag in self.TAGS
        invalid_include_tags = [tag for tag in (include_tags or []) if not is_valid_tag(tag)]
        invalid_exclude_tags = [tag for tag in (exclude_tags or []) if not is_valid_tag(tag)]

        if invalid_include_tags:
            raise InvalidTagsError(f"Invalid include tags: {invalid_include_tags}")
        if invalid_exclude_tags:
            raise InvalidTagsError(f"Invalid exclude tags: {invalid_exclude_tags}")

        filtered_tags = [tag for tag in self.TAGS if (include_tags is None or tag in include_tags) and (exclude_tags is None or tag not in exclude_tags)]

        if not filtered_tags:
            raise ValueError("No tags available after filtering.")

        num_selected_tags = min(num_tags, len(filtered_tags))
        selected_tags = random.sample(filtered_tags, num_selected_tags)
        payload = SearchPayload.create_default_payload()
        payload.tags = selected_tags
        payload.page = page
        search_result = SearchClient().search(payload)

        return SearchClient.parse_hits_data(search_result)


 
    
    



