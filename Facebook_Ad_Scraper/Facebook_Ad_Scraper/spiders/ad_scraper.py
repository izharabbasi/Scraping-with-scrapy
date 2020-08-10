# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from shutil import which
import urllib
import json
import re


class AdScraperSpider(scrapy.Spider):
    name = 'ad_scraper'
    allowed_domains = ['www.facebook.com']

    Input_file = r'C:\Users\izhar\Projects\Facebook_Ad_Scraper\Facebook_Ad_Scraper\spiders\InputFile.csv'

    

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52'    
    }
    custom_settings = {
        #'FEED_FORMAT': 'csv',
        #'FEED_URI': 'Data.csv',
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'DOWNLOAD_DELAY': 1
    }
    
    def start_requests(self):
        urls = ''

        with open(self.Input_file, 'r') as f:
            for line in f.read():
                urls += line

        urls = urls.split('\n')
        for url in urls:
            print(url)
        #     #yield SeleniumRequest(url=url, headers=self.headers, wait_time=3, screenshot=True, callback=self.parse)
            break



    def parse(self, response):
        pass
