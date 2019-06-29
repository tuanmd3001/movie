# -*- coding: utf-8 -*-
import requests
from api.services.config import SERVICE_URLS, APP_ID, get_request_date, get_checksum, VERSION


def call(query_id):
    params = {
        'app_id': APP_ID,
        'version': VERSION,
        'request_date': get_request_date(),
        'check_sum': get_checksum(),
        'query_id': query_id,
    }
    r = requests.get(SERVICE_URLS['get_book_ticket'], params=params)
    result = r.json()
    return result

