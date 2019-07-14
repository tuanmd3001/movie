# -*- coding: utf-8 -*-
import requests
from api.services.config import SERVICE_URLS, APP_ID, get_request_date, get_checksum, VERSION
import json


def call(post_data):
    language = post_data['language']
    post_data['app_id'] = APP_ID
    post_data['version'] = VERSION
    post_data['request_date'] = get_request_date()
    post_data['check_sum'] = get_checksum()
    post_data['channel_book'] = 'SCB|' + language
    r = requests.post(SERVICE_URLS['get_seats'], json=post_data)
    result = r.json()
    if "data" in result and result['data']:
        result["data"]['ticket_types'] = post_data['ticketTypes']
    return result
