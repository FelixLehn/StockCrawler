from flask import Flask
from flask_cors import CORS
import pandas as pd 
import re
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

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

@app.route('/stocks')
def stock_compiler():
    stock_data = pd.read_html(
        "https://www.finanznachrichten.de/nachrichten/alle-empfehlungen.html")

    stock_data_first=text_transform(stock_data)
    
    best_five = stock_data_first.iloc[:5]

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
        filtered_data=filtered_data.set_index(filtered_data['Unternehmen']).iloc[2]
        stock_data_onvista=stock_data_onvista.append(filtered_data) 
    stock_data_onvista=stock_data_onvista.set_index([pd.Index([1, 2, 3, 4, 5])])
    return stock_data_onvista.to_json(orient='records')
