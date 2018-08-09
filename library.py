import requests
import pandas as pd
from bs4 import BeautifulSoup as bs


def market_table():
    page=requests.get('https://coinmarketcap.com/all/views/all/')

    soup=bs(page.content,'html.parser')
    table = soup.find("table",{"id":'currencies-all'})

    title=[th.text for th in table.find("thead").find_all("th")]
    title.pop(0) # remove index position
    title.pop() # remove more column from title list

    body=[]
    for tr in table.find("tbody").find_all("tr"):

        td_list=tr.find_all("td")

        row=[]
        row.append(td_list[1].find("a",{"class":"currency-name-container link-secondary"}).text) # name
        row.append(td_list[2].text) # symbol
        row.append(float(td_list[3]['data-sort'])) # market cap
        row.append(float(td_list[4]['data-sort'])) # price
        row.append(float(td_list[5]['data-sort'])) # circulating supply
        row.append(float(td_list[6]['data-sort'])) # volume 24
        row.append(float(td_list[7]['data-sort'])) # % 1h
        row.append(float(td_list[8]['data-sort'])) # % 24h
        row.append(float(td_list[9]['data-sort'])) # % 7d

        body.append(row)

    df=pd.DataFrame(body)

    df.columns=title

    return df


def get_tags(name='bitcoin'):
    page = requests.get('https://coinmarketcap.com/currencies/{}/'.format(name))

    soup = bs(page.content, 'html.parser')
    li = soup.find_all("ul", {"class": 'list-unstyled details-panel-item--links'})[0] # last element is the tag list
    tag_list = [tag.text.lower() for tag in li.find_all("span")]


    return {"is_coin": "coin" in tag_list, "is_mineable": "mineable" in tag_list}
