#!/usr/bin/python
# login with cookies
# Method build_opener_with_chrome_cookies cann't work rigth cause my_pass
# is not right
# Conlusions is here: https://github.com/n8henrie/pycookiecheat/issues/14
# But I still cann't work right. It seems like reletaed with my machine
# I won't waste my time on this thing. Maybe one day I'll figure this out


__Author__ = 'hiro'

import requests
import urllib
import os
import sqlite3
from http.cookiejar import CookieJar
from requests.cookies import RequestsCookieJar
from urllib.request import HTTPCookieProcessor
from find_div import parse_form

from Crypto.Cipher import AES
from hashlib import pbkdf2_hmac

import gi
gi.require_version('Secret', '1')
from gi.repository import Secret


def login_with_urllib(url, login_email, login_passwd):
    cj = CookieJar()
    opener = urllib.request.build_opener(HTTPCookieProcessor(cj))
    html = opener.open(url).read()
    data = parse_form(html)
    data['email'] = login_email
    data['password'] = login_passwd
    encode_data = urllib.parse.urlencode(data)
    request = urllib.request.Request(url, encode_data.encode())
    response = opener.open(request)
    return response.geturl()


def login_with_requests(url, login_email, login_passwd):
    '''
    需要先获取表单的 cookies
    使用 post 方法
    '''
    r = requests.get(url)
    data = parse_form(r.text)
    data['email'] = login_email
    data['password'] = login_passwd
    r = requests.post(url, data, cookies=r.cookies)
    return r.url


def build_opener_with_chrome_cookies(domain=None):
    cookie_file_path = '/home/hiro/.config/google-chrome/Default/Cookies'
    if not os.path.exists(cookie_file_path):
        raise Exception('Cookies file not exists')
    conn = sqlite3.connect(cookie_file_path)
    cursor = conn.cursor()
    sql = 'select host_key, name, encrypted_value from cookies'
    if domain:
        sql += ' where host_key like "%{}%"'.format(domain)

    cookiejar = RequestsCookieJar()

    cursor.execute(sql)
    for host_key, name, encrypted_value in cursor.fetchall():
        print('encrypted_value: ', encrypted_value)
        encrypted_value = encrypted_value[3:]
        decrypted_value = aes_decrypt(encrypted_value)
        print("clean_decrypted_value: ", decrypted_value)
        # cookiejar.set('host_key', host_key)
        # cookiejar.set('name', name)
        # cookiejar.set('value', decrypted_value)
        # print(cookiejar)

    conn.commit()
    conn.close()


def aes_decrypt(token):
    my_pass = 'peanuts'
    iterations = 1
    salt = b'saltysalt'
    length = 16
    iv = b' ' * length

    flags = Secret.ServiceFlags.LOAD_COLLECTIONS
    service = Secret.Service.get_sync(flags)

    gnome_keyring = service.get_collections()
    unlocked_keyrings = service.unlock_sync(gnome_keyring).unlocked

    keyring_name = "{} Safe Storage".format('Chrome'.capitalize())

    # for item in (unlocked_keyrings.get_items()):
    #     print(item.get_label())
    #     if item.get_label() == keyring_name:
    #         item.load_secret_sync()
    #         my_pass = item.get_secret().get_text()

    for unlocked_keyring in unlocked_keyrings:
        print('unlocked_keyring: ', unlocked_keyring.get_items())
        for item in unlocked_keyring.get_items():
            if item.get_label() == keyring_name:
                item.load_secret_sync()
                my_pass = item.get_secret().get_text()
                print(my_pass)
                break
        else:
            continue
        break

    print('my_pass: ', my_pass)

    key = pbkdf2_hmac(hash_name='sha1',
                      password=my_pass.encode('utf8'),
                      salt=salt,
                      iterations=iterations,
                      dklen=length)

    cipher = AES.new(key, AES.MODE_CBC, IV=iv)
    dec_token = cipher.decrypt(token)
    # pycookiecheat.pycookiecheat.chrome_decrypt(token, key, iv)
    return clean(dec_token)


def clean(x):
    print('decrypted_value: ', x)
    last = x[-1]
    if isinstance(last, int):
        return x[:-last].decode('utf8')
    return x[:-ord(last)].decode('utf8')


if __name__ == '__main__':
    url = 'http://example.webscraping.com/places/default/user/login'
    login_email = '2436678006@qq.com'
    login_passwd = 'w1234567'
    # print('login_with_urllib...................')
    # print(login_with_urllib(url, login_email, login_passwd))
    # print('login_with_requests.................')
    # print(login_with_requests(url, login_email, login_passwd))
    build_opener_with_chrome_cookies('.baidu.com')
