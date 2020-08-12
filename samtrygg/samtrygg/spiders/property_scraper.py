# -*- coding: utf-8 -*-
import scrapy


class PropertyScraperSpider(scrapy.Spider):
    name = 'property_scraper'
    allowed_domains = ['www.samtrygg.se']
    start_urls = ['https://www.samtrygg.se/']

    def parse(self, response):
        pass
