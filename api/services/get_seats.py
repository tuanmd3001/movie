# -*- coding: utf-8 -*-
import requests
from api.services.config import SERVICE_URLS, APP_ID, get_request_date, get_checksum, VERSION


def call(app_mobile, ss_id, book_service_id, request_id=0, language='VN'):
    params = {
        'app_id': APP_ID,
        'version': VERSION,
        'request_date': get_request_date(),
        'check_sum': get_checksum(),
        'app_mobile': app_mobile,
        'request_id': request_id,
        'book_service_id': book_service_id,
        'queryId': 1,
        'ss_id': ss_id,
        'channel_book': 'SCB|' + language,

    }
    r = requests.post(SERVICE_URLS['get_seats'], json=params)
    result = r.json()
    return result['data']
