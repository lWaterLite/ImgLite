import os
import time
import uuid
from PIL import Image
from json import dumps
from django.http import HttpResponse, FileResponse
from django.db.models import ObjectDoesNotExist
from django.core.paginator import Paginator

from utils.Config import StaticPath
from utils.Encryption import RsaDecrypt
from utils.Response import BadRequestMethodResponse, BadResponse, NotFoundResponse
from .models import ImgIndex, ImgType, UserIndex


def getImgInfoListPageCount(request):
    if request.method == 'GET':
        userUUID = RsaDecrypt(request.GET.get('userUUID', ''))
        userIndex = UserIndex.objects.get(userUUID=userUUID).userIndex
        imgIndexObjectList = ImgIndex.objects.filter(userIndex=userIndex)
        if imgIndexObjectList.exists():
            return HttpResponse(dumps({
                'pageCount': imgIndexObjectList.count() // 15 + 1
            }), content_type='application/json')
        else:
            return HttpResponse(dumps({
                'pageCount': 0
            }), content_type='application/json')
    else:
        return BadRequestMethodResponse()


def getImgInfoListByUserUUID(request) -> HttpResponse:
    """
    @summary This view function returns all pictures' info of one user.

    @param request: The default param of django view function.
    @return: A HttpResponse, Content-Type="application/json", the detail content are as followed.

    For the content it MUST be a json array, containing the images' info.
    For ech element in array, it MUST BE an object. The key-value pair are as followed:
        - imgUUID: string, the uuid of image.
        - imgFilename: string, the filename of image, with suffix.
        - imgUploadDate: string, the upload date of image, in form of "YYYY-MM-DD".

    @warning This function only supports GET method, if you are trying request with any other method,
    it will return with a HttpResponse, containing json with an object. Inner content can be found in utils/Response.

    """
    if request.method == 'GET':
        userUUID = RsaDecrypt(request.GET.get('userUUID', ''))
        currentPage = int(request.GET.get('page', '1'))
        userIndex = UserIndex.objects.get(userUUID=userUUID).userIndex
        imgIndexObjectList = ImgIndex.objects.filter(userIndex=userIndex).order_by('imgUploadDate', 'imgUUID')
        if imgIndexObjectList.exists():
            imgInfoList = []
            pageObject = Paginator(imgIndexObjectList, 15)
            imgIndexObjectPagedList = pageObject.get_page(int(currentPage)).object_list
            for imgIndexObject in imgIndexObjectPagedList:
                imgUUID = imgIndexObject.imgUUID
                imgFilename = imgIndexObject.imgName + "." + imgIndexObject.imgType.imgTypeName
                imgUploadDate = str(imgIndexObject.imgUploadDate)
                imgInfoList.append({
                    'imgUUID': imgUUID,
                    'imgFilename': imgFilename,
                    'imgUploadDate': imgUploadDate
                })
            return HttpResponse(dumps(imgInfoList), content_type='application/json')
        else:
            return HttpResponse(dumps([]), content_type='application/json')
    else:
        return BadRequestMethodResponse()


def getImgBinaryByImgUUID(request, imgUUID):
    if request.method == 'GET':
        try:
            imgIndexObject = ImgIndex.objects.get(imgUUID=imgUUID)
        except ObjectDoesNotExist:
            return NotFoundResponse(dumps({
                'message': 'Fail to get picture file!'
            }))
        userIndex = imgIndexObject.userIndex.userIndex
        year, month, day = str(imgIndexObject.imgUploadDate).split('-')
        imgTypeName = imgIndexObject.imgType.imgTypeName
        imgUUID = imgIndexObject.imgUUID
        imgStaticFileName = f'{imgUUID}.{imgTypeName}'
        imgFileAbsolutePath = StaticPath + f'/{userIndex}/{year}/{month}/{day}/{imgStaticFileName}'
        if os.path.exists(imgFileAbsolutePath):
            imgFile = open(imgFileAbsolutePath, 'rb')
            return HttpResponse(imgFile, content_type=f'image/{imgTypeName}')
        else:
            return NotFoundResponse(dumps({
                'message': 'Fail to get picture file!'
            }))
    else:
        return BadRequestMethodResponse()


def getImgThumbByImgUUID(request, imgUUID):
    if request.method == 'GET':
        imgIndexObject = ImgIndex.objects.get(imgUUID=imgUUID)
        userIndex = imgIndexObject.userIndex.userIndex
        year, month, day = str(imgIndexObject.imgUploadDate).split('-')
        imgTypeName = imgIndexObject.imgType.imgTypeName
        imgUUID = imgIndexObject.imgUUID
        imgStaticFileName = f'{imgUUID}.{imgTypeName}'
        imgFileAbsolutePath = StaticPath + f'/{userIndex}/{year}/{month}/{day}/thumbs/{imgStaticFileName}'
        if os.path.exists(imgFileAbsolutePath):
            imgFile = open(imgFileAbsolutePath, 'rb')
            return HttpResponse(imgFile, content_type=f'image/{imgTypeName}')
        else:
            return NotFoundResponse(dumps({
                'message': 'Fail to get picture file!'
            }))
    else:
        return BadRequestMethodResponse()


