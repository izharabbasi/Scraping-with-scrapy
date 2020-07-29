import scrapy
from scrapy.crawler import CrawlerProcess
import json

class Olx(scrapy.Spider):
    name = 'olx'

    url = 'https://www.olx.in/api/relevance/search?category=1725&facet_limit=100&lang=en&location=1000001&location_facet_limit=20&page=1&showAllCars=true&user=1739bbd2288x31429d7c'

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'data.csv'
    }

    def start_requests(self):
        for page in range(1,5):
            yield scrapy.Request(url=self.url + '&page' + str(page), callback=self.parse, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.44'
            })

    def parse(self, response):
        resp = json.loads(response.body)
        datas = resp.get('data')
        for data in datas:
            yield {
                'title': data.get('title'),
                'price': data.get('price').get('value').get('display'),
                'main_info': data.get('main_info'),
                'location': data.get('locations_resolved').get('ADMIN_LEVEL_1_name' ),
                'description': data.get('description'),

            }

#run scraper
process = CrawlerProcess()
process.crawl(Olx)
process.start()