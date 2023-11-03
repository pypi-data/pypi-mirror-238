import json

import requests

from . import query
from .utils import HEADERS


class MenuMixin:
    def get_popular_menus(self, business_id:str, cid: str = "231053", type: str = 'PICKUP'):
        data = query.get_popular_menus.create(business_id, cid, type)
        response = requests.post("https://pcmap-api.place.naver.com/graphql", headers=HEADERS, data=json.dumps(data))
        response.raise_for_status()
        response_data = response.json()
        graphql_data = response_data['data']['popularMenus']
        if graphql_data is None:
            return None
        graphql_data['business_id'] = business_id
        return graphql_data



