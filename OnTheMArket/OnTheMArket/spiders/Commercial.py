# -*- coding: utf-8 -*-
import scrapy


class CommercialSpider(scrapy.Spider):
    name = 'Commercial'
    allowed_domains = ['www.onthemarket.com']
    start_urls = ['http://www.onthemarket.com/']

    def parse(self, response):
        pass
