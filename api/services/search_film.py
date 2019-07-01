# -*- coding: utf-8 -*-
import requests
from api.services.config import SERVICE_URLS, APP_ID, get_request_date, get_checksum, VERSION


def call(keyword, status_id=0, page_no=1, page_size=20):
    params = {
        'app_id': APP_ID,
        'version': VERSION,
        'request_date': get_request_date(),
        'check_sum': get_checksum(),
        'keyword': keyword,
        'status_id': status_id,
        'pageNo': page_no,
        'pageSize': page_size,
    }
    r = requests.get(SERVICE_URLS['search_film'], params=params)
    result = r.json()
    return result

