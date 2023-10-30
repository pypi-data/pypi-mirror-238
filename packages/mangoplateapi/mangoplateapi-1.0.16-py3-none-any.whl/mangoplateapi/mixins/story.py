import json

from sphinx.util import requests
from bs4 import BeautifulSoup

from mangoplateapi.config import HEADERS
from mangoplateapi.utils import get_dict_field


class StoryMixin:
    def get_stories(self, start_index: int, page_size: int, proxy=None):
        url = f"http://stage.mangoplate.com/api/v5/mango_picks/list.json"
        data = {
            "language": "kor",
            "start_index": start_index,
            "request_count": page_size
        }
        response = requests.get(url, data=data, proxies={"http":proxy})
        response.raise_for_status()
        response_dict = response.json()

        for item in response_dict:
            _id = item['post_id']
            item['_id'] = _id
            item['id'] = _id
        return response_dict

    def _parse_content(self, page_soup):
        contents = []
        list_elem = page_soup.find('div', class_='Story__ContentList')
        items = list_elem.find_all("div", class_="Story__Content")
        for item in items:
            pic_elem = item.find("img", class_="StoryContent__Picture")
            img_url = get_dict_field(pic_elem.attrs, ["src"], None)

            img_source_elem = item.find("span", class_="StoryContent__SourceText")
            image_source = img_source_elem.text or ""

            text_elem = item.find("p", class_="StoryContent__Caption")
            text = text_elem.text or ""
            contents.append({
                "image_url": img_url,
                "image_source": image_source,
                "text": text
            })
        return contents

    def _parse_related_stories(self, page_soup):
        story_ids = []
        list_elem = page_soup.find("ul", class_="Story__RelatedStoryList")
        items = list_elem.find_all("li", class_="Story__RelatedStoryItem")
        for item in items:
            story_id = get_dict_field(item.attrs, ["data-story-id"], None)
            story_ids.append(story_id)
        return story_ids

    def get_story(self, no: int, proxy=None):
        """

        :param no:
        :return:
        """
        """
        망고 스토리 웹페이지에 대한 HTML 페이지를 요청  
        """
        url = f"http://www.mangoplate.com/mango_picks/{no}"
        response = requests.get(url, headers=HEADERS, proxies={"http":proxy})
        response.raise_for_status()
        # HTML 페이지를 BeautifulSoup으로 파싱.
        soup = BeautifulSoup(response.text, 'html.parser')

        """
        HTML 페이지에 저장되어있는 Story 데이터 정보 획득
        """
        # id가 "storyData"인 script 태그를 찾습니다.
        script_tag = soup.find('script', id='storyData')
        # 데이터가 저장된 태그가 존재 하지 않는경우, 빈 Dict를 반환하고 종료
        if not script_tag:
            return {}
        # script 태그 내용을 추출합니다.
        """
        획득한 Story 데이터와 관련 가게정보 데이터에 id값을 설정
        NOTE: id/_id 값을 설정하여, 데이터베이스 저장시, 중복 저장을 방지 하기 위함
        """
        script_content = script_tag.text
        data = json.loads(script_content)
        id = data['id']
        data['_id'] = id
        restaurants = data['restaurants']
        for restaurant in restaurants:
            _id = restaurant['restaurant_uuid']
            restaurant['id'] = _id
            restaurant['_id'] = _id
        """
        HTML 스토리 페이지에서 컨텐츠 정보를 획득
        """
        contents = self._parse_content(soup)
        data['contents'] = contents

        # 스토리 게시물의 컨텐츠 정보 획득
        # list = soup.find(".Story__ContentList")

        # 관련 스토리 정보 획득
        """
        HTLM 스토리 페이지에서 연관된 스토리 ID 값을 획득
        """
        related_story_ids = self._parse_related_stories(soup)
        data['related_stories'] = related_story_ids

        return data
