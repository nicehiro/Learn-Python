#!/usr/bin/python


import lxml.etree
import requests
import pandas as pd
from pandas import DataFrame, Series


def parse_html():
    url = 'http://example.webscraping.com/places/default/view/Afghanistan-1'
    r = requests.get(url)

    tree = lxml.etree.HTML(r.text)
    l = tree.xpath('body//td[@class="w2p_fw"]')
    datas = []

    for item in l:
        if item.text is None:
            if item.xpath('a/@href'):
                datas.append(item.xpath('a/@href')[0])
            elif item.xpath('img/@src'):
                datas.append(item.xpath('img/@src')[0])
            else:
                datas.append('')
        else:
            datas.append(item.text)

    return datas


def parse_df(lst):
    indexs = ['National Flag', 'Area', 'Population', 'Iso', 'Country',
              'Capital', 'Continent', 'Tld', 'Currency Code',
              'Currency Name', 'Phone', 'Postal Code Format',
              'Postal Code Regex', 'Languages', 'Neighbours']
    lst2 = []
    lst2.append(lst)
    df = DataFrame(lst2, columns=indexs)
    df = df.set_index('Country')
    return df


def save_csv(df):
    df.to_csv('out.csv')


if __name__ == '__main__':
    datas = parse_html()
    df = parse_df(datas)
    save_csv(df)
