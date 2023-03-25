from rsa import DecryptionError
from pandas import DataFrame
from django.http import FileResponse, HttpResponse
from os import remove

from utils.Response import BadRequestMethodResponse, BadUUIDResponse
from utils.Encryption import RsaDecrypt
from .models import ImgIndex, UserIndex
from utils.Config import RawUrlPrefix
from ImgLite_Django.settings import BASE_DIR


def getStatementInCsvByUserUUID(request) -> FileResponse | HttpResponse:
    """
    This view is used to get csv file of image statement.\n
    The full api is "api/state/csv?userUUID=<userUUID>".\n
    The param is:
        userUUID: string, user uuid, MUST be RSA encrypted.\n
    The requesting method MUST be GET, any other methods are forbidden.\n

    Args:
        request: The default param of django view functon.

    Returns:
        FileResponse if success, HttpResponse otherwise.
            The FileResponse contains the csv file of image statement.
            The HttpResponse contains error message, Content-Type="application/json".
            If requesting method is unaccepted, it will return a BadRequestMethodResponse,
                see details in its docstring.

    See Also:
        getStatementInExcelByUserUUID: get Excel file of image statement.
    """
    if request.method == 'GET':
        try:
            userUUID = RsaDecrypt(request.GET.get('userUUID', ''))
        except DecryptionError:
            return BadUUIDResponse()

        userIndex = UserIndex.objects.get(userUUID=userUUID).userIndex
        imgIndexObjectList = ImgIndex.objects.filter(userIndex=userIndex)
        if imgIndexObjectList.exists():
            imgDataList = []
            for imgIndexObject in imgIndexObjectList:
                imgData = [imgIndexObject.imgName + "." + imgIndexObject.imgType.imgTypeName,
                           str(imgIndexObject.imgUploadDate), RawUrlPrefix + imgIndexObject.imgUUID]
                imgDataList.append(imgData)
            cacheCsvFilePath = BASE_DIR.__str__() + f'/cache/{userUUID}.csv'
            DataFrame(imgDataList, columns=['文件名', '上传日期', '直链']).to_csv(cacheCsvFilePath, index=False, sep=' ')
            imgStateCsvFile = open(cacheCsvFilePath, 'rb')
            response = FileResponse(imgStateCsvFile)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = f'attachment;filename="image.csv"'
            remove(cacheCsvFilePath)
            return response
        else:
            cacheCsvFilePath = BASE_DIR + f'/cache/{userUUID}.csv'
            DataFrame({'文件名': [], '上传日期': [], '直链': []}).to_csv(cacheCsvFilePath, index=False, sep=' ')
            imgStateCsvFile = open(cacheCsvFilePath, 'rb')
            response = FileResponse(imgStateCsvFile)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = f'attachment;filename="image.csv"'
            remove(cacheCsvFilePath)
            return response
    else:
        return BadRequestMethodResponse()


def getStatementInExcelByUserUUID(request):
    """
    This view is used to get Excel file of image statement.\n
    The full api is "api/state/excel?userUUID=<userUUID>".\n
    The param is:
        userUUID: string, user uuid, MUST be RSA encrypted.\n
    The requesting method MUST be GET, any other methods are forbidden.\n

    Args:
        request: The default param of django view functon.

    Returns:
        FileResponse if success, HttpResponse otherwise.
            The FileResponse contains the csv file of image statement.
            The HttpResponse contains error message, Content-Type="application/json".
            If requesting method is unaccepted, it will return a BadRequestMethodResponse,
                see details in its docstring.

    See Also:
        getStatementInCsvByUserUUID: get csv file of image statement.
    """
    if request.method == 'GET':
        try:
            userUUID = RsaDecrypt(request.GET.get('userUUID', ''))
        except DecryptionError:
            return BadUUIDResponse()

        userIndex = UserIndex.objects.get(userUUID=userUUID).userIndex
        imgIndexObjectList = ImgIndex.objects.filter(userIndex=userIndex)
        if imgIndexObjectList.exists():
            imgDataList = []
            for imgIndexObject in imgIndexObjectList:
                imgData = [imgIndexObject.imgName + "." + imgIndexObject.imgType.imgTypeName,
                           str(imgIndexObject.imgUploadDate), RawUrlPrefix + imgIndexObject.imgUUID]
                imgDataList.append(imgData)
            cacheExcelFilePath = BASE_DIR.__str__() + f'/cache/{userUUID}.xlsx'
            DataFrame(imgDataList, columns=['文件名', '上传日期', '直链']).to_excel(cacheExcelFilePath, index=False)
            imgStateExcelFile = open(cacheExcelFilePath, 'rb')
            response = FileResponse(imgStateExcelFile)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = f'attachment;filename="image.xlsx"'
            return response
    else:
        return BadRequestMethodResponse()
