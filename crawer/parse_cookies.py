#!/usr/bin/python


import os
import sqlite3
import requests


def getCookieFromChrome(host='example.webscraping.com'):
    cookie_path = '/home/hiro/.config/google-chrome/Default/Cookies'
    sql = ("select host_key, name, encrypted_value from cookies "
           "where host_key='%s'") % host
    with sqlite3.connect(cookie_path) as conn:
        cursor = conn.cursor()
        data = cursor.execute(sql).fetchall()
        print(data)
        return data


if __name__ == '__main__':
    getCookieFromChrome('.baidu.com')
