import json
import fraud_analysis as algo
from rest_framework.response import Response
import rest_framework.status as status
from rest_framework import generics
import pandas as pd
from django.core.files.storage import FileSystemStorage
from rest_framework.parsers import MultiPartParser, FormParser
from server.serializers import UploadSerializer

class UploadCSV(generics.CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = UploadSerializer

    def post(self, request, *args, **kwargs): 
        serializer = UploadSerializer(data=request.data)
        
        if serializer.is_valid():
            
            file = serializer.validated_data['file']
            fs = FileSystemStorage()

            file_instance = fs.save(file.name, file)
            fileurl = fs.url(file_instance)
            url = "." + fileurl

            df = pd.read_csv(url, delimiter=';', low_memory=False)

            js_response = algo.get_fraud_analysis(df=df)
            p = json.loads(js_response)

            context = {
             'data': p,
            }
            
            fs.delete(file_instance)

            return Response(context, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)