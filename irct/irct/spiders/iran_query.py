# -*- coding: utf-8 -*-
import scrapy


class IranQuerySpider(scrapy.Spider):
    name = 'iran_query'
    allowed_domains = ['www.irct.ir/search/result?query=Iran']
    start_urls = ['http://www.irct.ir/search/result?query=Iran/']

    def parse(self, response):
        pass
