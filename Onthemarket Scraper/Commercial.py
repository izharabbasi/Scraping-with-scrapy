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
    
    base_url = 'https://www.onthemarket.com/for-sale/commercial/property/'

    params = {
        'page' : '0',
        'radius': '3.0'
    }

    headers = {
        'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52'
    }

    #Current Page
    current_page = 0

    #postcode List
    postcodes = []

    def __init__(self):

        content = ''
        with open('postcodes.json', 'r') as f:
            for line in f.read():
                content += line

        for item in json.loads(content):
            self.postcodes.append(item['postcode'])

        
    def start_requests(self):
        count = 1

        for postcode in self.postcodes:
            self.current_page = 0
            next_postcode = self.base_url + postcode.lower() + '/?' + urllib.parse.urlencode(self.params)
            yield scrapy.Request(url=next_postcode, headers=self.headers, meta={'postcode':postcode, 'count':count}, callback=self.parse_link)
            count += 1
            break
    
    def parse_link(self,res):
        postcode = res.meta.get('postcode')
        count = res.meta.get('count')

        cards = res.xpath("//span[@class='title']/a")
        for card in cards:
            link = res.urljoin(card.xpath(".//@href").get())
            yield res.follow(url=link, headers=self.headers, meta={'postcode':postcode}, callback=self.parse_listing)
            break
        

    def parse_listing(self,res):
        #postcode = res.meta.get('postcode')

        content = ''

        with open('res.html' , 'r') as f:
            for line in f.read():
                content += line

        res = Selector(text=content)

        #extract features
        features = {
            'id' : '',
            'url' : '',
            'postcode' :'',
            'title' : '',
            'address' : '',
            'price' : '',
            'agent_link' : '',
            'agent_name' : '',
            'agent_address' : '',
            'agent_phone' : '',
            'image_url' : '',
            'full_description' : ''
            
        }

        print(json.dumps(features, indent=2))



        



            

#Run Spider
if __name__ == "__main__":
    #process = CrawlerProcess()
    #process.crawl(CommercialSpider)
    #process.start()

    CommercialSpider.parse_listing(CommercialSpider, '')