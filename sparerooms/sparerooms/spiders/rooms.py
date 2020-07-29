# -*- coding: utf-8 -*-
import scrapy


class RoomsSpider(scrapy.Spider):
    name = 'rooms'
    allowed_domains = ['www.spareroom.co.uk/flatshare/?offset=0']
    start_urls = ['http://www.spareroom.co.uk/flatshare/?offset=0/']

    def parse(self, response):
        pass
