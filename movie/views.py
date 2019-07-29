import re
from urllib.parse import urlencode

from django.http import HttpResponseRedirect
from datetime import datetime

from django.urls import reverse

from api.services.config import PASSWORD, URL_BACK_TO_APP, INTERNAL_ERROR, SUCCESS, INVALID_DATA
from movie.AESCipher import AESCipher


def validate_data(request, number_param):
    if request.method == "GET":
        params = request.GET
        password = PASSWORD
        aes_cipher = AESCipher(password)
        if 'lang' in params:
            language = params['lang']
            if language == 'VI':
                language = 'VN'
            elif language == 'EN':
                language = 'ENG'
            else:
                language = 'VN'
        else:
            language = 'VN'
        if 'data' in params:
            try:
                raw_data = aes_cipher.decrypt(params['data'])
                result = get_data_from_raw(raw_data, language, number_param)
                if result and result['code'] == '00':
                    result_bank_code = validate_bank_code(result['data']['bank_code'])
                    if result_bank_code != SUCCESS:
                        result['code'] = result_bank_code
                    else:
                        # result_request_date = validate_request_date(result['data']['request_date'])
                        # if result_request_date != SUCCESS:
                        #     result['code'] = result_request_date
                        # else:
                        result_app_mobile = validate_app_mobile(result['data']['app_mobile'])
                        if result_app_mobile != SUCCESS:
                            result['code'] = result_app_mobile
            except ValueError as e:
                result = {
                    'code': INVALID_DATA,
                    'data': {},
                    'raw': ''
                }

        else:
            result = {
                'code': INVALID_DATA,
                'data': {},
                'raw': ''
            }
        result['lang'] = params['lang'] if 'lang' in params else 'VI'
    else:
        result = {
            'code': INVALID_DATA,
            'data': {},
            'raw': '',
            'lang': 'VI'
        }
    return result


def validate_bank_code(bank_code):
    if bank_code != 'SACOMBANK':
        return INVALID_DATA
    return SUCCESS


def validate_request_date(request_date):
    try:
        request_time = datetime.strptime(request_date, '%Y%m%d%H%M%S')
        if datetime.now().timestamp() - 600 <= request_time.timestamp() <= datetime.now().timestamp() + 600:
            return SUCCESS
        else:
            return INVALID_DATA
    except Exception as e:
        return INVALID_DATA


def validate_app_mobile(app_mobile):
    rule = re.compile(r'([0]{1})([1-9]{1})([0-9]{8})')
    if not rule.search(app_mobile):
        return INVALID_DATA
    return SUCCESS


def index(request, *args, **kwargs):
    result = validate_data(request, 6)
    if result['code'] == SUCCESS:
        return custom_redirect('index', *(), **result['data'])
    else:
        return redirect_error(result)


def order_preview(request, *args, **kwargs):
    result = validate_data(request, 7)
    if result['code'] == SUCCESS:
        return custom_redirect('bill', *(), **result['data'], payCode=result['data']['paycode'])
    else:
        return redirect_error(result)


def create_bill(request, *args, **kwargs):
    result = validate_data(request, 7)
    if result['code'] == SUCCESS:
        return custom_redirect('bill', *(), **result['data'], payCode=result['data']['paycode'])
    else:
        return redirect_error(result)


def custom_redirect(url_name, *args, **kwargs):
    url = reverse(url_name, args=args)
    params = urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)


def redirect_error(result):
    raw_data = result['raw']
    if len(raw_data) > 0:
        raw_data = "%s|%s" % (raw_data, result['code'])
        password = PASSWORD
        aes_cipher = AESCipher(password)
        try:
            return_data = aes_cipher.encrypt(raw_data)
        except ValueError as e:
            return_data = ""
        return HttpResponseRedirect(URL_BACK_TO_APP + "&data=%s&lang=%s" % (return_data, result['lang']))
    else:
        return HttpResponseRedirect(URL_BACK_TO_APP + "&lang=%s" % result['lang'])


def get_data_from_raw(raw, language, number_param):
    list_data = raw.split('|')
    if len(list_data) == number_param:
        bank_code = list_data[0]
        os_type = list_data[1]
        version = list_data[2]
        request_date = list_data[3]
        user_name = list_data[4]
        app_mobile = list_data[5]
        if len(list_data) > 6:
            paycode = list_data[6]
        else:
            paycode = None
        timestamp = datetime.now().timestamp()
        raw_token = "%s|%s" % (raw, timestamp)
        password = PASSWORD
        aes_cipher = AESCipher(password)
        try:
            token = aes_cipher.encrypt(raw_token)
            code = SUCCESS
            data = {
                'bank_code': bank_code,
                'os_type': os_type,
                'version': version,
                'request_date': request_date,
                'user_name': user_name,
                'app_mobile': app_mobile,
                'token': token,
                'language': language
            }
            if paycode:
                data['paycode'] = paycode
        except ValueError as e:
            code = INTERNAL_ERROR
            data = {}
    else:
        code = INVALID_DATA
        data = {}
    return {
        'code': code,
        'raw': raw,
        'data': data
    }


