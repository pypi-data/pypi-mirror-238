import json
import re
import requests
from . import query
from bs4 import BeautifulSoup

from .utils import HEADERS, parse_naver_var_in_script_texts


class PlaceMixin:

    def search_places(self, keyword: str, page_no: int, page_size: int):
        data = query.get_restaurants.create(keyword, page_no, page_size)
        response = requests.post("https://pcmap-api.place.naver.com/graphql", headers=HEADERS, data=json.dumps(data))
        response.raise_for_status()
        results = response.json()

        for result in results:
            id = result['id']
            result['_id'] = id
        return result

    def get_place(self, business_id):
        # url = f"https://pcmap.place.naver.com/restaurant/{business_id}/home"
        url = "https://pcmap.place.naver.com/restaurant/{}".format(business_id)
        response = requests.get(url)
        response.raise_for_status()
        html_text = response.content

        broadcasts = self.__parse_broadcast_in_html(html_text)
        return broadcasts

    def __parse_broadcast_in_html(self, html_text: str):
        soup = BeautifulSoup(html_text, "html.parser", from_encoding="utf-8")
        scripts = soup.find_all("script")

        naver_var = parse_naver_var_in_script_texts(scripts)
        variable_name = 'window.__APOLLO_STATE__'
        pattern = re.compile(rf'\b{re.escape(variable_name)}\s*=\s*(.*?)(\n)')
        match = pattern.search(naver_var)

        if match:
            data = match.group(1)
            return json.loads(data[:-1])
        else:
            return None


    def get_place_summary(self, id: str, proxy=None):
        url = f"https://map.naver.com/v5/api/sites/summary/" + id + "?lang=ko"
        data = {
            "language": 'kor',
            "order_by": "2"
        }
        response = requests.get(url, data=data, proxies={"http": proxy})
        response.raise_for_status()
        resposne_data = response.json()
        resposne_data['_id'] = id
        return resposne_data

    def get_menus(self, business_id):
        url = f"https://pcmap.place.naver.com/restaurant/{business_id}/menu/list"
        response = requests.get(url)
        response.raise_for_status()
        html_text = response.content
        menus = self.__parse_menus_internal(html_text)
        result = {
            "business_id": business_id,
            "menus": menus
        }
        return result

    def __parse_menus_internal(self, html_text: str):
        soup = BeautifulSoup(html_text, "html.parser", from_encoding="utf-8")
        scripts = soup.find_all("script")
        naver_string = None

        for s in scripts:
            if s.string is None:
                continue
            if "var naver=" in s.string:
                naver_string = s.string

        menu_regex = re.compile(r'\{"__typename":"Menu".*?\}')
        menu_string_list = re.findall(menu_regex, naver_string)

        # 일반
        menus = []
        for menu_string in menu_string_list:
            menu_json = json.loads(menu_string)
            menu = {
                "name": menu_json["name"],
                "price": menu_json["price"],
                "description": menu_json["description"],
                "imageUrl": menu_json["images"][0] if menu_json["images"] else "",
                "isRecommended": menu_json["recommend"],
            }
            menus.append(menu)
        # baemin
        baemin_menu_regex = re.compile(r'\{"__typename":"BaeminMenu".*?\}')
        baemin_menu_string_list = re.findall(baemin_menu_regex, naver_string)

        for baemin_menu_string in baemin_menu_string_list:
            baemin_menu_json = json.loads(baemin_menu_string)
            menu = {
                "name":baemin_menu_json["name"],
                "price":baemin_menu_json["price"],
                "imageUrl":menu_json["images"][0] if menu_json["images"] else "",

            }
            menus.append(menu)
        return menus
