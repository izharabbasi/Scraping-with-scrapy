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


    def parse(self, response):
    
        driver = response.request.meta['driver']

        html = driver.page_source
        res = Selector(text=html)
        ads = res.xpath("//div[@class='_99sa']/div/div/div[2]/div/div")

        l_date = res.xpath("//div[@class='_7jwu']/span/text()").get()
        print("\n\nTHIS IS DATE", l_date)
        
        for ad in ads:
            l_date = res.xpath("//div[@class='_7jwu']/span/text()").get()
            try:
                yield {
                    'FB_AD_link' : response.url,
                    'Fan_Page' : ad.xpath(".//div[@class='_8nqr _3qn7 _61-3 _2fyi _3qng']/span/a/text()").get(),
                    'Store_link' : ad.xpath(".//div[@style='line-height: 16px; max-height: 112px; -webkit-line-clamp: 7;']/div/a/text()").get(),
                    'Product_Launch_Date': l_date,
                    'Heading' : ad.xpath(".//div[@class='_8jh2']/div/div/text()").get(),
                    'AD_copy': ad.xpath(".//div[@style='line-height: 16px; max-height: 112px; -webkit-line-clamp: 7;']/div/text()").get(),
                    'File_Generated_Date': date.today(),
                    'video_Link': ad.xpath(".//div[@class='_8o0a _8o0b']/video/@src").get()
                }
            except AttributeError:
                pass
                
