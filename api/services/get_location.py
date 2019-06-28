# -*- coding: utf-8 -*-
import requests
from api.services.config import SERVICE_URLS, APP_ID, get_request_date, get_checksum, VERSION
import math


def call(long=None, lat=None):
    params = {
        'app_id': APP_ID,
        'version': VERSION,
        'request_date': get_request_date(),
        'check_sum': get_checksum(),
    }
    r = requests.get(SERVICE_URLS['get_location'], params=params)
    result = r.json()
    try:
        if 'code' in result and result.get('code') == '00':
            if 'data' in result and len(result.get('data')) > 0:
                current_location = get_current_location(result.get('data'), float(long), float(lat))
                result['data'] = current_location
    except Exception:
        result['current_location'] = -1
    return result


def get_current_location(list_location, long, lat):
    min_distance = 0
    current_location = None
    for location in list_location:
        loc_long = location.get('longitude')
        loc_lat = location.get('latitude')
        distance = math.sqrt(math.pow(loc_long - long, 2) + math.pow(loc_lat - lat, 2))
        if distance < min_distance or min_distance == 0:
            min_distance = distance
            current_location = location
        if distance == 0:
            break
    return current_location
