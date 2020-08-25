import scrapy
from scrapy.crawler import CrawlerProcess
import urllib
import json

class SoldPrices(scrapy.Spider):
    name = 'sold_prices'

    base_url = 'https://www.onthemarket.com/uk-house-prices/?'

    params = {
        'property-type-prices' : 'any',
        'search-type': 'prices',
        'sold-in': 'all-years'
    }

    custom_settings = {
        'FEED_FORMAT' : 'csv',
        'FEED_URI' : 'Sale_data.csv',
        #CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        #'DOWNLOAD_DELAY': 1
    }

    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63'
    }

    postcodes = []

    def __init__(self):
        content = ''
        with open(r'C:\Users\izhar\Projects\Property scraper\Right Move\postcode.json','r') as f:
            for line in f.read():
                content += line
            content = json.loads(content)

            for item in content:
                self.postcodes.append(item['postcode'])
            
    def start_requests(self):
        for postcode in self.postcodes:
            next_postcode = self.base_url + urllib.parse.urlencode(self.params) + '&sold-prices-input=' + postcode
            yield scrapy.Request(
                url=next_postcode,
                headers=self.headers,
                meta={
                    'postcode' : postcode
                },
                callback=self.parse
            )
            break
    
    def parse(self,response):
        postcode = response.meta.get('postcode')

        listings = response.xpath("//div[@class='outcode-street-list column_quarter']/ul/li")
        for l in listings:
            link = l.xpath(".//a/@href").get()
            street = l.xpath(".//a/text()").get()
            yield response.follow(
                url=link,
                headers=self.headers,
                meta={
                    'postcode' : postcode,
                    'street' : street
                },
                callback=self.parse_data
            )
        
        next_page = response.xpath("//a[@title='Next page']/@href").get()
        try:
            if next_page:
                yield response.follow(
                    url=next_page,
                    headers=self.headers,
                    meta={
                        'postcode' : postcode,
                        'street' : street
                    },
                    callback=self.parse
                )
        except AttributeError:
            pass



    def parse_data(self,response):
        postcode = response.meta.get('postcode')
        street = response.meta.get('street')
        cards = response.xpath("//div[@class='results list-tabcontent primary-col']/div/div")
        for card in cards:
            yield {
                'postcode': postcode,
                'street' : street,
                'address' : card.xpath("./h2/text()").get(),
                'price' : card.xpath(".//ul/li[1]/span[1]/text()").getall(),
                'description' : card.xpath(".//ul/li[1]/span[2]/text()").get(),
                'date' : card.xpath(".//ul/li[1]/span[3]/text()").get()

            }
        next_page = response.xpath("//a[@title='Next page']/@href").get()
        
        try:
            if next_page:
                yield response.follow(
                    url=next_page,
                    headers=self.headers,
                    meta={
                        'postcode' : postcode,
                        'street' : street
                    },
                    callback=self.parse_data
                )
        except AttributeError:
            pass




#run scraper
process = CrawlerProcess()
process.crawl(SoldPrices)
process.start()