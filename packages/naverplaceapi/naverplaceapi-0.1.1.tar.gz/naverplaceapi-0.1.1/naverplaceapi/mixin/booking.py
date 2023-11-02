import re
import json
import requests
from bs4 import BeautifulSoup
from . import query

from .utils import HEADERS, parse_naver_var_in_script_texts


class BookingMixin:
    def get_booking_items(self, business_id, business_type='restaurant', biz_type='STANDARD'):
        data = query.get_booking_items.create(business_id, business_type, biz_type)
        response = requests.post("https://pcmap-api.place.naver.com/graphql", headers=HEADERS, data=json.dumps(data))
        response.raise_for_status()
        response_data = response.json()
        graphql_data = response_data['data']
        graphql_data['business_id'] = business_id
        return graphql_data
