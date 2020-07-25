# -*- coding: utf-8 -*-
import scrapy


class TableSpider(scrapy.Spider):
    name = 'table'
    allowed_domains = ['www.iayt.org/search/newsearch.asp']
    start_urls = ['http://www.iayt.org/search/newsearch.asp/']

    def parse(self, response):
        pass
