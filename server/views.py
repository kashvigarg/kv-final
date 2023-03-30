from rest_framework.response import Response
import rest_framework.status as status
from rest_framework import generics
import pandas as pd
from django.core.files.storage import FileSystemStorage
import seaborn as sns
from pyod.models.iforest import IForest
from rest_framework.parsers import MultiPartParser, FormParser
from datetime import timedelta 
from server.serializers import UploadSerializer
from server.models import File

class UploadCSV(generics.CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = UploadSerializer

    def post(self, request, *args, **kwargs): 
        serializer = UploadSerializer(data=request.data)
        #serializer.is_valid(raise_exception=True)
        
        if serializer.is_valid():
            
            file = serializer.validated_data['file']
            fs = FileSystemStorage()
            file2 = fs.save(file.name, file)
            fileurl = fs.url(file2)
            url = "."+fileurl
            df = pd.read_csv(url, delimiter=';', low_memory=False)
            df = df[['trans_id', 'date', 'account_id', 'type', 'amount']]
            df['date'] = pd.to_datetime(df['date'], format='%y%m%d')
            df.replace(to_replace='PRIJEM', value = 'Credit', inplace= True)
            df.replace(to_replace='VYDAJ', value = 'Withdrawl', inplace= True)
            df_W = df.query('type == "Withdrawl"')
            df_C = df.query('type == "Credit"')
            df_W = df_W.sort_values(by=['account_id', 'date']).set_index('date')
            df_C = df_C.sort_values(by=['account_id', 'date']).set_index('date')
            df_W['sum_5days'] = df_W.groupby('account_id')['amount'].transform(lambda s: s.rolling(timedelta(days=5)).sum())
            df_W['freq_5days'] = df_W.groupby('account_id')['amount'].transform(lambda s: s.rolling(timedelta(days=5)).count())


            # sns.displot(df_W['sum_5days'], bins=50)
            # sns.countplot(x='freq_5days', data=df_W)

            model = IForest(contamination= 0.001)
            X = df_W[['freq_5days', 'sum_5days']]
            model.fit(X)

            df_W['pred'] = model.labels_
            df_W['score'] = model.decision_scores_
            
            flagged = df_W.query('pred == 1')
            f_flagged = flagged[['trans_id', 'pred', 'score']]
            jsrec = f_flagged.to_json(orient ='records')
            context = {
             'data': jsrec,
            }
            
            fs.delete(file2)
            return Response(context, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)