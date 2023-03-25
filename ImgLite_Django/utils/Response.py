from django.http import HttpResponse
from json import dumps


class BadResponse(HttpResponse):
    """
    Inherited from HttpResponse.\n
    Set Content-Type="application/json" and
    status_code=400
    """
    status_code = 400
    content_type = 'application/json'


class BadUUIDResponse(BadResponse):
    """
    Inherited from BadResponse.\n
    Fix the content with json object:
        message: "bad user uuid in request"\n
        status； “false”
    """
    content = dumps({
        'message': 'bad user uuid in request',
        'status': 'false'
    })


class NotFoundResponse(HttpResponse):
    """
    Inherited from HttpResponse.\n
    Set Content-Type="application/json" and status_code=404.
    """
    status_code = 404
    content_type = 'application/json'


class BadRequestMethodResponse(BadResponse):
    """
    Inherited from BadResponse. Fix the content with json object:
        message: 'bad request method'\n
        status: 'false'
    """
    content = dumps({
        'message': 'bad request method',
        'status': 'false'
    })
