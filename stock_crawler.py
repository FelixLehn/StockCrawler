
import pandas as pd 

stock_data=pd.read_html("https://www.finanznachrichten.de/nachrichten/alle-empfehlungen.html")

import re

stock_data_first['Aktuelle Nachrichten']=stock_data_first['Aktuelle Nachrichten'].str.findall('(?:stuft|belässt)\s([A-Za-z]+)').transform(''.join)

stock_data_first['Potential in %']=stock_data_first['PotentialKurse aktuell'].str.findall('([+-]\d*)\s%').transform(''.join).apply(pd.to_numeric)

stock_data_first=stock_data_first.sort_values(by=['Potential in %'],ascending=False)

from bs4 import BeautifulSoup
import requests

page=requests.get("https://www.finanznachrichten.de/nachrichten/alle-empfehlungen.html")
soup=BeautifulSoup(page.content,"html.parser")

best_five=stock_data_first.iloc[:5]

tables_list=[x for x in soup.find_all("table",attrs={"class":"rel-ct"})]

links=tables_list[0].tbody.find_all('a')
filtered_links=[x.get('href') for i,x in enumerate(links) if i%2==0]

best_links=list(map(lambda x:list([(y,x) for y in filtered_links if x in y]),best_five['Aktuelle Nachrichten'].str.lower()))
best_links=list(map(lambda x: x[0],best_links))

isins=[]
for li in best_links:
    page_2=requests.get(li[0])
    soup_2=BeautifulSoup(page_2.content,"html.parser")
    span=soup_2.find('span',attrs={'class':"wkn-isin"})
    isins.append((span.find_all(id="produkt-isin")[0].get('data-isin'),*li))

stock_data_onvista=pd.DataFrame([])
for isin in isins:
    #page_3=requests.get("https://www.onvista.de/aktien/fundamental/-Aktie-{}".format(isin[0]))
    data=pd.read_html("https://www.onvista.de/aktien/fundamental/-Aktie-{}".format(isin[0]))
    filtered_data=data[1].rename(columns={data[1].columns[0]:"Stats"})
    filtered_data['Unternehmen']=isin[2]
    filtered_data=filtered_data.set_index(filtered_data['Unternehmen']).iloc[2]
    stock_data_onvista=stock_data_onvista.append(filtered_data) 



