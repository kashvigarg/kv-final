from django.urls import path
from . import views

urlpatterns = [
     path('upload/', views.UploadCSV.as_view(), name = 'upload-csv'),
]
