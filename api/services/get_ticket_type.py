# -*- coding: utf-8 -*-
import requests
from api.services.config import SERVICE_URLS, APP_ID, get_request_date, get_checksum
import json


def call(app_mobile, ss_id, request_id=0, language='VN'):
    params = {
        'app_id': APP_ID,
        'request_date': get_request_date(),
        'check_sum': get_checksum(),
        'app_mobile': app_mobile,
        'request_id': request_id,
        'ss_id': ss_id,
        'channel_book': 'SCB|' + language,

    }
    r = requests.post(SERVICE_URLS['get_ticket_type'], json=params)
    result = r.json()
    return result['data']
