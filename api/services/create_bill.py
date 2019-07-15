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
    param = {
        'data': json.dumps(post_data)
    }
    r = requests.post(SERVICE_URLS['create_bill'], data=param)
    result = r.json()
    if result['code'] == '99':
        result['message'] = 'Lỗi hệ thống, vui lòng thử lại sau.'
    elif result['code'] == '51':
        result['message'] = 'Rạp không hỗ trợ xuất hóa đơn.'
    elif result['code'] == '01':
        result['message'] = 'PayCode không hợp lệ hoặc không chính xác.'
    elif result['code'] == '03':
        result['message'] = 'Dữ liệu không đầy đủ hoặc không chính xác.'
    return result
