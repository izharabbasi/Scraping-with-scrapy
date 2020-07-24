# -*- coding: utf-8 -*-
import scrapy


class CoinsSpider(scrapy.Spider):
    name = 'coins'
    allowed_domains = ['www.livecoin.net/en']
    start_urls = ['http://www.livecoin.net/en/']

    def parse(self, response):
        pass
