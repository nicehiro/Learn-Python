#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author: hiro
# Learn from ‘用 Python 写网络爬虫’
# Python 3.6
# 使用 requests 库

import requests
import time
import datetime
from urllib import parse
import socket

DEFAULT_AGENT = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                 '(KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
DEFAULT_DELAY = 5
DEFAULT_RETRIES = 1
DEFAULT_TIMEOUT = 60

'''
socks5 代理设置
我使用本地的 socks5 来代理爬取一些需要翻墙的网站信息
'''
proxies = {
    'https': 'socks5://127.0.0.1:1080'
}


class Throttle:
    '''
    限速
    实际上就是延迟几秒钟请求
    '''

    def __init__(self, delay):
        self.delay = delay
        self.domains = {}

    def wait(self, url):
        domain = parse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - \
                (datetime.datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)

        self.domains[domain] = datetime.datetime.now()


class Downloader:
    '''
    将 download 封装，添加缓存功能
    '''

    def __init__(self, delay=DEFAULT_DELAY, user_agent=DEFAULT_AGENT,
                 proxies=None,
                 num_retries=DEFAULT_RETRIES, timeout=DEFAULT_TIMEOUT,
                 cache=None):
        socket.setdefaulttimeout(timeout)
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.cache = cache

    def download(self, url, headers, proxy, num_retries):
        print('Downloading......................')
        request = requests.get(url, headers or {}, proxies=proxy)
        print(request.status_code)
        return {'html': request, 'code': request.status_code}

    def __call__(self, url):
        print('call back........................')
        result = None
        '''
        如果此时已经有了缓存，先在缓存中查找此刻 url 的缓存内容
        '''
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                pass
            else:
                if self.num_retries > 0 and 500 <= result['code'] < 600:
                    result = None

        '''
        第一次为某个 url 设置缓存
        将缓存写到 cache 中
        '''
        if result is None:
            self.throttle.wait(url)
            # proxy = random.choice(self.proxies) if self.proxies else None
            proxy = self.proxies if self.proxies else None
            headers = {'user_agent': self.user_agent}
            result = self.download(url, headers, proxy,
                                   num_retries=self.num_retries)
            print('saving cache.....................')
            if self.cache:
                self.cache[url] = result
        return result['html']
