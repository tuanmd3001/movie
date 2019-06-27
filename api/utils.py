# -*- coding: utf-8 -*-
from api.services.config import APP_ID
from django.http import JsonResponse


def check_param(dic, key):
    if key in dic:
        return dic.get(key)
    else:
        return None


def response_error(code, message):
    r = {
        'app_id': APP_ID,
        'code': code,
        'message': message,
        'data': None
    }
    return JsonResponse(r)


def int_or_0(value):
    try:
        return int(value)
    except:
        return 0