from rest_framework.decorators import parser_classes
from django.core.files.storage import default_storage
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
import io, csv, pandas as pd
from django.shortcuts import render
from server.models import File
from . import serializers

class UploadCSV(generics.CreateAPIView):
    serializer_class = serializers.UploadSerializer

    def post(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.FILES)
        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data['file']
        
        result = [0,0,0]
        return Response(result)