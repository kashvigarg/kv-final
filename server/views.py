from rest_framework.decorators import parser_classes
from django.core.files.storage import default_storage
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.http import HttpResponse
import io, csv, pandas as pd
import seaborn as sns
import numpy as np
from pyod.models.iforest import IForest
from sklearn.ensemble import IsolationForest
from datetime import datetime, timedelta 
from django.shortcuts import render
from server.models import File
from rest_framework.renderers import JSONRenderer
from server.serializers import UploadSerializer
from . import serializers

class UploadCSV(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs): 
        serializer = UploadSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            file = serializer.data
            df = pd.read_csv(file, delimiter=';')
            df = df[['date', 'account_id', 'type', 'amount']]
            df['date'] = pd.to_datetime(df['date'], format='%y%m%d')
            df.replace(to_replace='PRIJEM', value = 'Credit', inplace= True)
            df.replace(to_replace='VYDAJ', value = 'Withdrawl', inplace= True)
            df_W = df.query('type == "Withdrawl"')
            df_C = df.query('type == "Credit"')
            df_W = df_W.sort_values(by=['account_id', 'date']).set_index('date')
            df_C = df_C.sort_values(by=['account_id', 'date']).set_index('date')
            delta = timedelta(days = 5)
            df_W['sum_5days'] = df_W.groupby('account_id')['amount'].transform(lambda s: s.rolling(timedelta(days=5)).sum())
            df_W['freq_5days'] = df_W.groupby('account_id')['amount'].transform(lambda s: s.rolling(timedelta(days=5)).count())


            sns.displot(df_W['sum_5days'], bins=50)
            sns.countplot(x='freq_5days', data=df_W)

            model = IForest(contamination= 0.001)
            X = df_W[['freq_5days', 'sum_5days']]
            model.fit(X)

            df_W['pred'] = model.labels_
            df_W['score'] = model.decision_scores_
            
            flagged = df_W.query('pred == 1')
            jsrec = flagged.reset_index().to_json(orient ='records')
            arr = []
            arr = json.loads(jsrec)
            
            return Response(arr, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)