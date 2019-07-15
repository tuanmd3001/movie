# -*- coding: utf-8 -*-
from datetime import datetime

SERVICE_DOMAIN = "http://127.0.0.1:8688/"
APP_ID = "SCB"
VERSION = 2
URL_BACK_TO_APP = "https://filmservice.vnpaytest.vn/backtoapp/?action=backtoapp"
PASSWORD = "Sacombank_Vnpay"


SERVICE_URLS = {
    'get_location': SERVICE_DOMAIN + 'get_location',
    'get_cinema_by_location': SERVICE_DOMAIN + 'get_cinema_by_location',
    'get_film': SERVICE_DOMAIN + 'get_film',
    'search_film': SERVICE_DOMAIN + 'search_film',
    'get_my_films': SERVICE_DOMAIN + 'get_my_films',
    'get_book_ticket': SERVICE_DOMAIN + 'get_book_ticket',
    'get_film_by_id': SERVICE_DOMAIN + 'get_film_by_id',
    'get_ticket_type': SERVICE_DOMAIN + 'get_ticket_type',
    'get_seats': SERVICE_DOMAIN + 'get_seats_v2',
    'create_order': SERVICE_DOMAIN + 'create_order',
    'cancel_order': SERVICE_DOMAIN + 'cancel_order',
    'get_order_detail': SERVICE_DOMAIN + 'get_order_detail',
    'create_bill': SERVICE_DOMAIN + 'create_bill',
}


def get_checksum():
    return "123201906109834999037620190610171730123456"


def get_request_date():
    return datetime.now().strftime('%Y%m%d%H%M%S')
