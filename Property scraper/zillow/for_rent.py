import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import urllib
import json

class ForSale(scrapy.Spider):
    name = 'for_sale'
    region = input('Please Enter CITY/STATE/POSTCODE  ')

    base_url = 'https://www.zillow.com/homes/for_rent/'

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63'
    }

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'Data.csv',
        #'CONCURRENT_REQUESTS_PER_DOMAIN' : 1,
        #'DOWNLOAD_DELAY' : 0.5
    }
      

    def start_requests(self):
        url = self.base_url + self.region.lower()
        yield scrapy.Request(
            url=url,
            headers=self.headers,
            callback=self.parse
        )
        
    def parse(self,response):
        cards = response.xpath("//ul[@class='photo-cards photo-cards_wow photo-cards_short']/li")
        for card in cards:
            yield {
                'link' : response.xpath(".//a[@class='list-card-link list-card-img']/@href").get(),
                'Lising_Date' : card.xpath(".//div[@class='list-card-top']/div/text()").get(),
                'address' : card.xpath(".//address[@class='list-card-addr']/text()").get(),
                'price' : card.xpath(".//div[@class='list-card-price']/text()").get(),
                'bedrooms' : str(''.join(card.xpath(".//ul[@class='list-card-details']/li[1]/descendant-or-self::text()").getall())).replace("' '",'').replace( ' ,','').strip(),
                'bathrooms' : str(''.join(card.xpath(".//ul[@class='list-card-details']/li[2]/descendant-or-self::text()").getall())).replace("' '",'').replace( ' ,','').strip(),
                'Area' : str(''.join(card.xpath(".//ul[@class='list-card-details']/li[3]/descendant-or-self::text()").getall())).replace("' '",'').replace( ' ,','').strip(),
                'prorperty_type' : response.xpath(".//div[@class='list-card-type']/text()").get(),
                'agency_name' : response.xpath("//div[@class='list-card-brokerage list-card-img-overlay']/div/text()").get()
            }
        next_page = response.xpath("//a[@title='Next page']/@href").get()
        if next_page:
            yield response.follow(
                url=next_page,
                headers=self.headers,
                callback=self.parse
            )


#run scraper

process = CrawlerProcess()
process.crawl(ForSale)
process.start()