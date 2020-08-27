import scrapy
from scrapy.crawler import CrawlerProcess
import urllib
import csv
import re


class ForSale(scrapy.Spider):
    name = 'for_sale'
    
    column_names = [
        'Address',
        'Bedrooms',
        'Bathrooms',
        'Listing Title / Heading',
        'Today Listing',
        'Date Property First Listed',
        'Rent $ First Listed',
        'Rent $ Per Week',
        'Date Property Removed',
        'Agency Name',
        'Agent Name',
        'Private Agent Name',
        'Listing Link',
        'Contact Number',
        'Property Description'
    ]

   

    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63'
    }

    custom_settings = {
        #'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        #'DOWNLOAD_DELAY': 1
    }

    def __init__(self):
        with open('For_Rent.csv', 'w', newline='', encoding='utf-8') as f:
            f.write(','.join(self.column_names) + '\n')


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
       
        features =  {
            'Address': str(response.xpath('/html/body/trade-me/div[1]/main/div/tm-property-listing/div/tm-property-listing-body/div/section[1]/tg-row/tg-col/h1/text()').get()).strip(),
            'Bedrooms': str(response.xpath("//ul[@class='tm-property-listing-attributes__tag-list']/li[1]/tm-property-listing-attribute-tag/tg-tag/span/div/text()").get()).strip(),
            'Bathrooms': str(response.xpath("//ul[@class='tm-property-listing-attributes__tag-list']/li[2]/tm-property-listing-attribute-tag/tg-tag/span/div/text()").get()).strip(),
            'Listing Title / Heading': str(response.xpath("//h2[@class='tm-property-listing-body__title p-h1']/text()").get()).strip(),
            'Today Listing' : str(response.xpath("//div[@class='tm-property-listing-body__date p-secondary-copy tm-property-listing-body__date--today']/text()").get()).strip(),
            'Date Property First Listed': str(response.xpath("//div[@class='tm-property-listing-body__date p-secondary-copy']/text()").get()).strip(),
            'Rent $ First Listed': str(response.xpath("//h2[@class='tm-property-listing-body__price']/strong/text()").get()).strip(),
            'Rent $ Per Week': str(response.xpath("//h2[@class='tm-property-listing-body__price']/strong/text()").get()).strip(),
            'Date Property Removed' : str(response.xpath("//table[@class='o-table']/tbody/tr[1]/td[2]/text()").get()).strip(),
            'Agency Name' : str(response.xpath("//h3[@class='pt-agency-summary__agency-name']/text()").get()).strip(),
            'Agent Name': str(response.xpath("//h3[@class='pt-agent-summary__agent-name']/text()").get()).strip(),
            'Private Agent Name' : str(response.xpath("(//a[@class='tm-private-seller--member-name-link'])[1]/text()").get()).strip(),
            'Listing Link': response.url,
            'Contact Number': str(response.xpath("//div[@class='pt-agency-summary__agency-information-footer-section']/span/a/text()").get()).strip(),
            'Property Description' : str(response.xpath("//div[@class='tm-markdown']/descendant::node()/text()").getall()).strip()
        }
        yield features

        with open('For_Rent.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, self.column_names)
                writer.writerow(features)



#Run Scraper

process = CrawlerProcess()
process.crawl(ForSale)
process.start()

