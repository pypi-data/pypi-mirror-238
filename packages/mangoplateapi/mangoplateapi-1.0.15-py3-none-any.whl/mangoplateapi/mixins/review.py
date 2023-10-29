from sphinx.util import requests

class ReviewMixin:
    def get_reviews(self, restaurant_code, start_index: int, page_size: int, proxy=None):
        url = f"http://stage.mangoplate.com/api/v5/restaurants/{restaurant_code}/reviews.json"
        data = {
            "language": "kor",
            "start_index": start_index,
            "request_count": page_size,
        }
        response = requests.get(url, data=data, proxies={"http":proxy})
        response.raise_for_status()
        response_dict = response.json()
        
        # ID 값 설정
        for item in response_dict:
            _id = item['action_id']
            item['_id'] = _id
            item['id'] = _id

        return response_dict
