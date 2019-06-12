# -*- coding: utf-8 -*-

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cinema/<int:cinema_id>', views.get_film_by_cinema, name='get_film_by_cinema'),
]