#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author: hiro
# Learn from ‘用 Python 写网络爬虫’
# Python 3.6
# 使用 requests 库


from selenium import webdriver


def main():
    driver = webdriver.Chrome()
    url = 'http://example.webscraping.com/places/default/search'
    driver.get(url)
    driver.find_element_by_id('search_term').send_keys('.')
    js = "document.getElementById('page_size').options[1].text='1000'"
    driver.execute_script(js)
    driver.find_element_by_id('search').click()
    driver.implicitly_wait(30)

    links = driver.find_element_by_css_selector('#results a')
    countries = [link.text for link in links]
    driver.close()
    print(countries)


if __name__ == '__main__':
    main()
