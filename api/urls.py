# -*- coding: utf-8 -*-
from django.urls import path
from api import views

urlpatterns = [
    path('get_cinema_by_location', views.get_cinema, name='get_cinema'),
    path('get_seat_type', views.get_ticket_type_request, name='get_ticket_type_request'),
    path('get_seats', views.get_seats_request, name='get_seats_request'),
    path('get_seats_vista', views.get_seats_vista_request, name='get_seats_vista_request'),

]