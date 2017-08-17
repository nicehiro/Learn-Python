#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author: hiro
# Learn from ‘用 Python 写网络爬虫’
# Python 3.6
# 使用 requests 库


import csv
from io import BytesIO, StringIO
from zipfile import ZipFile
from mongo_cache import MongoCache


class AlexaCallback:
    def __init__(self, max_urls=1000):
        self.max_urls = max_urls
        self.filename = '/home/hiro/Downloads/top-1m.csv.zip'
        self.seed_url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'

    def __call__(self, url, html):
        if url == self.seed_url:
            urls = []
            cache = MongoCache()
            with ZipFile(BytesIO(html.content)) as zf:
                csv_filename = zf.namelist()[0]
                data = StringIO(zf.open(csv_filename).read().decode('utf-8'))
                for _, website in csv.reader(data):
                    if 'http://' + website not in cache:
                        urls.append('http://' + website)
                        if len(urls) == self.max_urls:
                            break
            return urls
