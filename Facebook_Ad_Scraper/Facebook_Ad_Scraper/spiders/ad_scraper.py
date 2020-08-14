# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from scrapy.selector import Selector
from datetime import date
import re


class AdScraperSpider(scrapy.Spider):
    name = 'ad_scraper'
    allowed_domains = ['www.facebook.com']

    start_urls = [
        'https://web.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&impression_search_field=has_impressions_lifetime&view_all_page_id=100113075122815'
    ]

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

    
    def __init__(self):
        self.driver = webdriver.Chrome()
        urls = ''

        with open(self.Input_file, 'r') as f:
            for line in f.read():
                urls += line

        urls = urls.split('\n')
        for self.url in urls:
            self.driver.get(self.url)
            break
            

    def parse(self, response):
        resp = Selector(text=self.driver.page_source)
        items = {
            'Heading' : resp.xpath("//div[@class='_3qn7 _61-0 _2fyh _3qnf']/div/span/a/text()").get(),
            'store_link' : resp.xpath("//a[@data-lynx-mode='asynclazy'][1]/text()").get()
        }
        yield items


        
        

    















            # yield scrapy.Request(
            #     url= store_link,
            #     headers=self.headers,
            #     meta={
            #         'FB_AD_link': FB_AD_link,
            #         'Fan_Page':Fan_Page,
            #         'store_link':store_link,
            #         'Heading':Heading,
            #         'AD_copy':AD_copy,
            #         'video_Link':video_Link
            #     },
            #     callback= self.parse_website
            # )












    # def parse_website(self,response):

    #     store_link = response.meta['store_link']
    #     FB_AD_link = response.meta['FB_AD_link']
    #     Fan_Page = response.meta['Fan_Page']
    #     Heading = response.meta['Heading']
    #     AD_copy = response.meta['AD_copy']
    #     video_Link = response.meta['video_Link']
    #     self.driver.get(store_link).click()

    #     items = {
    #         'FB_AD_link':FB_AD_link,
    #         'Fan_Page':Fan_Page,
    #         'store_link':store_link,
    #         'Heading':Heading,
    #         'AD_copy':AD_copy,
    #         'video_Link':video_Link
            
    #     }
    #     yield items
