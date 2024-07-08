
from django.core.cache import cache
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
import time
from collections import defaultdict
RATE_LIMIT = 4 #requests
TIME_WINDOW = 1 #seconds

def get_user_key(request):

    user_id, user_name = request.GET.get('user_id',), request.GET.get('user_name')

    return user_id, user_name

    # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    # if x_forwarded_for:
    #     ip_address = x_forwarded_for.split(',')[0]
    # else:
    #     ip_address = request.META.get('REMOTE_ADDR')
    # return ip_address
cache_storage = defaultdict(lambda: (0, time.time()))
def rate_limit_middleware(get_response):

    def middleware(request):

        # user_ip = get_user_key(request)
        user_id, user_name = get_user_key(request)
        cache_key = f"rate_limit_{user_id}_{user_name}"

        request_count, first_request_time = cache.get(cache_key, (0, time.time()))
        print(request_count)
        print(time.time() - first_request_time)
        if time.time() - first_request_time > TIME_WINDOW:
            request_count = 0
            first_request_time = time.time()
        
        request_count += 1

        if request_count > RATE_LIMIT:

            return JsonResponse({"error": "Rate limit exceeded"}, status=429)

        cache.set(cache_key, (request_count, first_request_time), timeout=TIME_WINDOW) # type: ignore

        response = get_response(request)

        return response

    return middleware