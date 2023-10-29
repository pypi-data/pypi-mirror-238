from sphinx.util import requests
from bs4 import BeautifulSoup

from mangoplateapi.config import HEADERS
from mangoplateapi.utils import get_dict_field


class RestaurantMixin:
    def search_restaurants(self, keyword, start_index, page_size, proxy=None):
        url = f"http://stage.mangoplate.com/api/v5/search/by_keyword.json"
        data = {
            "language": "kor",
            "start_index": start_index,
            "request_count": page_size,
            "keyword": keyword,
            # "filter": {"subcuisine_codes":[],"metro_codes":[],"price_codes":[],"cuisine_codes":[],"is_parking_available":0},
            "order_by": "2"
        }
        response = requests.get(url, data=data, proxies={"http":proxy})
        response.raise_for_status()
        response_dict = response.json()
        items = response_dict['result']
        for item in items:
            _id = item['restaurant']['restaurant_uuid']
            item['_id'] = _id
            item['id'] = _id
            item['key'] = item['restaurant']['restaurant_key']
        return items

    def search_restaurants_count(self, keyword, proxy=None):
        url = f"http://stage.mangoplate.com/api/v5/search/by_keyword/count.json"
        data = {
            "language": "kor",
            "keyword": keyword,
        }
        response = requests.get(url, data=data, proxies={"http":proxy})
        response.raise_for_status()
        response_dict = response.json()
        return response_dict['count']

    def get_restaurant(self, code, proxy=None):
        url = f"http://stage.mangoplate.com/api/v5/restaurants/{code}.json"
        data = {
            "language": "kor",
        }
        response = requests.get(url, data=data, proxies={"http":proxy})
        response.raise_for_status()
        response_dict = response.json()
        
        # id값 설정
        _id = response_dict['restaurant_uuid']
        response_dict['_id'] = _id
        response_dict['id'] = _id

        key = response_dict['restaurant_key']
        #menus = self._parse_menu(code)
        menus = self._parse_menu(key)
        response_dict['menus'] = menus

        related_tags = self._parse_related_tags(key)
        response_dict['related_tags'] = related_tags

        return response_dict

    def _parse_related_tags(self, code, proxy=None):
        """
        망고 스토리 웹페이지에 대한 HTML 페이지를 요청
        """
        url = f"http://www.mangoplate.com/restaurants/{code}"
        response = requests.get(url, headers=HEADERS, proxies={"http":proxy})
        response.raise_for_status()
        # HTML 페이지를 BeautifulSoup으로 파싱.
        soup = BeautifulSoup(response.text, 'html.parser')

        """
        HTML 페이지에서 가게 메뉴 정보(이름, 가격, 이미지) 획득
        """
        related_tags = []
        related_tag_container_elem = soup.find("ul", class_="related-tags")
        if related_tag_container_elem is None:
            return related_tags
        tags = related_tag_container_elem.find_all("a")

        for tag in tags:
            related_tags.append(tag.text)
        return related_tags

    def _parse_menu(self, code, proxy=None):
        """
        망고 스토리 웹페이지에 대한 HTML 페이지를 요청
        """
        url = f"http://www.mangoplate.com/restaurants/{code}"
        response = requests.get(url, headers=HEADERS, proxies={"http":proxy})
        response.raise_for_status()
        # HTML 페이지를 BeautifulSoup으로 파싱.
        soup = BeautifulSoup(response.text, 'html.parser')

        """
        HTML 페이지에서 가게 메뉴 정보(이름, 가격, 이미지) 획득
        """
        menu_container_elem = soup.find("ul", class_="Restaurant_MenuList")
        if menu_container_elem is None:
            return {
                "menus": [],
                "image_urls": []
            }
        menu_item_elems = menu_container_elem.find_all("li", class_='Restaurant_MenuItem')
        menus = []
        for menu_item_elem in menu_item_elems:
            menu_data = {"name":"","price":0}
            name_elem = menu_item_elem.find("span", class_="Restaurant_Menu")
            if name_elem:
                menu_data['name'] = name_elem.text
            price_elem = menu_item_elem.find("span", class_="Restaurant_MenuPrice")
            if price_elem:
                menu_data['price'] = price_elem.text
            menus.append(menu_data)

        image_urls = []

        image_container_elem = soup.find("div", class_="list-thumb-photos")
        if image_container_elem is None:
            return {
                "menus": [],
                "image_urls": []
            }
        image_elems = image_container_elem.find_all("img")

        for image_elem in image_elems:
            image_url = get_dict_field(image_elem.attrs, ["src"], None)
            if image_url is None:
                image_url = get_dict_field(image_elem.attrs, ["data-original"], None)

            image_urls.append(image_url)

        return {
            "menus": menus,
            "image_urls": image_urls
        }
