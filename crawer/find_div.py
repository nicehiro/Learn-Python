#!/usr/bin/python


import lxml.etree
import requests
from pprint import PrettyPrinter


login_url = 'http://example.webscraping.com/places/default/user/login'
login_email = '2436678006@qq.com'
login_passwd = 'w1234567'


def parse_form(html):
    tree = lxml.etree.HTML(html)
    data = {}
    l = tree.xpath('body//form//input')
    print(l)
    for e in l:
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data


def main():
    r = requests.get(login_url)
    data = parse_form(r)
    PrettyPrinter(indent=4).pprint(data)
    return data


def login(data):
    data['email'] = login_email
    data['password'] = login_passwd

    r = requests.get(login_url, data)
    print(r.url)


if __name__ == '__main__':
    data = main()
    login(data)
