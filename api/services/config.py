# -*- coding: utf-8 -*-
SERVICE_DOMAIN = "http://localhost:8688/"
APP_ID = "123"
VERSION = 2

SERVICE_URLS = {
    'get_location' : SERVICE_DOMAIN + 'get_location',
    'get_cinema_by_location' : SERVICE_DOMAIN + 'get_cinema_by_location',
    'get_film' : SERVICE_DOMAIN + 'get_film',
    'get_film_by_id' : SERVICE_DOMAIN + 'get_film_by_id',
    'get_ticket_type' : SERVICE_DOMAIN + 'get_ticket_type',
    'get_seats' : SERVICE_DOMAIN + 'get_seats',
    'create_order' : SERVICE_DOMAIN + 'create_order',

}

def get_checksum():
    return "123201906109834999037620190610171730123456"

def get_request_date():
    return '20190610171730'