# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from shutil import which
from datetime import date
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
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'Data.csv',
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
            yield SeleniumRequest(url=url, headers=self.headers, wait_time=3, screenshot=True, callback=self.parse)
            break

    @property       
    def getDays(self):

        today = date.today()
        ad_date = date(2020,8,9)
        current_date = today - ad_date
        return current_date


    def parse(self, response):
    
        driver = response.request.meta['driver']

        html = driver.page_source
        res = Selector(text=html)
        ads = res.xpath("//div[@class='_99sa']/div/div/div[2]/div/div")

        
        for ad in ads:
            try:
                yield {
                    'FB_AD_link' : response.url,
                    'Fan_Page' : ad.xpath(".//div[@class='_8nqr _3qn7 _61-3 _2fyi _3qng']/span/a/text()").get(),
                    'Store_link' : ad.xpath(".//div[@style='line-height: 16px; max-height: 112px; -webkit-line-clamp: 7;']/div/a/text()").get(),
                    'Number_of_Days_Launched': str(self.getDays.replace(', 0:00:00',''),
                    'Heading' : ad.xpath(".//div[@class='_8jh2']/div/div/text()").get(),
                    'AD_copy': ad.xpath(".//div[@style='line-height: 16px; max-height: 112px; -webkit-line-clamp: 7;']/div/text()").get(),
                    'Product_Launch_Date': ad.xpath(".//div[@class='_7jwu']/span[1]/text()").get(),
                    'File_Generated_Date': date.today()
                }
            except AttributeError:
                pass
                
