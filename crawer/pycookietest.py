import requests
from pycookiecheat import chrome_cookies


if __name__ == '__main__':
    url = 'https://www.google.com'
    cookies = chrome_cookies(url)
