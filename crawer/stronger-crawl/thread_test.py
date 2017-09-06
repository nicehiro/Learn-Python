#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author: hiro
# Learn from ‘用 Python 写网络爬虫’
# Python 3.6
# 使用 requests 库


from thread_crawler import thread_crawler
from mongo_cache import MongoCache
from alexaCallback import AlexaCallback
from call_back import ScrapeCallback


def main(max_threads):
    scrape_callback = ScrapeCallback()
    thread_crawler(scrape_callback.seed_url, scrape_callback=scrape_callback,
                   cache=None, max_threads=max_threads, timeout=10)


if __name__ == '__main__':
    main(5)
