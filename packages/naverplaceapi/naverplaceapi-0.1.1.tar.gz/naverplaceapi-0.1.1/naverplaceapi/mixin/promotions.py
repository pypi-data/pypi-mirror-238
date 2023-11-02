import json
import re
import requests
from . import query
from bs4 import BeautifulSoup

from .utils import HEADERS


class PromotionsMixin:

    def get_promotions(self, business_id: str, is_booking:bool = False):
        data = query.get_promotions.create(business_id, is_booking)
        response = requests.post("https://pcmap-api.place.naver.com/graphql", headers=HEADERS, data=json.dumps(data))
        response.raise_for_status()
        response_data = response.json()
        graphql_data = response_data['data']
        graphql_data['business_id'] = business_id
        graphql_data['_id'] = business_id
        return graphql_data
