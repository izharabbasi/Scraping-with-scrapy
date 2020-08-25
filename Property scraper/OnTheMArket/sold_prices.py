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
            print(next_postcode)
#run scraper
process = CrawlerProcess()
process.crawl(SoldPrices)
process.start()