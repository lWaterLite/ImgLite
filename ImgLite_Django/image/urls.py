from django.urls import path
from . import views

urlpatterns = [
    path('images', views.getImgInfoListByUserUUID),
    path('upload', views.uploadImgFile),
    path('thumb/<str:imgUUID>', views.getImgThumbByImgUUID),
    path('delete', views.deleteImgFile),
    path('page', views.getImgInfoListPageCount)
]
