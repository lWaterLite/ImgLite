from image.models import ImgIndex

from django.core.paginator import Paginator

imgIndexObjectList = ImgIndex.objects.filter(userIndex='1327654').order_by('imgUUID')
imgIndexObjectListPage = imgIndexObjectList.count() // 12 + 1
pageObject = Paginator(imgIndexObjectList, 15)
print(pageObject.get_page(1).object_list)
