#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author: hiro
# Learn from ‘用 Python 写网络爬虫’
# Python 3.6
# 使用 requests 库


import time
import threading
from urllib import parse
from downloader import Downloader


SLEEP_TIME = 1
DEFAULT_AGENT = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                 '(KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
proxies = {
    'https': 'socks5://127.0.0.1:1080',
    'http': 'socks5://127.0.0.1:1080'
}


def thread_crawler(seed_url, delay=5, cache=None, scrape_callback=None,
                   user_agent=DEFAULT_AGENT, proxies=None, num_retries=1,
                   max_threads=10, timeout=60):
    crawl_queue = [seed_url]
    seen = set([seed_url])
    D = Downloader(delay=delay, user_agent=user_agent, proxies=proxies,
                   num_retries=num_retries, timeout=timeout, cache=cache)

    def process_queue():
        while True:
            try:
                url = crawl_queue.pop()
            except IndexError:
                break
            else:
                html = D(url)
                if scrape_callback:
                    try:
                        links = scrape_callback(url, html) or []
                    except Exception as e:
                        print('Error in callback for: {} : {}'.format(url, e))
                    else:
                        for link in links:
                            link = normalize(seed_url, link)
                            if link not in seen:
                                seen.add(link)
                                crawl_queue.append(link)

    threads = []
    while threads or crawl_queue:
        for thread in threads:
            if not thread.is_alive():
                print('a thread is dead...................')
                threads.remove(thread)
        while len(threads) < max_threads and crawl_queue:
            thread = threading.Thread(target=process_queue)
            # 一个线程结束后可以停止
            thread.setDaemon(True)
            thread.start()
            print('a thread is start......................')
            threads.append(thread)

        time.sleep(SLEEP_TIME)


def normalize(seed_url, link):
    link, _ = parse.urldefrag(link)
    return parse.urljoin(seed_url, link)
