from sphinx.util import requests


class KeywordMixin:
    def search_keywords(self, keyword, start_index, page_size, proxy=None):
        url = f"http://stage.mangoplate.com/api/v3/web/search/by_keyword/suggested.js"
        data = {
            "language": "kor",
            "keyword": keyword,
            "start_index": start_index,
            "request_count": page_size,
            "order_by": "2"
        }
        response = requests.get(url, data=data, proxies={"http":proxy})
        response.raise_for_status()
        response_dict = response.json()
        return response_dict['result']

    def recommend_keywords(self, proxy=None):
        url = f"http://stage.mangoplate.com/api/v5/search/keyword/suggestion.json"
        data = {
            "language": "kor",
        }
        response = requests.get(url, data=data, proxies={"http":proxy})
        response.raise_for_status()
        response_dict = response.json()

        # ID 설정
        id = 1
        response_dict['id'] = id
        response_dict['_id'] = id
        return response_dict

