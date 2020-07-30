import scrapy
from scrapy.crawler import CrawlerProcess


class Onthemarket(scrapy.Spider):
    name = 'onthemarket'

    def start_requests(self):
        pass

    def parse(self,response):
        pass






#Run Spider
process = CrawlerProcess()
process.crawl(Onthemarket)
process.start()