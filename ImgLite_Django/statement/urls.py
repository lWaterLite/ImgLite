from django.urls import path
from . import views

urlpatterns = [
    path('csv', views.getStatementInCsvByUserUUID),
    path('excel', views.getStatementInExcelByUserUUID)
]