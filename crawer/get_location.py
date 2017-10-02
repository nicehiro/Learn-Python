#!/usr/bin/python

import pandas as pd
from pandas import DataFrame, Series

import wikipedia


def get_name():
    df = pd.read_excel('/home/hiro/genre.xls')
    lst = df['national'].tolist()
    return df, lst


def get_locations():
    df, nationals = get_name()
    lats = []
    lons = []

    for nation in nationals:
        n = wikipedia.page(nation)
        lat, lon = n.coordinates
        lats.append(lat)
        lons.append(lon)
        print(lat, lon)

    df['lats'] = lats
    df['lons'] = lons
    df.to_excel('/home/hiro/test.xls')


get_locations()
