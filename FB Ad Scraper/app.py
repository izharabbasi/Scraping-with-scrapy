# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import urllib
import json


class AdScraperSpider(scrapy.Spider):
    name = 'ad_scraper'
    allowed_domains = ['www.facebook.com']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52'    
    }
    custom_settings = {
        #'FEED_FORMAT': 'csv',
        #'FEED_URI': 'Data.csv',
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'DOWNLOAD_DELAY': 1
    }
    urls = []
    def __init__(self):
        content = ''

        with open('InputFile.csv', 'r') as f:
            for line in f.read():
                content += line

            print(content)



    def parse(self, response):
        pass
