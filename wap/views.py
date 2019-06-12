from django.shortcuts import render

# Create your views here.
from api.services import get_location, get_film


def index(request):
    location_list = get_location.call()
    return render(request, 'wap/index.html', {'locations': location_list})


def get_film_by_cinema(request, cinema_id):
    film_list = get_film.call(cinema_id)
    film_showing = []
    film_coming = []
    for film in film_list:
        if film['statusId'] == 1:
            film_coming.append(film)
        elif film['statusId'] == 2:
            film_showing.append(film)
    return render(request, 'wap/film_by_cinema.html', {'film_showing': film_showing, 'film_coming': film_coming})
