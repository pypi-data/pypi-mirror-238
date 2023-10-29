import base64

from sphinx.util import requests


def extract_code_id(data):
    return data['type_name'], data['display_text']
def encode_to_base64(input_string):
    try:
        # 문자열을 바이트로 인코딩합니다.
        input_bytes = input_string.encode('utf-8')

        # base64로 인코딩합니다.
        encoded_bytes = base64.b64encode(input_bytes)

        # 바이트를 문자열로 디코딩합니다.
        encoded_string = encoded_bytes.decode('utf-8')

        return encoded_string
    except Exception as e:
        return str(e)

class CodeMixin:
    def get_codes(self, proxy=None):
        url = f"http://stage.mangoplate.com/api/common/codetable.js"
        data = {
            "language": "kor",
            "order_by": "2"
        }
        response = requests.get(url, data=data, proxies={"http":proxy})
        response.raise_for_status()
        codes = response.json()

        # ID 설정
        for code in codes:
            keyword, code_status = extract_code_id(code)
            id = encode_to_base64(f'{keyword}_{code_status}')
            code['_id'] = id
            code['id'] = id
        return codes