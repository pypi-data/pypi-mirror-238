import json

import requests

from . import query
from naverplaceapi.mixin.utils import HEADERS


class ReviewMixin:
    def get_visitor_reviews(self, business_id: str, page_no: int, page_cnt: int):
        data = query.get_visitor_reviews.create(business_id, page_no, page_cnt)
        response = requests.post("https://pcmap-api.place.naver.com/graphql", headers=HEADERS, data=json.dumps(data))
        response.raise_for_status()
        response_data = response.json()
        graphql_data = response_data['data']
        # ['visitorReviews']
        graphql_data['business_id'] = business_id
        return graphql_data

    def get_ugc_reviews(self, business_id: str, page_no: int, page_cnt: int):
        data = query.get_ugc_reviews.create(business_id, page_no, page_cnt)
        response = requests.post("https://pcmap-api.place.naver.com/graphql", headers=HEADERS, data=json.dumps(data))
        response.raise_for_status()
        graphql_data = response.json()
        graphql_data['business_id'] = business_id
        return graphql_data

    def get_visitor_review_stats(self, business_id: str):
        data = query.get_visitor_review_stats.create(business_id)
        response = requests.post("https://pcmap-api.place.naver.com/graphql", headers=HEADERS, data=json.dumps(data))
        response.raise_for_status()
        response_data = response.json()
        graphql_data = response_data['data']['visitorReviewStats']
        if graphql_data is None:
            return None
        graphql_data['_id'] = graphql_data['id']
        graphql_data['business_id'] = business_id
        return graphql_data

    def get_visitor_review_photos_in_visitor_review_tab(self, store_id: str, page_no: int, page_size: int):
        data = query.get_visitor_review_photos_in_visitor_review_tab.create(store_id, page_no, page_size)
        response = requests.post("https://pcmap-api.place.naver.com/graphql", headers=HEADERS, data=json.dumps(data))
        response.raise_for_status()
        response_data = response.json()
        graphql_data = response_data['data']
        graphql_data['business_id'] = store_id
        return graphql_data

    def get_visitor_review_theme_lists(self, store_id: str, page_no, page_size):
        data = query.get_visitor_review_theme_lists.create(store_id, page_no, page_size)
        response = requests.post("https://pcmap-api.place.naver.com/graphql", headers=HEADERS, data=json.dumps(data))
        response.raise_for_status()
        response_data = response.json()
        graphql_data = response_data['data']
        graphql_data['business_id'] = store_id

        return graphql_data


