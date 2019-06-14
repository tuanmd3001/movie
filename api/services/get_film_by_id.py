# -*- coding: utf-8 -*-
import requests
from api.services.config import SERVICE_URLS, APP_ID, get_request_date, get_checksum
from datetime import datetime, timedelta


def call(cinema_id, film_id, from_date, to_date):
    params = {
        'app_id': APP_ID,
        'request_date': get_request_date(),
        'check_sum': get_checksum(),
        'cinema_id': cinema_id,
        'film_id': film_id,
        'from_date': from_date.strftime("%Y%m%d"),
        'to_date': to_date.strftime("%Y%m%d")
    }
    r = requests.get(SERVICE_URLS['get_film_by_id'], params=params)
    result = r.json()
    return result['data']

