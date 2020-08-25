import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import urllib
import json
import re

def cleanUp(inputString):
    if inputString:
        return re.sub('[\n\\n\n\n''                      ]','',inputString).strip()

class ForSale(scrapy.Spider):
    name = 'sale'

    base_url = 'https://www.onthemarket.com/for-sale/property/'

    params = {
        'page': '0',
        'radius': '3.0'
    }

    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63'
    }

    custom_settings = {
        'FEED_FORMAT' : 'csv',
        'FEED_URI' : 'Sale_data.csv'
    }

    postcodes = []

    def __init__(self):
        content = ''

        with open(r'C:\Users\izhar\Projects\Property scraper\Right Move\postcode.json', 'r') as f:
            for line in f.read():
                content += line
        
        for item in json.loads(content):
            self.postcodes.append(item['postcode'])

        
    def start_requests(self):
        for poscode in self.postcodes:
            next_postcode = self.base_url + poscode.lower() + '/?' + urllib.parse.urlencode(self.params)
            yield scrapy.Request(url=next_postcode,headers=self.headers, meta={'postcode': poscode}, callback=self.parse)
            break

    def parse(self, response):
        postcode = response.meta.get('postcode')

        cards = response.xpath("//ul[@id='properties']/li")
        for card in cards:
            title = card.xpath('.//div[3]/p[2]/span[1]/a/text()').get()
            address = card.xpath('.//div[3]/p[2]/span[2]/a/text()').get()
            price = card.xpath('.//div[3]/p[1]/a/text()[1]').get()
            link = card.xpath(".//div[3]/p[2]/span[2]/a/@href").get()
            
            yield response.follow(
                url=link,
                headers=self.headers,
                meta={
                    'title': title,
                    'address': address,
                    'price': price,
                    'postcode':postcode
                },
                callback=self.parse_listings
            )
    
    def parse_listings(self,response):
        postcode = response.meta.get('postcode')
        title = response.meta.get('title')
        address = response.meta.get('address')
        price = response.meta.get('price')

        yield {
            'postcode':postcode,
            'id': response.url.split("https://www.onthemarket.com/details/")[-1].split('/')[0],
            'title': title,
            'address': address,
            'price' : price,
            'agent' : response.xpath('//*[@id="property-actions"]/div/div[1]/div/a/div[2]/h2/text()').get(),
            'agent_address' : response.xpath('//*[@id="property-actions"]/div/div[1]/div/a/div[2]/div/text()').get().strip(),
            'agent_phone': response.xpath('//*[@id="property-actions"]/div/div[1]/div/div/div[2]/text()').get(),
            'features' : str(response.xpath("//ul[@class='property-features']/li/descendant::text()").getall()).strip(),
            'description' : cleanUp(str(response.xpath("//div[@id='description-text']/descendant::text()").getall())).replace('\\n','').replace('','')

        }
      



#Run Scraper
process = CrawlerProcess()
process.crawl(ForSale)
process.start()