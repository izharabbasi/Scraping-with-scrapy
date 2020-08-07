# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import urllib
import json

class CommercialSpider(scrapy.Spider):
    #spider name
    name = 'Commercial'
    allowed_domains = ['www.onthemarket.com']
    
    base_url = 'https://www.onthemarket.com/for-sale/property/'

    #search Query params
    params = {
        'page' : '0',
        'radius' : '3.0'
        }
    #headers 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52'
    }
    
    #current page
    current_page = 0
    #postcodes list
    Postcodes = [] 

    def __init__(self):

        content = ''

        with open('postcodes.json', 'r') as f:
            for line in f.read():
                content += line
        
        for item in json.loads(content):
            self.Postcodes.append(item['postcode'])

    #general crawler
    def start_requests(self):
        count = 1

        for postcode in self.Postcodes:
            next_postcode = self.base_url + postcode.lower() + '/?' + urllib.parse.urlencode(self.params)
            yield scrapy.Request(url=next_postcode , headers=self.headers, meta={'postcode': postcode, 'count': count}, callback=self.parse_links)
            count +=1
            break

    def parse_links(self, res):
        postcode = res.meta.get('postcode')
        count = res.meta.get('count')
        print(postcode , count)






#Run Spider
process = CrawlerProcess()
process.crawl(CommercialSpider)
process.start()