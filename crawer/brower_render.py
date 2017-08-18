#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author: hiro
# Learn from ‘用 Python 写网络爬虫’
# Python 3.6
# 使用 requests 库


import re
import csv
import time

from PyQt5.QtCore import QUrl, QEventLoop, QTimer
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebKitWidgets import QWebView

import lxml.etree


class BrowerRender(QWebView):
    def __init__(self, display=True):
        self.app = QApplication([])
        QWebView.__init__(self)
        if display:
            self.show()

    def open(self, url, timeout=60):
        loop = QEventLoop()
        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(loop.quit)
        self.loadFinished.connect(loop.quit)
        self.load(QUrl(url))
        timer.start(timeout * 1000)
        loop.exec_()

        if timer.isActive():
            timer.stop()
            return self.html()
        else:
            print('Request timed out: ', url)

    def html(self):
        return self.page().mainFrame().toHtml()

    def find(self, pattern):
        return self.page().mainFrame().findAllElements(pattern)

    def attr(self, pattern, name, value):
        for e in self.find(pattern):
            e.setAttribute(name, value)

    def text(self, pattern, value):
        for e in self.find(pattern):
            e.setPlainText(value)

    def click(self, pattern):
        for e in self.find(pattern):
            e.evaluateJavaScript('this.click()')

    def wait_load(self, pattern, timeout=60):
        deadline = time.time() + timeout
        while time.time() < deadline:
            self.app.processEvents()
            matches = self.find(pattern)
            if matches:
                return matches
        print('Wait load timed out')


def main():
    br = BrowerRender()
    url = 'http://example.webscraping.com/places/default/search'
    br.open(url)
    br.attr('#search_term', 'value', '.')
    br.text('#page_size option:checked', '1000')
    br.click('#search')

    elements = br.wait_load('#results a')
    writer = csv.writer(open('countries.csv', 'w'))
    for country in [e.toPlainText().strip() for e in elements]:
        writer.writerow([country])


if __name__ == '__main__':
    main()
