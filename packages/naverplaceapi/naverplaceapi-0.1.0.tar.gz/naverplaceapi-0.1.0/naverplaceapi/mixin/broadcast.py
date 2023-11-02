import re
import json
import requests
from bs4 import BeautifulSoup

from .utils import HEADERS, parse_naver_var_in_script_texts


class BroadcastMixin:
    def get_broadcasts_of_store(self, business_id):
        # url = f"https://pcmap.place.naver.com/restaurant/{business_id}/home"
        url = "https://pcmap.place.naver.com/restaurant/{}".format(business_id)
        response = requests.get(url)
        response.raise_for_status()
        html_text = response.content

        broadcasts = self.__parse_broadcast_in_html(html_text)
        result = {
            "business_id": business_id,
            "broadcasts": broadcasts
        }
        return result

    def __parse_broadcast_in_html(self, html_text: str):
        soup = BeautifulSoup(html_text, "html.parser", from_encoding="utf-8")
        scripts = soup.find_all("script")

        naver_var = parse_naver_var_in_script_texts(scripts)

        # broadcast
        media_regex = re.compile(r'\{"__typename":"BroadcastInfo".*?\}')
        media_string_list = re.findall(media_regex, naver_var)

        broadcasts = []
        for media_string in media_string_list:
            media_json = json.loads(media_string)
            broadcast = {
                "channel": media_json["channel"],
                "program": media_json["program"],
                "episode": media_json["episode"],
                "date": media_json["date"],
                "menu": media_json["menu"],
                "tvcast": media_json["tvcast"]
            }
            broadcasts.append(broadcast)

        return broadcasts
