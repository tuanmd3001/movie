# -*- coding: utf-8 -*-
import requests
from api.services.config import SERVICE_URLS, APP_ID, get_request_date, get_checksum, VERSION


def call(pay_code):
    params = {
        'app_id': APP_ID,
        'version': VERSION,
        'request_date': get_request_date(),
        'check_sum': get_checksum(),
        'pay_code': pay_code,
    }
    r = requests.get(SERVICE_URLS['get_order_detail'], params=params)
    result = r.json()
    result['request_data'] = params
    return result

