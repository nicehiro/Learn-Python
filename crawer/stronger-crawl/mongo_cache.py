#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author: hiro
# Learn from ‘用 Python 写网络爬虫’
# Python 3.6
# 使用 requests 库


import pickle
import zlib
from datetime import datetime, timedelta
from pymongo import MongoClient
from bson.binary import Binary
from stronger_crawer import link_crawler


class MongoCache:
    def __init__(self, client=None, expires=timedelta(days=30)):
        self.client = MongoClient(
            'localhost', 27017) if client is None else client
        # 获得一个 database 实例
        self.db = self.client.cache
        # webpage 为获得的一个 collection
        # 使用 timestamp 为索引
        self.db.webpage.create_index(
            'timestamp', expireAfterSeconds=expires.total_seconds())

    def clear(self):
        self.db.webpage.drop()

    def __setitem__(self, url, result):
        record = {'result': Binary(zlib.compress(pickle.dumps(result))),
                  'timestamp': datetime.utcnow()}
        self.db.webpage.update({'_id': url}, {'$set': record}, upsert=True)

    def __getitem__(self, url):
        record = self.db.webpage.find_one({'_id': url})
        if record:
            return pickle.loads(zlib.decompress(record['result']))
        else:
            raise KeyError(url + ' dose not exist')

    def __contains__(self, url):
        '''
        是否包含此 url
        其实调用了 __getitem__ 方法
        '''
        try:
            self[url]
        except KeyError:
            return False
        else:
            return True


if __name__ == '__main__':
    url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'
    url2 = 'http://example.webscraping.com'
    link_crawler(url2,
                 delay=0, max_urls=10, cache=MongoCache(), ignore_robot=True)
    # MongoCache().clear()
