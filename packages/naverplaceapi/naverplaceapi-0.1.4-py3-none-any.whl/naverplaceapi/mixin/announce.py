import json
import re
import requests
from . import query
from bs4 import BeautifulSoup

from .utils import HEADERS


class AnnouncementMixin:

    def get_announcement(self, business_id:str, business_type:str='restaurant', device_type:str='pcmap'):
        data = query.get_announcements.create(business_id, business_type, device_type)

        response = requests.post("https://pcmap-api.place.naver.com/graphql", headers=HEADERS, data=json.dumps(data))
        response.raise_for_status()
        response_data = response.json()
        graphql_data = response_data['data']
        graphql_data['business_id'] = business_id

        return graphql_data
