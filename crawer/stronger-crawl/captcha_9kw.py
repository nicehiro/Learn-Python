#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
import requests
import time
from io import BytesIO

from PIL import Image
from captcha import register

import base64
import urllib


class CaptchaAPI:
    def __init__(self, api_key, timeout=60):
        self.api_key = api_key
        self.timeout = timeout
        self.url = 'https://www.9kw.eu/index.cgi'

    def solve(self, img):
        print(type(img))
        img_buffer = BytesIO()
        img.save(img_buffer, format="PNG")
        img_data = img_buffer.getvalue()
        captcha_id = self.send(img_data).text
        start_time = time.time()
        while time.time() < start_time + self.timeout:
            try:
                text = self.get(captcha_id).text
            except CaptchaError:
                pass
            else:
                if text != 'NO DATA':
                    if text == 'ERROR NO USER':
                        raise CaptchaError('Error: no user available to solve')
                    else:
                        print('Captcha Solved!')
                        return text
            print('Waiting for Captcha_9kw')

        raise CaptchaError('Error: API timeout')

    def send(self, img_data):
        print('Submittting Captcha')
        data = {
            'action': 'usercaptchaupload',
            'apikey': self.api_key,
            'file-upload_01': base64.b64encode(img_data),
            'base64': '1',
            'selfsolve': '0',
            'maxtimeout': '60'
        }
        encoded_data = urllib.parse.urlencode(data)
        r = requests.post(self.url, encoded_data)
        self.check(r.text)
        return r

    def get(self, captcha_id):
        data = {
            'action': 'usercaptchacorrectdata',
            'id': captcha_id,
            'apikey': self.api_key,
            'info': '1'
        }

        encoded_data = urllib.parse.urlencode(data)
        r = requests.get(self.url + '?' + encoded_data)
        self.check(r.text)
        return r

    def check(self, result):
        if re.match('00\d\d \w+', result):
            raise CaptchaError('API Error: ' + result)


class CaptchaError(Exception):
    pass


def main(api_key, url, filename):
    captcha = CaptchaAPI(api_key)
    print(register(url, 'Test Account', 'Test Account',
                   'example.com', 'example', captcha.solve))


if __name__ == '__main__':
    api_key = 'AKW1CDUTLREJR7O9C5'
    filename = '/home/hiro/crawer/captcha_thresholded.png'
    url = 'http://example.webscraping.com/places/default/user/register'
    # main(api_key, url, filename)
    captcha = CaptchaAPI(api_key)
    img = Image.open(filename)
    captcha.solve(img)
