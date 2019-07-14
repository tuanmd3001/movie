

import json
from urllib.parse import urlencode, quote

from django.contrib import messages
from django.http import HttpResponseRedirect
from datetime import datetime

from django.urls import reverse

from api.services.config import PASSWORD, URL_BACK_TO_APP
from movie.AESCipher import AESCipher


def index(request, *args, **kwargs):
    if request.method == "GET":
        params = request.GET
        password = PASSWORD
        aes_cipher = AESCipher(password)
        if 'data' in params:
            raw_data = aes_cipher.decrypt(params['data'])
            result = get_data_from_raw(raw_data)
            return custom_redirect('index', *(), **(result['data']))
        else:
            return HttpResponseRedirect(URL_BACK_TO_APP +
                                        "&reason=error&code=%s&message=%s" %
                                        ('00', 'Dữ liệu không hợp lệ hoặc bạn không có quyền truy cập dịch vụ này.'))
    else:
        return HttpResponseRedirect(URL_BACK_TO_APP +
                                    "&reason=error&code=%s&message=%s" %
                                    ('00', 'Dữ liệu không hợp lệ hoặc bạn không có quyền truy cập dịch vụ này.'))


def custom_redirect(url_name, *args, **kwargs):
    url = reverse(url_name, args=args)
    params = urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)


def get_data_from_raw(raw):
    list_data = raw.split('|')
    if len(list_data) == 5:
        bank_code = list_data[0]
        os_type = list_data[1]
        version = list_data[2]
        request_date = list_data[3]
        app_mobile = list_data[4]
        code = '00'
        timestamp = datetime.now().timestamp()
        raw_token = "%s|%s" % (raw, timestamp)
        password = PASSWORD
        aes_cipher = AESCipher(password)
        token = aes_cipher.encrypt(raw_token)
        return {
            'code': code,
            'data': {
                'bank_code': bank_code,
                'os_type': os_type,
                'version': version,
                'request_date': request_date,
                'app_mobile': app_mobile,
                'token': token
            }
        }
    else:
        return None


