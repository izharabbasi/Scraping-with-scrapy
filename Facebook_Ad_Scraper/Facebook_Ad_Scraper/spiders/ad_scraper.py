# -*- coding: utf-8 -*-
import scrapy


class AdScraperSpider(scrapy.Spider):
    name = 'ad_scraper'
    allowed_domains = ['www.facebook.com']
    start_urls = ['http://www.facebook.com/']

    def parse(self, response):
        pass
