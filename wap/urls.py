# -*- coding: utf-8 -*-

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cinema/<int:location_id>/<int:cinema_id>/', views.get_film_by_cinema, name='get_film_by_cinema'),

    path('movie/<int:cinema_id>/<int:film_id>', views.get_film_detail_by_cinema, name='get_film_detail_by_cinema'),
    path('movie/<int:film_id>', views.get_film_detail, name='get_film_detail'),

    path('ticket_type/<int:cinema_id>/<int:film_id>/<int:session_id>', views.ticket_type, name='get_ticket_type_by_cinema'),
    path('ticket_type/<int:film_id>/<int:session_id>', views.ticket_type, name='get_ticket_type'),

    path('choose_seats/<int:cinema_id>/<int:film_id>/<int:session_id>/<int:book_service_id>', views.get_seats, name='get_seats_by_cinema'),
    path('choose_seats/<int:film_id>/<int:session_id>/<int:book_service_id>', views.get_seats, name='get_seats'),

]