def downloadImgFileByImgUUID(request, imgUUID):
    if request.method == 'GET':
        imgIndexObject = ImgIndex.objects.get(imgUUID=imgUUID)
        userIndex = imgIndexObject.userIndex.userIndex
        year, month, day = str(imgIndexObject.imgUploadDate).split('-')
        imgTypeName = imgIndexObject.imgType.imgTypeName
        imgName = imgIndexObject.imgName
        imgUUID = imgIndexObject.imgUUID
        imgStaticFileName = f'{imgUUID}.{imgTypeName}'
        imgFileAbsolutePath = StaticPath + f'/{userIndex}/{year}/{month}/{day}/{imgStaticFileName}'
        if os.path.exists(imgFileAbsolutePath):
            imgFile = open(imgFileAbsolutePath, 'rb')
            response = FileResponse(imgFile)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = f'attachment;filename="{imgName}.{imgTypeName}"'
            return response
        else:
            return NotFoundResponse(dumps({
                'message': 'Fail to get picture file!'
            }))
    else:
        return BadRequestMethodResponse()


def uploadImgFile(request):
    if request.method == 'POST':
        userUUID = RsaDecrypt(request.POST['userUUID'])
        userIndexObject = UserIndex.objects.get(userUUID=userUUID)
        userIndex = userIndexObject.userIndex
        imgBinaryObject = request.FILES['file']
        imgFilename = imgBinaryObject.name
        imgName = imgFilename.rsplit('.', 1)[0]
        imgTypeObject = ImgType.objects.get(imgTypeName=imgFilename.rsplit('.', 1)[1])
        imgIndex = str(int(round(time.time() * 1000000)))
        imgUUID = uuid.uuid3(uuid.NAMESPACE_URL, imgIndex + imgName).hex
        imgUploadDate = time.strftime('%Y-%m-%d', time.localtime())
        year, month, date = imgUploadDate.split('-')

        ImgIndex.objects.create(imgIndex=imgIndex, imgName=imgName, imgType=imgTypeObject,
                                imgUploadDate=imgUploadDate, imgUUID=imgUUID, userIndex=userIndexObject)

        fileURL = StaticPath + f'/{userIndex}'
        if not os.path.exists(fileURL):
            os.mkdir(fileURL)
        fileURL = fileURL + f'/{year}'
        if not os.path.exists(fileURL):
            os.mkdir(fileURL)
        fileURL = fileURL + f'/{month}'
        if not os.path.exists(fileURL):
            os.mkdir(fileURL)
        fileURL = fileURL + f'/{date}'
        fileThumbURL = fileURL + '/thumbs'
        if not os.path.exists(fileURL):
            os.mkdir(fileURL)
        fileURL = fileURL + f'/{imgUUID}.{imgTypeObject.imgTypeName}'
        with open(fileURL, 'wb+') as f:
            for chunk in imgBinaryObject.chunks():
                f.write(chunk)

        if not os.path.exists(fileThumbURL):
            os.mkdir(fileThumbURL)

        image = Image.open(fileURL)
        width, height = image.size
        if width > 150:
            ratio = 240 / width
            new_height = int(height * ratio)
            image.thumbnail((240, new_height))
        image.save(fileThumbURL + f'/{imgUUID}.{imgTypeObject.imgTypeName}')

        return HttpResponse(dumps({
            'message': 'success',
            'imgUUID': imgUUID,
            'imgFilename': imgFilename
        }), content_type='application/json')
    else:
        return BadRequestMethodResponse()


def deleteImgFile(request):
    if request.method == 'DELETE':
        imgUUID = request.GET.get('imgUUID', '')
        userUUID = RsaDecrypt(request.GET.get('userUUID', ''))
        userIndex = UserIndex.objects.get(userUUID=userUUID).userIndex
        try:
            imgIndexObject = ImgIndex.objects.get(imgUUID=imgUUID)
        except ObjectDoesNotExist:
            return NotFoundResponse(dumps({
                'message': 'Fail to get picture file!'
            }))

        try:
            userIndexObject = UserIndex.objects.get(userUUID=userUUID)
        except ObjectDoesNotExist:
            return BadResponse(dumps({
                'message': 'user UUID does not match!'
            }))

        if imgIndexObject.userIndex.userIndex != userIndexObject.userIndex:
            return BadResponse(dumps({'message': 'user UUID does not match'}))
        else:
            year, month, day = str(imgIndexObject.imgUploadDate).split('-')
            imgTypeName = imgIndexObject.imgType.imgTypeName
            imgIndexObject.delete()
            os.remove(StaticPath+f'/{userIndex}/{year}/{month}/{day}/{imgUUID}.{imgTypeName}')
            os.remove(StaticPath+f'/{userIndex}/{year}/{month}/{day}/thumbs/{imgUUID}.{imgTypeName}')
            return HttpResponse(dumps({'message': 'delete success'}), content_type='application/json')
    else:
        return BadRequestMethodResponse()
