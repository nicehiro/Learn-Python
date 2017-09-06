#!/usr/bin/python
# 对 'http://example.webscraping.com/places/default/edit/Algeria-4'
# 网址进行登录和 post 操作的时候，需要先登录才行。需要获取 cookies1 来登录
# 请求上诉网址将会直接跳转到登录页面，由此登录操作之后获取 cookies2
# 上诉操作之后，返回的网页才是真正的 edit 页面。而此时如果再次 post 操作时，
# 需要提供的 cookies2 提交你的 post

__Author__ = 'hiro'


from find_div import parse_form
import requests
from urllib.parse import urlencode


login_email = '2436678006@qq.com'
login_passwd = 'w1234567'


def login(url):
    r1 = requests.get(url)
    data = parse_form(r1.text)
    data['email'] = login_email
    data['password'] = login_passwd
    r2 = requests.post(r1.url, data, cookies=r1.cookies)

    data2 = parse_form(r2.text)
    data2['population'] = int(data2['population']) + 1
    encoded_data = urlencode(data2)

    r3 = requests.post(url, encoded_data, cookies=r2.cookies)
    print(r3.url)


if __name__ == '__main__':
    url = 'http://example.webscraping.com/places/default/edit/Algeria-4'
    login(url)
