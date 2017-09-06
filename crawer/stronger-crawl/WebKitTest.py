#!/usr/bin/python


from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebKitWidgets import *


url = 'http://example.webscraping.com/places/default/search'

app = QApplication([])
webview = QWebView()
loop = QEventLoop()
webview.loadFinished.connect(loop.quit)
webview.load(QUrl(url))

loop.exec_()
webview.show()

frame = webview.page().mainFrame()
frame.findFirstElement('#search_term').setAttribute('value', '.')
frame.findFirstElement('#page_size option:checked').setPlainText('1000')
frame.findFirstElement('#search').evaluateJavaScript('this.click()')

app.exec_()
