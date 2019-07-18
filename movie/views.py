
from urllib.parse import urlencode

from django.http import HttpResponseRedirect
from datetime import datetime

from django.urls import reverse

from api.services.config import PASSWORD, URL_BACK_TO_APP
from movie.AESCipher import AESCipher

def validate_data(request):
    if request.method == "GET":
        params = request.GET
        password = PASSWORD
        aes_cipher = AESCipher(password)
        if 'data' in params:
            try:
                raw_data = aes_cipher.decrypt(params['data'])
                result = get_data_from_raw(raw_data)
                if result and result['code'] == '00':
                    return result['data'], ''
                else:
                    return None, 'Dữ liệu không hợp lệ hoặc bạn không có quyền truy cập dịch vụ này.'
            except ValueError as e:
                return None, 'Dữ liệu không hợp lệ hoặc bạn không có quyền truy cập dịch vụ này.'

        else:
            return None, 'Dữ liệu không hợp lệ hoặc bạn không có quyền truy cập dịch vụ này.'
    else:
        return None, 'Dữ liệu không hợp lệ hoặc bạn không có quyền truy cập dịch vụ này.'

def index(request, *args, **kwargs):
    data, error = validate_data(request)
    if error == "":
        return custom_redirect('index', *(), **data)
    else:
        return HttpResponseRedirect(URL_BACK_TO_APP + "&reason=error&code=%s&message=%s" % ('01', error))

def order_preview(request, *args, **kwargs):
    data, error = validate_data(request)
    if error == "":
        if request.GET.get('payCode'):
            return custom_redirect('preview', *(), **data, payCode=request.GET.get('payCode'))
        return HttpResponseRedirect(URL_BACK_TO_APP + "&reason=error&code=%s&message=%s" % ('01', 'Missing parameter (payCode)'))
    else:
        return HttpResponseRedirect(URL_BACK_TO_APP + "&reason=error&code=%s&message=%s" % ('01', error))

def create_bill(request, *args, **kwargs):
    data, error = validate_data(request)
    if error == "":
        if request.GET.get('payCode'):
            return custom_redirect('bill', *(), **data, payCode=request.GET.get('payCode'))
        return HttpResponseRedirect(URL_BACK_TO_APP + "&reason=error&code=%s&message=%s" % ('01', 'Missing parameter (payCode)'))
    else:
        return HttpResponseRedirect(URL_BACK_TO_APP + "&reason=error&code=%s&message=%s" % ('01', error))


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
        timestamp = datetime.now().timestamp()
        raw_token = "%s|%s" % (raw, timestamp)
        password = PASSWORD
        aes_cipher = AESCipher(password)
        try:
            token = aes_cipher.encrypt(raw_token)
            code = '00'
        except ValueError as e:
            code = '01'
            return {
                'code': code,
                'message': str(e),
                'data': {

                }
            }
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


