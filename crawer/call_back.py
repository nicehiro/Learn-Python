# -*- coding: utf-8 -*-

import csv
import re
import lxml.etree
from stronger_crawer import link_crawler


class ScrapeCallback:
    def __init__(self):
        self.writer = csv.writer(open('countries.csv', 'w'))
        self.fields = ('area', 'population', 'iso', 'country', 'capital',
                       'continent',
                       'tld', 'currency_code', 'currency_name', 'phone',
                       'postal_code_format', 'postal_code_regex',
                       'languages', 'neighbours')
        self.writer.writerow(self.fields)

    def __call__(self, url, html):
        if re.search('/view/', url):
            tree = lxml.etree.HTML(html.text)
            row = []
            for field in self.fields:
                text = tree.xpath(
                    'body//tr[@id="places_{}__row"]/td[@class="w2p_fw"]'
                    .format(field))[0].text
                row.append(text)
            self.writer.writerow(row)


if __name__ == '__main__':
    link_regex = '.*/(index|view)/.*'
    url = 'http://example.webscraping.com'
    link_crawler(url, link_regex,
                 delay=0, max_urls=10,
                 scrape_callback=ScrapeCallback())
