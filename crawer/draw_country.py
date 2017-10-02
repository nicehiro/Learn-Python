#!/usr/bin/python


import pandas as pd
from pandas import DataFrame, Series

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

import numpy as np


def get_locations():
    file_path = '/home/hiro/genre.xls'
    df = pd.read_excel(file_path, encoding='gb2312')
    lats = df.lats.tolist()
    lons = df.lons.tolist()
    names = df.name.tolist()


    lllat = df.lats.min()
    urlat = df.lats.max()
    lllon = df.lons.min()
    urlon = df.lons.max()

    bmap = Basemap(projection='ortho',
                  lon_0=-40,
                  lat_0=35,
                  resolution='l')
    
    bmap.drawcoastlines()
    bmap.drawstates()
    bmap.drawcountries()
    bmap.fillcontinents(color='#BF9E30',lake_color='#689CD2',zorder=0)
    bmap.drawmeridians(np.arange(0,360,30))
    bmap.drawparallels(np.arange(-90,90,30))
    return df, bmap, lats, lons, names


def draw():
    df, bmap, lats, lons, names = get_locations()
    x, y = bmap(lons, lats)
    y_offset = 35
    x_offset = 35
    rotation = 20

    for i, j, name in zip(x, y, names):
        size = 80
        bmap.scatter(i, j, s=size, marker='o', color='#FF0000')
        plt.text(i+x_offset,j+y_offset,name,rotation=rotation,fontsize=10, color='#9400D3')

    plt.show()

plt.title('The Distribution of Musicians about Hiro\'s Favorite', fontsize=20)

draw()
