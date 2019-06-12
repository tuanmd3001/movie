# -*- coding: utf-8 -*-
import requests
from api.services.config import SERVICE_URLS, APP_ID, get_request_date, get_checksum


def call(location_id):
    params = {
        'app_id': APP_ID,
        'request_date': get_request_date(),
        'check_sum': get_checksum(),
        'location_id': location_id
    }
    r = requests.get(SERVICE_URLS['get_cinema_by_location'], params=params)
    result = r.json()
    return result


