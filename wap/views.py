from functools import wraps
from turtledemo.penrose import f

import json

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from datetime import datetime, timedelta

from django.urls import reverse, resolve

from api.services import get_location, get_film, get_film_by_id, get_ticket_type, get_seats_vista, \
    get_seats as get_seats_api


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
            kwargs['app_mobile'] = params.get('app_mobile')
        return function(request, *args, **kwargs)

    return wrap


def string_to_datetime(string, date_format="%d/%m/%Y %H:%M:%S"):
    try:
        date = datetime.strptime(string, date_format)
        return date
    except:
        return None

def custom_redirect(url_name, *args, **kwargs):
    import urllib
    url = reverse(url_name, args = args)
    params = urllib.parse.urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)


def call_service(request, service, *params):
    response = service.call(*params)
    if response:
        if 'code' in response and response['code'] == "00":
            return response['data']
        else:
            messages.error(request, response['message'])
    else:
        messages.error(request, "Không thể kết nối dịch vụ. Vui lòng thử lại")

    return None

@has_app_mobile
def index(request, *args, **kwargs):
    location_list = call_service(request, get_location)
    return render(request, 'wap/index.html', {
        'locations': location_list,
        'tab': request.GET.get('tab') if request.GET.get('tab') else "",
        'location': request.GET.get('location') if request.GET.get('location') else "",
        **kwargs
    })


@has_app_mobile
def get_film_by_cinema(request, *args, **kwargs):
    cinema_name = "Chọn phim"
    film_showing = []
    film_coming = []
    film_list = call_service(request, get_film, kwargs['cinema_id'])
    if film_list:
        for film in film_list:
            if cinema_name == "Chọn phim" and "cinemaName" in film and film['cinemaName'] != "":
                cinema_name = film['cinemaName']
            if film['statusId'] == 1:
                film_coming.append(film)
            elif film['statusId'] == 2:
                film_showing.append(film)
    return render(request, 'wap/film_by_cinema.html', {
        'film_showing': film_showing,
        'film_coming': film_coming,
        'cinema_name': cinema_name,
        **kwargs
    })


@has_app_mobile
def get_film_detail_by_cinema(request, *args, **kwargs):
    film = None
    from_date = datetime.now()
    date_range = 7
    to_date = from_date + timedelta(days=date_range)
    sessions = {}
    dates = [single_date for single_date in (from_date + timedelta(n) for n in range(date_range))]
    film_detail = call_service(request, get_film_by_id, kwargs['film_id'], from_date, to_date, kwargs['cinema_id'])
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
        'film': film,
        'sessions': sessions,
        'dates': dates,
        'is_booking': request.GET.get('tab') == "tab-booking",
        **kwargs
    })


@has_app_mobile
def get_film_detail(request, *args, **kwargs):
    film = None
    from_date = datetime.now()
    date_range = 7
    to_date = from_date + timedelta(days=date_range)
    sessions = {}
    dates = [single_date for single_date in (from_date + timedelta(n) for n in range(date_range))]
    film_detail = call_service(request, get_film_by_id, kwargs['film_id'], from_date, to_date)
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
        'film': film,
        'sessions': sessions,
        'dates': dates,
        'is_booking': request.GET.get('tab') == "tab-booking",
        **kwargs
    })


@has_app_mobile
def ticket_type(request, *args, **kwargs):
    ticket_types = None
    if request.method == "GET":
        ticket_types = call_service(request, get_ticket_type, kwargs['app_mobile'], kwargs['session_id'])
    elif request.method == "POST":
        ticket_types = request.POST.get('ticket_types')
        if not ticket_types:
            ticket_types = call_service(request, get_ticket_type, kwargs['app_mobile'], kwargs['session_id'])
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
            seats = call_service(request, get_seats_vista, params)
            if seats:
                kwargs['seats'] = seats
                return get_seats(request, *args, **kwargs)

    return render(request, 'wap/ticket_type.html', {
        'ticket_types': ticket_types,
        'ticket_types_json': json.dumps(ticket_types),
        **kwargs
    })


@has_app_mobile
def get_seats(request, *args, **kwargs):
    if kwargs.get('seats'):
        seats = kwargs.get('seats')
    else:
        seats = call_service(request, get_seats_api, kwargs['app_mobile'], kwargs['session_id'], kwargs['book_service_id'])
        if not seats:
            if 'cinema_id' not in kwargs:
                return custom_redirect('get_film_detail', kwargs['film_id'], app_mobile=kwargs['app_mobile'])
            else:
                return custom_redirect('get_film_detail_by_cinema', kwargs['cinema_id'], kwargs['film_id'], app_mobile=kwargs['app_mobile'])

    if resolve(request.path_info).url_name == "get_ticket_type":
        back_url = request.path
    else:
        if 'cinema_id' in kwargs:
            back_url = reverse('get_film_detail_by_cinema', kwargs={
                'cinema_id': kwargs['cinema_id'],
                'film_id': kwargs['film_id']
            }) + "?app_mobile=" + kwargs['app_mobile'] + '&tab=tab-booking'
        else:
            back_url = reverse('get_film_detail', kwargs={
                'film_id': kwargs['film_id']
            }) + "?app_mobile=" + kwargs['app_mobile'] + '&tab=tab-booking'
    return render(request, 'wap/seats.html', {
        **kwargs,
        "back_url": back_url,
        "seats": seats,
    })
