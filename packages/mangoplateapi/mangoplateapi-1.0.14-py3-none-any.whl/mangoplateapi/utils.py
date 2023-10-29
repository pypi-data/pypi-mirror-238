def get_dict_field(data, keys, default=None):
    """
    중첩된 dict 구조에서 안전하게 필드를 가져오고,
    필드가 존재하지 않는 경우 기본값을 반환합니다.

    :param data: 중첩된 dict 구조
    :param keys: 필드의 키를 나타내는 리스트
    :param default: 필드가 존재하지 않을 경우 반환할 기본값
    :return: 필드의 값 또는 기본값
    """
    try:
        for key in keys:
            data = data[key]
        return data
    except (KeyError, TypeError):
        return default