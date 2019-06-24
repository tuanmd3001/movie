from django.http import JsonResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from api.services import get_cinema_by_location, get_ticket_type, get_seats, get_seats_vista, create_order, get_film
from api.services.config import APP_ID
import json

from api.services.error_code import ERROR_MISSING_PARAM, error_message


def get_film_request(request):
    app_mobile = check_param(request.GET, 'app_mobile')
    cinema_id = check_param(request.GET, 'cinema_id')
    location_id = check_param(request.GET, 'location_id')
    status_id = check_param(request.GET, 'status_id')
    if not app_mobile:
        return response_error(ERROR_MISSING_PARAM, error_message.get(ERROR_MISSING_PARAM) + 'app_mobile')
    if not cinema_id:
        cinema_id = 0
    if not location_id:
        location_id = 0
    if not status_id:
        status_id = 0
    return JsonResponse(get_film.call(cinema_id, location_id, status_id))


def get_cinema(request):
    app_mobile = check_param(request.GET, 'app_mobile')
    location_id = check_param(request.GET, 'location_id')
    if not app_mobile:
        return response_error(ERROR_MISSING_PARAM, error_message.get(ERROR_MISSING_PARAM) + 'app_mobile')
    if not location_id:
        return response_error(ERROR_MISSING_PARAM, error_message.get(ERROR_MISSING_PARAM) + 'location_id')
    return JsonResponse(get_cinema_by_location.call(location_id))


def get_ticket_type_request(request):
    app_mobile = check_param(request.GET, 'app_mobile')
    ss_id = check_param(request.GET, 'ss_id')
    request_id = check_param(request.GET, 'request_id')
    language = check_param(request.GET, 'language')
    if not app_mobile:
        return response_error(ERROR_MISSING_PARAM, error_message.get(ERROR_MISSING_PARAM) + 'app_mobile')
    if not ss_id:
        return response_error(ERROR_MISSING_PARAM, error_message.get(ERROR_MISSING_PARAM) + 'ss_id')
    if not request_id:
        request_id = 0
    if not language:
        language = 'VN'
    return JsonResponse(get_ticket_type.call(app_mobile, ss_id, request_id, language))


def get_seats_request(request):
    app_mobile = check_param(request.GET, 'app_mobile')
    ss_id = check_param(request.GET, 'ss_id')
    request_id = check_param(request.GET, 'request_id')
    book_service_id = check_param(request.GET, 'book_service_id')
    language = check_param(request.GET, 'language')
    if not app_mobile:
        return response_error(ERROR_MISSING_PARAM, error_message.get(ERROR_MISSING_PARAM) + 'app_mobile')
    if not ss_id:
        return response_error(ERROR_MISSING_PARAM, error_message.get(ERROR_MISSING_PARAM) + 'ss_id')
    if not book_service_id:
        return response_error(ERROR_MISSING_PARAM, error_message.get(ERROR_MISSING_PARAM) + 'book_service_id')
    if not request_id:
        request_id = 0
    if not language:
        language = 'VN'
    return JsonResponse(get_seats.call(app_mobile, ss_id, book_service_id, request_id, language))


# {
#     "app_mobile": "0943378298",
#     "request_id": "14932",
#     "language": "VN",
#     "queryId": 14932,
#     "ticketTypes": [
#         {
#             "ticketTypeId": 45983,
#             "quantity": 2
#         }
#     ],
#     "book_service_id": 0,
#     "ss_id": 2325085
# }
@csrf_exempt
def get_seats_vista_request(request):
    post_data = json.loads(request.body)
    app_mobile = check_param(post_data, 'app_mobile')
    ss_id = check_param(post_data, 'ss_id')
    request_id = check_param(post_data, 'request_id')
    queryId = check_param(post_data, 'queryId')
    book_service_id = check_param(post_data, 'book_service_id')
    language = check_param(post_data, 'language')
    ticketTypes = check_param(post_data, 'ticketTypes')
    if not app_mobile:
        return response_error(ERROR_MISSING_PARAM, error_message.get(ERROR_MISSING_PARAM) + 'app_mobile')
    if not ss_id:
        return response_error(ERROR_MISSING_PARAM, error_message.get(ERROR_MISSING_PARAM) + 'ss_id')
    if not book_service_id:
        return response_error(ERROR_MISSING_PARAM, error_message.get(ERROR_MISSING_PARAM) + 'book_service_id')
    if not request_id:
        return response_error(ERROR_MISSING_PARAM, error_message.get(ERROR_MISSING_PARAM) + 'request_id')
    if not queryId:
        return response_error(ERROR_MISSING_PARAM, error_message.get(ERROR_MISSING_PARAM) + 'queryId')
    if not ticketTypes:
        return response_error(ERROR_MISSING_PARAM, error_message.get(ERROR_MISSING_PARAM) + 'ticketTypes')
    if not language:
        post_data['language'] = 'VN'
    return JsonResponse(get_seats_vista.call(post_data))


# {
# "app_id":1,
# "queryId": {{query_id}},
# "customerName":"Nguyen Van A",
# "customeEmail":"hienht@vnpay.vn",
# "customerPhone":"0987654321",
# "seats":
# 	[
#         {
#             "seatId": {{seat_id}},
#             "code": "{{seat_code}}"
#         }
#     ],
# "language": "VN"
# }
@csrf_exempt
def create_order_request(request):
    post_data = json.loads(request.body)
    return JsonResponse(create_order.call(post_data))


def check_param(dic, key):
    if key in dic:
        return dic.get(key)
    else:
        return None


def response_error(code, message):
    r = {
        'app_id' : APP_ID,
        'code' : code,
        'message': message
    }
    return JsonResponse(r)

