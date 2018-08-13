import json
from django.http import HttpResponse

def JsonMiddleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        try:
            body_unicode = request.body.decode('utf-8')
            res = json.loads(body_unicode)
            request.json = res
        except :
            request.json = {}
        response = get_response(request)
        return response

    return middleware