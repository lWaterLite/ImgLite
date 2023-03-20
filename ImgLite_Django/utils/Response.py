from django.http import HttpResponse
from json import dumps


class BadResponse(HttpResponse):
    status_code = 400
    content_type = 'application/json'


class NotFoundResponse(HttpResponse):
    status_code = 404
    content_type = 'application/json'


class BadRequestMethodResponse(BadResponse):
    content = dumps({
        'message': 'bad request method',
        'status': 'false'
    })
