from django.http import JsonResponse

# Create your views here.
from api.services import get_cinema_by_location


def get_cinema(request):
    return JsonResponse(get_cinema_by_location.call(93))
