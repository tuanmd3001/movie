# -*- coding: utf-8 -*-
import requests
from api.services.config import SERVICE_URLS, APP_ID, get_request_date, get_checksum, VERSION


def call(app_mobile, app_id=APP_ID):
    params = {
        'app_id': app_id,
        'version': VERSION,
        'request_date': get_request_date(),
        'check_sum': get_checksum(),
        'app_mobile': app_mobile,
        'source_book': app_id
    }
    r = requests.get(SERVICE_URLS['get_my_films'], params=params)
    result = r.json()
    return result

