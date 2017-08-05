#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author: hiro
# Learn from ‘用 Python 写网络爬虫’
# Python 3.6
# 使用 requests 库


import requests
import re
import urllib.robotparser
from urllib import parse
import datetime
import time


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


# 从 Chrome 请求中复制的一段请求头，用来模拟浏览器请求
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'


'''
socks5 代理设置
我使用本地的 socks5 来代理爬取一些需要翻墙的网站信息
'''
proxies = {
    'https': 'socks5://127.0.0.1:1080'
}


# 实现下载功能
def download(url, agent=user_agent, proxy=None):
    print('Downloading: ', url)
    html = requests.get(url, proxies=proxy, timeout=5)
    print(html.status_code)
    return html


def link_crawler(seed_url, link_regex=None, headers=None, user_agent=user_agent, max_depth=2, delay=0, max_urls=-1):

    # 存放需要访问的 url
    crawl_queue = [seed_url]

    # 最多访问深度
    seen = {seed_url: 0}

    # 识别 robots.txt
    rp = get_robots(seed_url)

    # 延迟
    throttle = Throttle(delay)

    # 统计访问 url 次数
    num_urls = 0

    headers = headers or {}
    if user_agent:
        headers['User-agent'] = user_agent

    while crawl_queue:
        url = crawl_queue.pop()
        if rp.can_fetch(user_agent, url):
            throttle.wait(url)
            html = download(url, proxy=proxies)
            links = []

            depth = seen[url]
            if depth != max_depth:
                if link_regex:
                    links.extend(link for link in get_links(
                        html) if re.match(link_regex, link))
                    for link in links:
                        link = seed_url + link
                        if link not in seen:
                            seen[link] = depth + 1
                            print(link)
                            if same_domain(seed_url, link):
                                crawl_queue.append(link)
            num_urls += 1
            if num_urls == max_urls:
                break

        else:
            print('Blocked by robots.txt', url)


def normalize(seed_url, link):
    '''
    有时候我们拿到的网址是绝对路径，这里转换一下
    其实无非一个 append
    '''
    return parse.urljoin(seed_url, link)


def same_domain(url1, url2):
    '''
    urlparse 可以解析 url，具体解析成什么类型，可以自己试试
    '''
    return parse.urlparse(url1).netloc == parse.urlparse(url2).netloc


def get_links(html):
    '''
    这里直接匹配页面中所有的 url
    '''
    is_link_regex = re.compile('<a[^>]+href=["\'](.*?)["\']')
    return is_link_regex.findall(html.text)


def print_url(url_list):
    for link in url_list:
        print(link)


def get_robots(url):
    '''
    if or not visit this website
    '''
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(parse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp


if __name__ == '__main__':
    # url = "https://httpbin.org/status/404"
    url = 'http://example.webscraping.com'
    netflix = 'https://www.netflix.com/'

    link_regex = '.*/(index|view)/.*'
    # link_crawler(url, link_regex)
    link_crawler(netflix, link_regex,
                 delay=0, user_agent='BadCrawler', max_urls=10)
