# -*- coding: utf-8 -*-
import requests
from api.services.config import SERVICE_URLS, APP_ID, get_request_date, get_checksum, VERSION
from datetime import datetime, timedelta


def call(film_id, from_date, to_date, cinema_id=None):
    params = {
        'app_id': APP_ID,
        'version': VERSION,
        'request_date': get_request_date(),
        'check_sum': get_checksum(),
        'film_id': film_id,
        'from_date': from_date.strftime("%Y%m%d"),
        'to_date': to_date.strftime("%Y%m%d")
    }
    if cinema_id:
        params['cinema_id'] = cinema_id
    r = requests.get(SERVICE_URLS['get_film_by_id'], params=params)
    result = r.json()
    return result