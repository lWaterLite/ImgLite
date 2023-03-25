"""ImgLite_Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from authentication.views import get_csrf_token
from image.views import getImgBinaryByImgUUID, downloadImgFileByImgUUID

urlpatternsSub = [
    path('image/', include('image.urls')),
    path('auth/', include('authentication.urls')),
    path('state/', include('statement.urls')),
    path('token', get_csrf_token),
    path('r/<str:imgUUID>', getImgBinaryByImgUUID),
    path('d/<str:imgUUID>', downloadImgFileByImgUUID)
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(urlpatternsSub))
]
