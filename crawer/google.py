#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author: hiro
# Learn from ‘用 Python 写网络爬虫’
# Python 3.6
# 使用 requests 库


import sys
import urllib
import lxml.etree
from downloader import Downloader


search_url = 'https://www.google.com/search?q='


def search(keyword):
    D = Downloader()
    # quote_plus like quote, but also replace ' ' to '+'
    url = search_url + urllib.parse.quote_plus(keyword)
    print(url)
    html = D(url)
    tree = lxml.etree.HTML(html.text)
    links = []
    for result in tree.xpath('//h3[@class="r"]/a'):
        link = result.get('href')
        # query string parsing
        # print(urllib.parse.urlparse(link))
        qs = urllib.parse.urlparse(link).query
        # print(qs)
        links.extend(urllib.parse.parse_qs(qs).get('q', []))
    return links


if __name__ == '__main__':
    try:
        keyword = sys.argv[1]
    except IndexError:
        keyword = 'hello'
    print(search(keyword))
