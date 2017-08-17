#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author: hiro
# Learn from ‘用 Python 写网络爬虫’
# Python 3.6
# 使用 requests 库


from stronger_crawer import link_crawler
from mongo_cache import MongoCache
from alexaCallback import AlexaCallback


if __name__ == '__main__':
    scrape_callback = AlexaCallback()
    cache = MongoCache()
    link_crawler(scrape_callback.seed_url, max_urls=100,
                 scrape_callback=scrape_callback, cache=cache,
                 ignore_robot=True)
