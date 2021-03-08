from flask import Flask,Blueprint,request,Response,stream_with_context
from flask_cors import CORS
import pandas as pd 
import numpy as np
import re
import requests
from bs4 import BeautifulSoup
import json 

app = Flask(__name__)
CORS(app)
api = Blueprint('api', __name__)

def text_transform(stock_data):
    stock_data_first = pd.DataFrame(stock_data[1])
    stock_data_first['Aktuelle Nachrichten'] = stock_data_first['Aktuelle Nachrichten'].str.findall(
        '(?:stuft|belässt)\s([A-Za-z]+)').transform(''.join)
    stock_data_first['Potential in %'] = stock_data_first['PotentialKurse aktuell'].str.findall(
        '([+-]\d*)\s%').transform(''.join).apply(pd.to_numeric)
    stock_data_first = stock_data_first.sort_values(
        by=['Potential in %'], ascending=False)
    return stock_data_first

def get_best_links(best_five):
    page = requests.get(
        "https://www.finanznachrichten.de/nachrichten/alle-empfehlungen.html")
    soup = BeautifulSoup(page.content, "html.parser")

    tables_list = [x for x in soup.find_all("table", attrs={"class": "rel-ct"})]

    links = tables_list[0].tbody.find_all('a')
    filtered_links = [x.get('href') for i, x in enumerate(links) if i % 2 == 0]

    best_five['links']=best_five['Aktuelle Nachrichten'].apply(lambda x: [y for y in filtered_links if x.lower() in y][0])
    return best_five

@api.route('/stocks',methods=['POST'])
def stock_compiler():
    data=request.get_json()
    def streamer(i):
        n=np.array(range(5)) if i==0 else np.array(range(5,10))
        stock_data = pd.read_html(
            "https://www.finanznachrichten.de/nachrichten/alle-empfehlungen.html")

        stock_data_first=text_transform(stock_data)
        
        best_five = stock_data_first.iloc[n]

        best_links=get_best_links(best_five)

        isins=[]
        for index,li in best_five.iterrows():
            page_2=requests.get(li['links'])
            soup_2=BeautifulSoup(page_2.content,"html.parser")
            span=soup_2.find('span',attrs={'class':"wkn-isin"})
            isins.append((span.find_all(id="produkt-isin")[0].get('data-isin'),li['links'],li['Potential in %'],li['Unternehmen / Aktien']))
        stock_data_onvista=pd.DataFrame([])
        for isin in isins:
            data=pd.read_html("https://www.onvista.de/aktien/fundamental/-Aktie-{}".format(isin[0]))
            filtered_data=data[1].rename(columns={data[1].columns[0]:"Stats"})
            filtered_data['Unternehmen']=isin[3]
            filtered_data['Potential_Analyse']=isin[2]
            filtered_data['isin']=isin[0]
            filtered_data=filtered_data.set_index(filtered_data['Unternehmen']).iloc[2]
            stock_data_onvista=stock_data_onvista.append(filtered_data) 
        stock_data_onvista=stock_data_onvista.set_index([pd.Index([1, 2, 3, 4, 5])])
        return stock_data_onvista.to_json(orient='records')
    return Response(streamer(data.get("number")))

@api.route('/chart',methods=['POST'])
def stock_chart():
    data=request.get_json()
    if data:
        isin=data.get('isin')
        s_re=requests.post('https://api.openfigi.com/v2/mapping',json=[{'idType': 'ID_ISIN','idValue':isin}])
        s_json=s_re.json()[0]
        s_data=s_json.get('data')[0]
        s_ma=requests.get('http://api.marketstack.com/v1/eod?access_key={}&symbols={}'.format('1cbb6d9efae20cc7607095632401ef24',s_data.get('ticker')))
        s_ma_data=json.dumps(s_ma.json().get('data'))
        
        df=pd.read_json(s_ma_data)
        df['date']=pd.to_datetime(df['date'])
        df['date_1']=df['date'].dt.strftime('%m/%d/%Y')
        return Response(df.to_json(orient='records'))

app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5050)