from django.shortcuts import render
from datetime import datetime, timedelta

# Create your views here.
from api.services import get_location, get_film, get_film_by_id


def index(request):
    location_list = get_location.call()
    return render(request, 'wap/index.html', {'locations': location_list})


def get_film_by_cinema(request, cinema_id):
    film_list = get_film.call(cinema_id)
    film_showing = []
    film_coming = []
    cinema_name = "Chọn phim"
    for film in film_list:
        if film['cinemaName'] and film['cinemaName'] != "":
            cinema_name = film['cinemaName']
        film['publishDate'] = datetime.strptime(film['publishDate'], "%d/%m/%Y %H:%M:%S").strftime("%d/%m/%Y")
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
    film_list = get_film_by_id.call(cinema_id, film_id)
    film_showing = []
    film_coming = []
    for film in film_list:
        film['publishDate'] = datetime.strptime(film['publishDate'], "%d/%m/%Y %H:%M:%S").strftime("%d/%m/%Y")
        duration = str(timedelta(minutes=film['duration']))[:-3].split(":")
        film['duration'] = duration[0] + " giờ " + duration[1] + " phút"
        if film['statusId'] == 1:
            film_coming.append(film)
        elif film['statusId'] == 2:
            film_showing.append(film)
    return render(request, 'wap/film_by_cinema.html', {'film_showing': film_showing, 'film_coming': film_coming})
