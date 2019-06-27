# -*- coding: utf-8 -*-
from django.urls import path
from django.views.generic import RedirectView

from api import views

urlpatterns = [
    path('get_location', views.get_location_request, name='get_location'),
    path('get_loc', RedirectView.as_view(url='/api/get_location', permanent=True)),
    path('get_cinema_by_location', views.get_cinema, name='get_cinema'),
    path('get_film', views.get_film_request, name='get_film'),
    path('get_film_detail', views.get_film_detail_request, name='get_film_detail_request'),
    path('get_seat_type', views.get_ticket_type_request, name='get_ticket_type_request'),
    path('get_seats', views.get_seats_request, name='get_seats_request'),
    path('get_seats_vista', views.get_seats_vista_request, name='get_seats_vista_request'),
    path('create_order', views.create_order_request, name='create_order_request'),
]