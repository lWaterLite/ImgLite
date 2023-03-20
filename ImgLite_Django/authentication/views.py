import uuid
from json import dumps
from time import time

import django.middleware.csrf
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from utils.Encryption import RsaDecrypt, RsaEncrypt
from utils.Response import BadResponse, BadRequestMethodResponse
from .models import UserIndex, InviteCode


def login(request):
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


def register(request):
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


def get_csrf_token(request):
    django.middleware.csrf.get_token(request)
    return HttpResponse(dumps({'message': 'success'}), headers={'Content-Type': 'application/json'})
