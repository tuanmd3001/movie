"""movie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from movie import views

urlpatterns = [
    path('wap/', include('wap.urls')),
    path('api/', include('api.urls')),
    path('way-to-app/', views.index, name='index_home'),
    path('way-to-detail/', views.order_preview, name='order_preview'),
    path('way-to-vat/', views.create_bill, name='create_bill'),
]
