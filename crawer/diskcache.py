#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author: hiro
# Learn from ‘用 Python 写网络爬虫’
# Python 3.6
# 使用 requests 库


import os
import re
from urllib import parse
import shutil
import zlib
from datetime import datetime, timedelta
from stronger_crawer import link_crawler
import pickle


class DiskCache:
    '''
    compress: 是否需要压缩
    '''

    def __init__(self, cache_dir='cache', expires=timedelta(days=30),
                 compress=True):
        self.cache_dir = cache_dir
        self.expires = expires
        self.compress = compress

    '''
    将 url 转为 path
    '''

    def url_to_path(self, url):
        components = parse.urlsplit(url)
        path = components.path
        if not path:
            path = '/index.html'
        elif path.endswith('/'):
            path += 'index.html'

        filename = components.netloc + path + components.query
        filename = re.sub('[^/0-9a-zA-Z\-.,;_]', '_', filename)

        # 保证每级目录名不会超过 255 个字符
        filename = '/'.join(segment[:255] for segment in filename.split('/'))
        print(filename)
        return os.path.join(self.cache_dir, filename)

    def has_expired(self, timestamp):
        return datetime.utcnow() > timestamp + self.expires

    '''
    清除缓存
    '''

    def clear(self):
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)

    '''
    Python 内置的魔法方法
    可以将此类的实例对象当作 dict 来用
    '''

    def __setitem__(self, url, result):
        path = self.url_to_path(url)
        folder = os.path.dirname(path)

        if not os.path.exists(folder):
            os.makedirs(folder)

        # 序列化对象
        data = pickle.dumps((result, datetime.utcnow()))
        if self.compress:
            data = zlib.compress(data)
        with open(path, 'wb') as fp:
            fp.write(data)

    def __getitem__(self, url):
        path = self.url_to_path(url)
        if os.path.exists(path):
            with open(path, 'rb') as fp:
                data = fp.read()
                if self.compress:
                    data = zlib.decompress(data)

                result, timestamp = pickle.loads(data)
                if self.has_expired(timestamp):
                    raise KeyError(url + ' has expired')
                return result
        else:
            raise KeyError(url + ' dose not exist')

    def __delitem__(self, url):
        path = self._key_path(url)
        try:
            os.remove(path)
            os.removedirs(os.path.dirname(path))
        except OSError:
            pass


if __name__ == '__main__':
    link_crawler('http://example.webscraping.com', '.*/(index|view)/.*',
                 delay=0, max_urls=10, cache=DiskCache())
