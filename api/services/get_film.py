# -*- coding: utf-8 -*-
import requests
from api.services.config import SERVICE_URLS, APP_ID, get_request_date, get_checksum, VERSION


def call(cinema_id):
    params = {
        'app_id': APP_ID,
        'version': VERSION,
        'request_date': get_request_date(),
        'check_sum': get_checksum(),
        'cinema_id': cinema_id
    }
    r = requests.get(SERVICE_URLS['get_film'], params=params)
    result = r.json()
    return result['data']

