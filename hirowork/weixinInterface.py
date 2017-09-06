# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import urllib2, json
from lxml import etree

class WeixinInterface:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.template_root = os.path.join(self.app_root, 'templates')
        self.render = 
