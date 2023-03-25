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


def getImgInfoListPageCount(request) -> HttpResponse:
    """
    This view is used to get image data pages' number.\n
    The full api is "api/image/page?userUUID=<userUUID>".\n
    The param is:
        userUUID: string, user uuid, MUST be RSA encrypted.
    The requesting method MUST be GET, any other methods are forbidden.\n

    Args:
        request: The default param of django view functon.

    Returns:
        HttpResponse, Content-Type='application/json'.
            The key-value is:
                pageCount: int, number of data page. 0 when no image stored.
            If requesting method is unaccepted, it will return a BadRequestMethodResponse,
                see details in its docstring.
    """
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
    This view function is used to get pictures' info of one user in certain data page.\n
    The full api is "api/image/images?userUUID=<userUUID>&page=<page>".\n
    The params are:
        userUUID: user uuid, MUST be RSA encrypted.\n
        page: data page number.
    The requesting method MUST be GET, any other methods are forbidden.\n

    Args:
        request: The default param of django view functon.

    Returns:
        HttpResponse, Content-Type="application/json".
            It MUST be a json array containing image details, for each element in the array,
                it MUST be a json object with three key-values.
                imgUUID: string, the uuid of image.
                imgFilename: string, the filename of image, with suffix.
                imgUploadDate: string, the upload date of image, in form of "YYYY-MM-DD".
            If no image is stored, return an empty array.
            If requesting method is unaccepted, it will return a BadRequestMethodResponse,
                see details in its docstring.
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


def getImgBinaryByImgUUID(request, imgUUID: str) -> HttpResponse:
    """
    This view is used to get image file for direct link.
    The full api is "api/r/<imgUUID>"\n
    The param is:
        imgUUID: string, image uuid.\n
    Be advised that there is no authentication when requesting.\n
    The requesting method MUST be GET, any other methods are forbidden.\n

    Args:
        request: The default param of django view functon.
        imgUUID: string, image uuid.

    Returns:
        HttpResponse, Content-Type="image/<type>".
            It will return the image as an image element, which could be used for direct link.
            If failed, return a json object with error message.
            If requesting method is unaccepted, it will return a BadRequestMethodResponse,
                see details in its docstring.
    """
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


def getImgThumbByImgUUID(request, imgUUID: str) -> HttpResponse:
    """
    This view is used to get image thumbs file for direct link.\n
    The full api is "api/img/thumb/<imgUUID>".\n
    The param is:
        imgUUID: string, image uuid.
    Be advised that there is no authentication when requesting.\n
    The requesting method MUST be GET, any other methods are forbidden.\n

    Args:
        request: The default param of django view functon.
        imgUUID: string, image uuid.

    Returns:
        HttpResponse, Content-Type="application/json".
            It will return the image thumb as an image element, which could be used for direct link.
            If failed, return a json object with error message.
            If requesting method is unaccepted, it will return a BadRequestMethodResponse,
                see details in its docstring.
    """
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


def downloadImgFileByImgUUID(request, imgUUID: str) -> FileResponse | HttpResponse:
    """
    This view is used to download image file.\n
    The full api is "api/d/<imgUUID>".\n
    The param is:
        imgUUID: string, image uuid.
    Be advised that there is no authentication when requesting.\n
    The requesting method MUST be GET, any other methods are forbidden.\n

    Args:
        request: The default param of django view functon.
        imgUUID: string, image uuid.

    Returns:
        FileResponse if success, HttpResponse otherwise.
            The FileResponse contains the binary file of image. Filename attached.
            The HttpResponse contains error message, Content-Type="application/json".
            If requesting method is unaccepted, it will return a BadRequestMethodResponse,
                see details in its docstring.
    """
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
    """
    This view is used to upload image file.\n
    The full api is "api/image/upload".\n
    The requesting method MUST be POST, any other methods are forbidden.\n
    The Content-Type MUST be "application/form-data"
    The params are:
        userUUID: string, user uuid, MUST be RSA encrypted.
        file: binary, image binary file.

    Args:
        request: The default param of django view functon.

    Returns:
        HttpResponse, Content-Type="application/json".
            It contains a json object, the key-values are:
                message: string, "success".
                imgUUID: string, image's uploaded.
                imgFilename: string, image filename.
            If requesting method is unaccepted, it will return a BadRequestMethodResponse,
                see details in its docstring.

    Notes:
        The image uuid and upload date are auto generated. Since the uuid are
        generated based on time stamp,  the concurrent request capacity SHOULD
        be taken into consideration. Use nginx or other high concurrent capability
        web serve to ensure it work right.
    """
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


def deleteImgFile(request) -> HttpResponse:
    """
    The view is used to delete image.\n
    The full api is "api/img/delete?imgUUID=<imgUUID>&userUUID=<userUUID>"\n
    The params are:
        imgUUID: string, image uuid.\n
        userUUID: string, user uuid, MUST be RSA encrypted.
    The requesting method MUST be DELETE, any other methods are forbidden.\n

    Args:
        request: The default param of django view functon.

    Returns:
        HttpResponse, Content-Type="application/json"
            Contain the success message when success, error message otherwise.
            If requesting method is unaccepted, it will return a BadRequestMethodResponse,
                see details in its docstring.
    """
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
            os.remove(StaticPath + f'/{userIndex}/{year}/{month}/{day}/{imgUUID}.{imgTypeName}')
            os.remove(StaticPath + f'/{userIndex}/{year}/{month}/{day}/thumbs/{imgUUID}.{imgTypeName}')
            return HttpResponse(dumps({'message': 'delete success'}), content_type='application/json')
    else:
        return BadRequestMethodResponse()
