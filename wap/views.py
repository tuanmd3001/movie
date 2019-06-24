from django.shortcuts import render
from datetime import datetime, timedelta

# Create your views here.
from api.services import get_location, get_film, get_film_by_id


def string_to_datetime(string, date_format="%d/%m/%Y %H:%M:%S"):
    try:
        date = datetime.strptime(string, date_format)
        return date
    except:
        return None


def index(request):
    location_list = get_location.call()
    return render(request, 'wap/index.html', {'locations': location_list})


def get_film_by_cinema(request, cinema_id):
    film_list = get_film.call(cinema_id)
    film_showing = []
    film_coming = []
    cinema_name = "Chọn phim"
    for film in film_list:
        if cinema_name == "Chọn phim" and film['cinemaName'] and film['cinemaName'] != "":
            cinema_name = film['cinemaName']
        duration = str(timedelta(minutes=film['duration']))[:-3].split(":")
        film['duration'] = duration[0] + " giờ " + duration[1] + " phút"
        if film['statusId'] == 1:
            film_coming.append(film)
        elif film['statusId'] == 2:
            film_showing.append(film)
    return render(request, 'wap/film_by_cinema.html', {
        'film_showing': film_showing,
        'film_coming': film_coming,
        'cinema_id': cinema_id,
        'cinema_name': cinema_name,
    })


def get_film_detail(request, cinema_id, film_id):
    from_date = datetime.now()
    date_range = 7
    to_date = from_date + timedelta(days=date_range)
    film_detail = get_film_by_id.call(cinema_id, film_id, from_date, to_date)
    sessions = {}
    dates = [single_date for single_date in (from_date + timedelta(n) for n in range(date_range))]
    for date in dates:
        date_str = date.strftime("%d%m%Y")
        sessions[date_str] = {}
    if film_detail['listSession']:
        for s in film_detail['listSession']:
            if s["sessionTime"] and s["sessionTime"] != "":
                session_date = string_to_datetime(s["sessionTime"]).strftime("%d%m%Y")
                if session_date and session_date in sessions:
                    if s['versionId'] not in sessions[session_date]:
                        sessions[session_date][s['versionId']] = []
                    sessions[session_date][s['versionId']].append(s)
    return render(request, 'wap/film_detail.html', {
        'film': film_detail['film'],
        'sessions': sessions,
        'cinema_id': cinema_id,
        'dates': dates
    })
