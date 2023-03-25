import uuid
from json import dumps
from time import time

import django.middleware.csrf
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from utils.Encryption import RsaDecrypt, RsaEncrypt
from utils.Response import BadResponse, BadRequestMethodResponse
from .models import UserIndex, InviteCode


def login(request) -> HttpResponse:
    """
    This view is used to log in the image hosting site.\n
    The full api is "api/auth/login?userAccount=<userAccount>&userPassword=<userPassword>".\n
    The params are:
        userAccount: users' account.\n
        userPassword: users' password.\n
    Be advised that both of them MUST be RSA encrypted.\n
    The requesting method MUST be GET, any other methods are forbidden.\n

    Args:
        request: The default param of django view functon.

    Returns:
        HttpResponse, Content-Type="application/json".
            It contains the success info or error info.
            When success, it will return a HttpResponse contains json object with two key-values:
                userUUID: string, the user's uuid, be advised that it is RSA encrypted.
                status: string, the login status, true when success.
            When failed, it will return a HttpResponse contains json object with two key-values:
                message: string, the detail error message of the failure.
                status: string, false when failed.
            If requesting method is unaccepted, it will return a BadRequestMethodResponse,
                see details in its docstring.
    """
    if request.method == 'GET':
        userAccount = RsaDecrypt(request.GET.get('userAccount', ''))
        userPassword = RsaDecrypt(request.GET.get('userPassword', ''))
        try:
            user = UserIndex.objects.filter(userAccount=userAccount, userPassword=userPassword).get()
        except ObjectDoesNotExist:
            response = BadResponse(dumps({
                'message': '用户名或密码错误',
                'status': 'false'
            }))
            return response
        else:
            response = HttpResponse()
            userUUID = RsaEncrypt(user.userUUID)
            response.content = dumps({
                'userUUID': userUUID,
                'status': 'true'
            })
            response.content_type = 'application/json'
            return response
    else:
        return BadRequestMethodResponse()


def register(request) -> HttpResponse:
    """
    This view is used to register in image hosting site.\n
    The full api is "api/auth/register".\n
    The requesting method MUST be POST, any other methods are forbidden.\n
    The POST params are:
        userAccount: users' account.\n
        userPassword: users' password.\n
        inviteCode: the invite code for registering.\n
    Be advised that both of userAccount and userPassword MUST be RSA encrypted.


    Args:
        request: The default param of django view functon.

    Returns:
        HttpResponse, Content-Type="application/json".
        Either success or failed it contains json object with two key-values:
            message: string, the register status message, giving the detail info when failed.
            status: string, true when success, false otherwise.
        If requesting method is unaccepted, it will return a BadRequestMethodResponse,
                see details in its docstring.
    """
    if request.method == 'POST':
        userAccount = RsaDecrypt(request.POST['userAccount'])
        userPassword = RsaDecrypt(request.POST['userPassword'])
        inviteCode = RsaDecrypt(request.POST['inviteCode'])

        if UserIndex.objects.filter(userAccount=userAccount):
            response = BadResponse(dumps({
                'message': '此用户名已被注册',
                'status': 'false'
            }))
            return response
        else:
            if InviteCode.objects.filter(inviteCode=inviteCode):
                userIndex = str(int(round(time()*1000000)))
                userUUID = uuid.uuid3(uuid.NAMESPACE_DNS, userAccount).hex
                UserIndex.objects.create(userIndex=userIndex,
                                         userAccount=userAccount, userPassword=userPassword, userUUID=userUUID)
                return HttpResponse(dumps({
                    'message': '注册成功',
                    'status': 'false'
                }))
            else:
                response = BadResponse(dumps({
                    'message': '邀请码无效，请重新输入',
                    'status': 'false'
                }))
                return response
    else:
        return BadRequestMethodResponse()


def get_csrf_token(request) -> HttpResponse:
    """
    This view is used to get CSRF token.\n
    The full api is "api/token".\n
    Use it before requesting with insecure method,
    for details please check 'https://docs.djangoproject.com/en/4.1/ref/csrf/'

    Args:
        request: The default param of django view functon.

    Returns:
        HttpResponse, Content-Type=""application/json".
            It just contains the success message.
            However, the Set-Cookie Header is auto set, check it in django's doc with the link above.
    """
    django.middleware.csrf.get_token(request)
    return HttpResponse(dumps({'message': 'success'}), headers={'Content-Type': 'application/json'})
