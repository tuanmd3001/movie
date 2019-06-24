# -*- coding: utf-8 -*-
import requests
from api.services.config import SERVICE_URLS, APP_ID, get_request_date, get_checksum, VERSION
import json


def call(paycode):
    params = {
        'app_id': APP_ID,
        'version': VERSION,
        'paycode': paycode,
    }
    r = requests.post(SERVICE_URLS['get_seats'], data=params)
    result = r.json()
    return result['data']
