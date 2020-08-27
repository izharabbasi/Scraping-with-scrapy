import scrapy
from scrapy.crawler import CrawlerProcess
import urllib
import re


class ForSale(scrapy.Spider):
    name = 'for_sale'
   

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
        yield scrapy.Request(
            url= 'https://www.trademe.co.nz/a/property/residential/rent/search?page=5',
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
        # next_page = response.xpath("//a[contains(text(),'Next')]/@href").get()
        # if next_page:
        #     yield response.follow(
        #         url=next_page,
        #         headers=self.headers,
        #         callback=self.parse
        #     )
        
    def parse_listing(self, response):
        
        yield {
            'Address': response.xpath('/html/body/trade-me/div[1]/main/div/tm-property-listing/div/tm-property-listing-body/div/section[1]/tg-row/tg-col/h1/text()').get(),
            'Bedrooms': response.xpath("//ul[@class='tm-property-listing-attributes__tag-list']/li[1]/tm-property-listing-attribute-tag/tg-tag/span/div/text()").get(),
            'Bathrooms': response.xpath("//ul[@class='tm-property-listing-attributes__tag-list']/li[2]/tm-property-listing-attribute-tag/tg-tag/span/div/text()").get(),
            'Listing Title / Heading': response.xpath("//h2[@class='tm-property-listing-body__title p-h1']/text()").get(),
            'Date Property First Listed': response.xpath("(//div[@_ngcontent-frend-c46])[2]/text()").get(),
            'Agency Name' : response.xpath("//h3[@class='pt-agency-summary__agency-name']/text()").get(),
            'Agent Name': response.xpath("//h3[@class='pt-agent-summary__agent-name']/text()").get(),
            'Listing Link': response.url,
            'Contact Number': response.xpath("//a[@_ngcontent-frend-c97]/@href").get(),
            'Property Description' : response.xpath("//div[@class='tm-markdown']/descendant::node()/text()").getall()
        }




#Run Scraper

process = CrawlerProcess()
process.crawl(ForSale)
process.start()

