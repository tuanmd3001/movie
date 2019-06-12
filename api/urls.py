# -*- coding: utf-8 -*-
from django.urls import path
from api import views

urlpatterns = [
    path('get_cinema_by_location', views.get_cinema_by_location, name='get_cinema_by_location'),
]