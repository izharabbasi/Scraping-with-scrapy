import scrapy
from scrapy.crawler import CrawlerProcess
import urllib
import re


class ForSale(scrapy.Spider):
    name = 'for_sale'
    location = 'waikato'
    district = 'hamilton'
    suburbs = 'bader'

    base_url = 'https://www.trademe.co.nz/a/property/residential/rent/'

    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63'
    }

    custom_settings = {
        'FEED_FORMAT' : 'csv',
        'FEED_URI' : 'Rent_data.csv',
        #'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        #'DOWNLOAD_DELAY': 1
    }

    def start_requests(self):
        url = self.base_url + self.location + '/' + self.district + '/' +self.suburbs
        yield scrapy.Request(
            url= url,
            headers= self.headers,
            callback= self.parse
        )

    def parse(self,response):
        cards = response.xpath("//a[@class='tm-property-search-card__link']")

        for card in cards:
            link = card.xpath(".//@href").get()
            yield response.follow(
                url=link,
                headers=self.headers,
                callback=self.parse_listing
            )
        next_page = response.xpath("//a[contains(text(),'Next')]/@href").get()
        if next_page:
            yield response.follow(
                url=next_page,
                headers=self.headers,
                callback=self.parse
            )
        
    def parse_listing(self, response):
        
        yield {
            'link': response.url,
            'country': 'New Zealand',
            'listed': response.xpath("//div[@class='tm-property-listing-body__date p-secondary-copy']/text()").get(),
            'address': response.xpath('/html/body/trade-me/div[1]/main/div/tm-property-listing/div/tm-property-listing-body/div/section[1]/tg-row/tg-col/h1/text()').get(),
            'bedrooms': response.xpath("//ul[@class='tm-property-listing-attributes__tag-list']/li[1]/tm-property-listing-attribute-tag/tg-tag/span/div/text()").get(),
            'bathrooms': response.xpath("//ul[@class='tm-property-listing-attributes__tag-list']/li[2]/tm-property-listing-attribute-tag/tg-tag/span/div/text()").get(),
            'car_spaces' : response.xpath("(//td[@data-th='Value'])[3]/text()").get(),
            'agency' : response.xpath("//h3[@class='pt-agency-summary__agency-name']/text()").get(),
            'agent': response.xpath("//h3[@class='pt-agent-summary__agent-name']/text()").get()
        }




#Run Scraper

process = CrawlerProcess()
process.crawl(ForSale)
process.start()

