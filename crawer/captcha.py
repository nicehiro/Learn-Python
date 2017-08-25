#!/usr/bin/python


__Author__ = 'hiro'


from io import BytesIO
import lxml.etree
from PIL import Image
import requests
import base64
import pytesseract
from find_div import parse_form
from urllib.parse import urlencode


def get_captcha(html):
    tree = lxml.etree.HTML(html)
    l = tree.xpath('//div[@id="recaptcha"]/img')
    img = l[0].get('src')
    img_data = img.partition(',')[-1].encode()
    binary_img_data = base64.b64decode(img_data)
    file_like = BytesIO(binary_img_data)
    img = Image.open(file_like)
    img.save('captcha_original.png')
    gray = img.convert('L')
    gray.save('captcha_gray.png')
    bw = gray.point(lambda x: 0 if x < 1 else 255, '1')
    bw.save('captcha_thresholded.png')
    return bw


def img2str(img):
    return pytesseract.image_to_string(img)


def register(url, first_name, last_name, email, password, captcha_fn):
    r = requests.get(url)
    data = parse_form(r.text)
    data['first_name'] = first_name
    data['last_name'] = last_name
    data['email'] = email
    data['password'] = data['password_two'] = password
    img = get_captcha(r.text)
    captcha = captcha_fn(img)
    data['recaptcha_response_field'] = captcha
    encoded_data = urlencode(data)
    reps = requests.post(url, data, cookies=r.cookies)
    success = '/user/register' not in reps.url
    print(success)
    return success


if __name__ == '__main__':
    url = 'http://example.webscraping.com/places/default/user/register'
    register(url, 'ds', 'qq', '232342@qq.com', 'w1234567', img2str)
