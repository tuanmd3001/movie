# -*- coding: utf-8 -*-
import requests
from api.services.config import SERVICE_URLS, APP_ID, get_request_date, get_checksum, VERSION


def call():
    params = {
        'app_id': APP_ID,
        'version': VERSION,
        'request_date': get_request_date(),
        'check_sum': get_checksum(),
    }
    r = requests.get(SERVICE_URLS['get_location'], params=params)
    result = r.json()
    return result

