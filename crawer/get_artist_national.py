#!/usr/bin/python

import requests
from lxml import etree
import pandas as pd
from pandas import DataFrame, Series

import wikipedia
from wikipedia.exceptions import PageError


def get_name():
    file_path = '/home/hiro/genre.xls'
    df = pd.read_excel(file_path)
    lst = df.name.tolist()
    return df, lst

def parser(name):
    try:
        wk = wikipedia.page(name)
    except PageError:
        print('No Page found')
        return '0'
    text = wk.html()
    html = etree.HTML(text)
    result = html.xpath('//tr/th[@scope="row"]')

    s = '0'

    for i in result:
        if i.text == 'Born':
            a = i.xpath('../td')
            s = a[0].xpath('string(.)')
            break
        elif i.text == 'Origin':
            a = i.xpath('../td')
            s = a[0].xpath('string(.)')
            break

    s = s.replace('\n', '')
    print(name, s)
            
    return s 

def parse_form():
    df, names = get_name()
    nationals = []
    
    for name in names:
        if name == 'Lycaon':
            nationals.append('0')
            continue
        temp = parser(name)
        if temp == None:
            temp = '0'
        nationals.append(temp)

    df['national'] = nationals
    df.to_csv('/home/hiro/nations.csv')


parse_form()
