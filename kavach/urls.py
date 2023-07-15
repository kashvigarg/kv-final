from django.contrib import admin
from django.urls import path, include
from server import views
import server
from server import views

urlpatterns = [
    path('', views.UploadCSV.as_view(), name = 'upload-csv'),
]
