from dataclasses import dataclass, asdict
from bs4 import BeautifulSoup
import random
import requests
import json

@dataclass
class SearchPayload:
    search_text: str
    tags: list
    tags_mode: str
    brands: list
    blacklist: list
    order_by: str
    ordering: str
    page: int

    @classmethod
    def create_default_payload(cls):
        return cls(
            search_text='',
            tags=[],
            tags_mode='AND',
            brands=[],
            blacklist=[],
            order_by='created_at_unix',
            ordering='desc',
            page=0
        )

    @staticmethod
    def convert_ordering(ordering):
        ordering_map = {
            'recent_uploads': 'desc',
            'old_uploads': 'asc',
            'most_views': 'desc',
            'least_views': 'asc',
            'most_likes': 'desc',
            'least_likes': 'asc',
            'newest_uploads': 'desc',
            'oldest_uploads': 'asc',
            'alphabetical (a-z)': 'asc',
            'alphabetical (z-a)': 'desc',
        }
        return ordering_map.get(ordering, 'desc')  # Default to 'desc'

    @staticmethod
    def convert_order_by(order_by):
        order_by_map = {
            'most_views': 'views',
            'least_views': 'views',
            'most_likes': 'likes',
            'least_likes': 'likes',
            'newest_uploads': 'released_at_unix',
            'oldest_uploads': 'released_at_unix',
            'alphabetical (a-z)': 'title_sortable',
            'alphabetical (z-a)': 'title_sortable',
        }
        return order_by_map.get(order_by, 'created_at_unix')  # Default to 'created_at_unix'

@dataclass
class BaseSearchHeaders:
    authority: str
    accept: str
    accept_language: str
    content_type: str
    origin: str
    sec_ch_ua: str
    sec_ch_ua_mobile: str
    sec_ch_ua_platform: str
    sec_fetch_dest: str
    sec_fetch_mode: str
    sec_fetch_site: str
    user_agent: str

    @classmethod
    def create_default_headers(cls):
        return cls(
            authority='search.htv-services.com',
            accept='application.json, text.plain, /',
            accept_language='en-US,en;q=0.9',
            content_type='application/json;charset=UTF-8',
            origin='https://hanime.tv',
            sec_ch_ua='"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
            sec_ch_ua_mobile='?0',
            sec_ch_ua_platform='"Chrome OS"',
            sec_fetch_dest='empty',
            sec_fetch_mode='cors',
            sec_fetch_site='cross-site',
            user_agent='Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
        )
    
class ParsedData:
    def __init__(self, data):
        self.data = data

    def __getattr__(self, name):
        if name in self.data:
            return self.data[name]
        else:
            raise AttributeError(f"'ParsedData' object has no attribute '{name}'")
    
    @property
    def description(self):
        if 'description' in self.data:
            html_description = self.data['description']
            soup = BeautifulSoup(html_description, 'html.parser')
            return soup.get_text()
        else:
            return None

class SearchClient:
    BASE_URL = 'https://search.htv-services.com/'

    def __init__(self, client_identifier = None):
        self.session = requests.Session()
        self.session.headers = BaseSearchHeaders.create_default_headers()
        if client_identifier:
            self.session.headers.user_agent = f'HanimeWrapper ({client_identifier})'

    def search(self, payload):
        payload_dict = asdict(payload)
        response = self.session.post(self.BASE_URL, json=payload_dict)
        return response.json()

    @staticmethod
    def filter_response(base_response, filter_options):
        filtered_response = {}
        for key in filter_options:
            if key in base_response:
                filtered_response[key] = base_response[key]
        return filtered_response

    @staticmethod
    def parse_hits_data(response):
        try:
            hits = response['hits']
            hits_json = json.loads(hits)
            parsed_data = [ParsedData(hit) for hit in hits_json]
            return parsed_data
        except (KeyError, json.JSONDecodeError):
            return []


