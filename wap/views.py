import numbers
from functools import wraps

import json
from urllib import parse

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from datetime import datetime, timedelta

from django.urls import reverse, resolve
from django.views.decorators.cache import cache_control

from api.services import get_location, get_film, get_film_by_id, get_ticket_type, get_seats_vista, \
    get_seats as get_seats_api, get_ticket_detail, create_order, get_order_detail, create_bill as create_bill_api
from api.services.config import PASSWORD, URL_BACK_TO_APP, SUCCESS, SESSION_EXPIRED, INTERNAL_ERROR, INVALID_DATA
from movie.AESCipher import AESCipher


def validate_request(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        params = None
        if request.method == 'GET':
            params = request.GET
        elif request.method == 'POST':
            params = request.POST

        # validate token
        if 'token' not in params or params.get('token') == '':
            result = {
                "code": INVALID_DATA,
                "raw": "",
                "lang": "EN" if 'language' in params and params['language'] == 'ENG' else 'VI'
            }
            return redirect_error(result)
        else:
            result = verify_token(token=params['token'])
            if result['code'] != SUCCESS:
                result['language'] = "EN" if 'language' in params and params['language'] == 'ENG' else 'VI'
                return redirect_error(result)
            else:
                # has app_mobile
                if 'app_mobile' not in params or params.get('app_mobile') == '':
                    messages.error(request, "Missing parameter (app_mobile)")
                    if resolve(request.path_info).url_name != "index":
                        return HttpResponseRedirect(reverse('index'))
                else:
                    for key, val in params.items():
                        if key == 'token':
                            kwargs['token_encoded'] = parse.quote(val)
                        kwargs[key] = val
                return function(request, *args, **kwargs)
    return wrap


def verify_token(token):
    password = PASSWORD
    try:
        aes_cipher = AESCipher(password)
        raw = aes_cipher.decrypt(token)
        list_data = raw.split('|')
        if len(list_data) == 7 or len(list_data) == 8:
            if len(list_data) == 8:
                paycode = list_data[6]
            else:
                paycode = ""
            timestamp = list_data[len(list_data) - 1]
            now = datetime.now().timestamp()
            raw = raw.replace("|%s" % timestamp, "")
            if len(paycode) > 0:
                raw = raw.replace("|%s" % paycode, "")
            try:
                if now < float(timestamp) + 1800:
                    code = SUCCESS
                else:
                    code = SESSION_EXPIRED
            except Exception as e:
                code = INTERNAL_ERROR
        else:
            code = INVALID_DATA
            raw = ""
    except ValueError as e:
        code = INTERNAL_ERROR
        raw = ""
        paycode = ""
    return {
        "code": code,
        "raw": raw,
        "paycode": paycode
    }


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


def redirect_success(result):
    raw_data = result['raw']
    if len(raw_data) > 0:
        raw_data = "%s|%s|%s" % (raw_data, result['paycode'], 'PAYNOW')
        password = PASSWORD
        aes_cipher = AESCipher(password)
        try:
            return_data = aes_cipher.encrypt(raw_data)
        except ValueError as e:
            return_data = ""
        return HttpResponseRedirect(URL_BACK_TO_APP + "&data=%s&lang=%s" % (return_data, result['lang']))
    else:
        return HttpResponseRedirect(URL_BACK_TO_APP + "&lang=%s" % result['lang'])


def build_back_url(result, isPayment):
    raw_data = result['raw']
    if len(raw_data) > 0:
        if isPayment:
            raw_data = "%s|%s|%s" % (raw_data, result['paycode'], 'PAYNOW')
        else:
            raw_data = "%s|%s" %(raw_data, SUCCESS)
        password = PASSWORD
        aes_cipher = AESCipher(password)
        try:
            return_data = aes_cipher.encrypt(raw_data)
        except ValueError as e:
            return_data = ""
        return URL_BACK_TO_APP + "&data=%s&lang=%s" % (return_data, result['lang'])
    else:
        return URL_BACK_TO_APP + "&lang=%s" % result['lang']


def has_app_mobile(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        params = None
        if request.method == "GET":
            params = request.GET
        elif request.method == "POST":
            params = request.POST
        if 'app_mobile' not in params or params.get('app_mobile') == '':
            messages.error(request, "Thiếu tham số (app_mobile)")
            if resolve(request.path_info).url_name != "index":
                return HttpResponseRedirect(reverse('index'))
        else:
            for key, val in params.items():
                if key == 'token':
                    kwargs['token_encoded'] = parse.quote(val)
                kwargs[key] = val
        return function(request, *args, **kwargs)

    return wrap


def string_to_datetime(string, date_format="%d/%m/%Y %H:%M:%S"):
    try:
        date = datetime.strptime(string, date_format)
        return date
    except ():
        return None


def custom_redirect(url_name, *args, **kwargs):
    url = reverse(url_name, args = args)
    params = parse.urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)


def call_service(request, service, *params):
    response = service.call(*params)
    message = ''
    if response:
        if 'code' in response and response['code'] == "00":
            return response['data'], message
        else:
            messages.error(request, response['message'])
            message = response['message']
    else:
        messages.error(request, "Không thể kết nối dịch vụ. Vui lòng thử lại")
        message = 'Không thể kết nối dịch vụ. Vui lòng thử lại'

    return None, message


@validate_request
def index(request, *args, **kwargs):
    location_list, mess = call_service(request, get_location)
    return render(request, 'wap/index.html', {
        **kwargs,
        'locations': location_list,
        'tab': request.GET.get('tab') if request.GET.get('tab') else "",
        'location': request.GET.get('location') if request.GET.get('location') else ""
    })


@validate_request
def get_film_by_cinema(request, *args, **kwargs):
    cinema_name = "Chọn phim"
    film_showing = []
    film_coming = []
    film_list, mess = call_service(request, get_film, kwargs['cinema_id'])
    if film_list:
        for film in film_list:
            if cinema_name == "Chọn phim" and "cinemaName" in film and film['cinemaName'] != "":
                cinema_name = film['cinemaName']
            if film['statusId'] == 1:
                film_coming.append(film)
            elif film['statusId'] == 2:
                film_showing.append(film)
    return render(request, 'wap/film_by_cinema.html', {
        **kwargs,
        'film_showing': film_showing,
        'film_coming': film_coming,
        'cinema_name': cinema_name
    })


@validate_request
def get_film_detail_by_cinema(request, *args, **kwargs):
    film = None
    from_date = datetime.now()
    date_range = 11
    to_date = from_date + timedelta(days=date_range)
    sessions = {}
    dates = [single_date for single_date in (from_date + timedelta(n) for n in range(date_range))]
    film_detail, mess = call_service(request, get_film_by_id, kwargs['film_id'], from_date, to_date, kwargs['cinema_id'])
    if film_detail:
        film = film_detail['film']
        for date in dates:
            date_str = date.strftime("%d%m%Y")
            sessions[date_str] = {}
        if "listSession" in film_detail:
            for s in film_detail['listSession']:
                if s["sessionTime"] and s["sessionTime"] != "":
                    session_date = string_to_datetime(s["sessionTime"]).strftime("%d%m%Y")
                    if session_date and session_date in sessions:
                        if s['versionId'] not in sessions[session_date]:
                            sessions[session_date][s['versionId']] = []
                        sessions[session_date][s['versionId']].append(s)
    return render(request, 'wap/film_detail.html', {
        **kwargs,
        'film': film,
        'sessions': sessions,
        'dates': dates,
        'is_booking': request.GET.get('tab') == "tab-booking"
    })


@validate_request
def get_film_detail(request, *args, **kwargs):
    film = None
    from_date = datetime.now()
    date_range = 11
    to_date = from_date + timedelta(days=date_range)
    sessions = {}
    dates = [single_date for single_date in (from_date + timedelta(n) for n in range(date_range))]
    film_detail, mess = call_service(request, get_film_by_id, kwargs['film_id'], from_date, to_date)
    if film_detail:
        film = film_detail['film']
        for date in dates:
            date_str = date.strftime("%d%m%Y")
            sessions[date_str] = {}
        if "listSession" in film_detail:
            for s in film_detail['listSession']:
                if s["sessionTime"] and s["sessionTime"] != "":
                    session_date = string_to_datetime(s["sessionTime"]).strftime("%d%m%Y")
                    if session_date and session_date in sessions:
                        if s['cinemaGroupName'] not in sessions[session_date]:
                            sessions[session_date][s['cinemaGroupName']] = {
                                "cinemas": {},
                                "info": {
                                    "cinemaGroupName": s['cinemaGroupName'],
                                    "cinemaLogo": s['cinemaLogo']
                                }
                            }

                        if s['cinemaId'] not in sessions[session_date][s['cinemaGroupName']]['cinemas']:
                            sessions[session_date][s['cinemaGroupName']]['cinemas'][s['cinemaId']] = {
                                "sessions": {},
                                "info": {
                                    "cinemaId": s['cinemaId'],
                                    "cinemaName": s['cinemaName'],
                                    "cinemaAddress": s['cinemaAddress']
                                }
                            }
                        if s['versionId'] not in sessions[session_date][s['cinemaGroupName']]['cinemas'][s['cinemaId']][
                            'sessions']:
                            sessions[session_date][s['cinemaGroupName']]['cinemas'][s['cinemaId']]['sessions'][
                                s['versionId']] = []
                        sessions[session_date][s['cinemaGroupName']]['cinemas'][s['cinemaId']]['sessions'][
                            s['versionId']].append(s)

    return render(request, 'wap/film_detail.html', {
        **kwargs,
        'film': film,
        'sessions': sessions,
        'dates': dates,
        'is_booking': request.GET.get('tab') == "tab-booking",
    })


@validate_request
@cache_control(no_cache=True, must_revalidate=True)
def ticket_type(request, *args, **kwargs):
    ticket_types = None
    if request.method == "GET":
        ticket_types, mess = call_service(request, get_ticket_type, kwargs['app_mobile'], kwargs['session_id'])
        if not ticket_types:
            if 'cinema_id' in kwargs:
                return custom_redirect('get_film_detail_by_cinema', kwargs['location_id'], kwargs['cinema_id'], kwargs['film_id'], app_mobile=kwargs['app_mobile'], token=kwargs['token'], tab="tab-booking")
            else:
                return custom_redirect('get_film_detail', kwargs['film_id'], app_mobile=kwargs['app_mobile'], token=kwargs['token'], tab="tab-booking")

    elif request.method == "POST":
        ticket_types = request.POST.get('ticket_types')
        if not ticket_types:
            ticket_types, mess = call_service(request, get_ticket_type, kwargs['app_mobile'], kwargs['session_id'])
        else:
            ticket_types = json.loads(ticket_types)
            params = {
                "app_mobile": kwargs['app_mobile'],
                "request_id": ticket_types['queryId'],
                "language": "VN",
                "queryId": ticket_types['queryId'],
                "ticketTypes": [type for type in ticket_types['lstTicketType'] if type['quantity'] > 0],
                "book_service_id": ticket_types['bookServiceid'],
                "ss_id": ticket_types['ss_id'],
            }
            seats, mess = call_service(request, get_seats_vista, params)
            if seats:
                kwargs['seats'] = seats
                return get_seats(request, *args, **kwargs)

    return render(request, 'wap/ticket_type.html', {
        **kwargs,
        'ticket_types': ticket_types,
        'ticket_types_json': json.dumps(ticket_types)
    })


@validate_request
@cache_control(no_cache=True, must_revalidate=True)
def get_seats(request, *args, **kwargs):
    if kwargs.get('seats'):
        seats = kwargs.get('seats')
    else:
        seats, mess = call_service(request, get_seats_api, kwargs['app_mobile'], kwargs['session_id'], kwargs['book_service_id'])
        if not seats:
            if 'cinema_id' not in kwargs:
                return custom_redirect('get_film_detail', kwargs['film_id'], app_mobile=kwargs['app_mobile'], token=kwargs['token'], tab="tab-booking")
            else:
                return custom_redirect('get_film_detail_by_cinema', kwargs['location_id'], kwargs['cinema_id'], kwargs['film_id'], app_mobile=kwargs['app_mobile'], token=kwargs['token'], tab="tab-booking")

    if resolve(request.path_info).url_name in ["get_ticket_type", "get_ticket_type_by_cinema"]:
        back_url = request.path + "?app_mobile=" + kwargs['app_mobile'] + '&token=' + kwargs['token_encoded'] + '&tab=tab-booking'
    else:
        if 'cinema_id' in kwargs:
            back_url = reverse('get_film_detail_by_cinema', kwargs={
                'location_id': kwargs['location_id'],
                'cinema_id': kwargs['cinema_id'],
                'film_id': kwargs['film_id']
            }) + "?app_mobile=" + kwargs['app_mobile'] + '&token=' + kwargs['token_encoded'] + '&tab=tab-booking'
        else:
            back_url = reverse('get_film_detail', kwargs={
                'film_id': kwargs['film_id']
            }) + "?app_mobile=" + kwargs['app_mobile'] + '&token=' + kwargs['token_encoded'] + '&tab=tab-booking'
    return render(request, 'wap/seats.html', {
        **kwargs,
        "back_url": back_url,
        "seats": seats,
    })


@validate_request
def ticket_detail(request, *args, **kwargs):
    ticket, mess = call_service(request, get_ticket_detail, kwargs['ticket_id'])
    if ticket:
        return render(request, 'wap/ticket_detail.html', {
            **kwargs,
            "ticket": ticket
        })
    else:
        return custom_redirect('index', app_mobile=kwargs['app_mobile'], token=kwargs['token'], tab='ticket')


@validate_request
def order(request, *args, **kwargs):
    if request.method == 'POST':
        kwargs.update(json.loads(kwargs['payload']))
        kwargs['language'] = 'VN'
        order, mess = call_service(request, create_order, kwargs)
        if order is not None:
            result = verify_token(request.POST.get("token"))
            if result['code'] == SUCCESS:
                result['paycode'] = order['payCode']
                result["lang"] = "EN" if 'language' in kwargs and kwargs['language'] == 'ENG' else 'VI'
                return redirect_success(result)
            else:
                redirect_error(result)
        else:
            if 'cinema_id' in kwargs and 'location_id' in kwargs and 'film_id' in kwargs:
                return custom_redirect('get_film_detail_by_cinema', kwargs['location_id'], kwargs['cinema_id'], kwargs['film_id'],
                                       app_mobile=kwargs['app_mobile'], token=kwargs['token'], tab="tab-booking")
            elif 'film_id' in kwargs:
                return custom_redirect('get_film_detail', kwargs['film_id'],
                                       app_mobile=kwargs['app_mobile'], token=kwargs['token'],
                                       tab="tab-booking")
    return custom_redirect('index', app_mobile=kwargs['app_mobile'], token=kwargs['token'])


@validate_request
def preview(request, *args, **kwargs):
    if 'payCode' in kwargs:
        order_detail, mess = call_service(request, get_order_detail, kwargs['payCode'])
        if order_detail is None:
            result = {
                "code": INVALID_DATA,
                "raw": "",
                "lang": "EN" if 'language' in kwargs and kwargs['language'] == 'ENG' else 'VI'
            }
            return redirect_error(result)
        result = verify_token(request.GET.get("token"))
        result["lang"] = "EN" if 'language' in kwargs and kwargs['language'] == 'ENG' else 'VI'
        if result['code'] == SUCCESS:
            result['paycode'] = kwargs['payCode']
            back_url = build_back_url(result, True)
            return render(request, 'wap/preview.html', {
                **kwargs,
                "order_detail": order_detail,
                "back_url": back_url
            })
        else:
            redirect_error(result)
    else:
        result = {
            "code": INVALID_DATA,
            "raw": "",
            "lang": "EN" if 'language' in kwargs and kwargs['language'] == 'ENG' else 'VI'
        }
        return redirect_error(result)


@validate_request
def bill(request, *args, **kwargs):
    if 'payCode' in kwargs:
        if request.method == 'POST':
            data = request.POST.copy()
            data['paymentCode'] = data['payCode']
            data['billMethod'] = 'EMAIL'
            data['language'] = 'VN'
            create_bill, mess = call_service(request, create_bill_api, data)
            result = verify_token(request.GET.get("token"))
            if result['code'] == SUCCESS:
                result['paycode'] = data['payCode']
                result["lang"] = "EN" if 'language' in kwargs and kwargs['language'] == 'ENG' else 'VI'
                back_url = build_back_url(result, False)
                if create_bill is not None:
                    return render(request, 'wap/create_bill_success.html', {
                        **kwargs,
                        'back_url': back_url
                    })
        return render(request, 'wap/create_bill.html', {
            **kwargs
        })
    else:
        result = {
            "code": INVALID_DATA,
            "raw": "",
            "lang": "EN" if 'language' in kwargs and kwargs['language'] == 'ENG' else 'VI'
        }
        return redirect_error(result)
