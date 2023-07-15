import pandas as pd
from pyod.models.iforest import IForest
from datetime import timedelta 

def get_fraud_analysis(df):
    
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
    js_reponse = f_flagged.to_json(orient ='records')

    return js_reponse