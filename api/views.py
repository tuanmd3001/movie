from django.http import JsonResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from api.services import get_cinema_by_location, get_ticket_type, get_seats, get_seats_vista, create_order
import json


def get_cinema(request):
    return JsonResponse(get_cinema_by_location.call(93))


def get_ticket_type_request(request):
    app_mobile = request.GET.get('app_mobile')
    ss_id = request.GET.get('ss_id')
    request_id = request.GET.get('request_id')
    language = request.GET.get('language')
    return JsonResponse(get_ticket_type.call(app_mobile, ss_id, request_id, language))


def get_seats_request(request):
    app_mobile = request.GET.get('app_mobile')
    book_service_id = request.GET.get('book_service_id')
    ss_id = request.GET.get('ss_id')
    request_id = request.GET.get('request_id')
    language = request.GET.get('language')
    return JsonResponse(get_seats.call(app_mobile, ss_id, book_service_id, request_id, language))


@csrf_exempt
def get_seats_vista_request(request):
    post_data = json.loads(request.body)
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

