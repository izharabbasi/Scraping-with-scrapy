import scrapy
from scrapy.crawler import CrawlerProcess
import urllib
import json
import csv
import re


def cleanUp(inputString):
    if inputString:
        return re.sub('[\n\\n\n\n''                      ]','',inputString).strip()


class forRent(scrapy.Spider):
    name = 'Rent'
    # in-3002/list-1
    base_url = 'https://www.realestate.com.au/rent/'

    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63'
    }

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'Data.csv',
        #'CONCURRENT_REQUESTS_PER_DOMAIN' : 1,
        #'DOWNLOAD_DELAY' : 0.5
    }

    column_names = [
        'Address',
        'Listing Title / Heading',
        'postcode',
        'Rent $ First Listed',
        'Rent $ Per Month/Weak',
        'Date Property Removed',
        'Agency Name',
        'Agent_address',
        'listing_link',
        'Contact Number',
        'Features',
        'Property Description'
    ]

    postcodes = []
    def __init__(self):
        with open('For_Rent.csv', 'w', newline='', encoding='utf-8') as f:
            f.write(','.join(self.column_names) + '\n')

        content = ''
        with open(r'C:\Users\izhar\Projects\Property scraper\realestateAU\postcodes.json', 'r') as f:
            for line in f.read():
                content += line

        for item in json.loads(content):
            self.postcodes.append(item['postcode'])

    

    # def start_requests(self):
    #     for postcode in self.postcodes:
    #         next_postcode = self.base_url + postcode.lower()
    #         yield scrapy.Request(url=next_postcode, headers=self.headers, meta={'postcode':postcode}, callback=self.parse)
            
    
    # def parse(self, response):
    #     postcode = response.meta.get('postcode')

    #     cards = response.xpath("//ul[@id='properties']/li")
    #     for card in cards:
    #         title = card.xpath('.//div[3]/p[2]/span[1]/a/text()').get()
    #         address = card.xpath('.//div[3]/p[2]/span[2]/a/text()').get()
    #         link = card.xpath(".//div[3]/p[2]/span[2]/a/@href").get()
            
    #         yield response.follow(
    #             url=link,
    #             headers=self.headers,
    #             meta={
    #                 'title': title,
    #                 'address': address,
    #                 'postcode':postcode
    #             },
    #             callback=self.parse_listings
    #         )
    #     next_page = response.xpath("//a[@title='Next page']/@href").get()
    #     try:
    #         if next_page:
    #             yield response.follow(
    #                 url = next_page,
    #                 headers = self.headers,
    #                 meta = {
    #                     'postcode': postcode
    #                 },
    #                 callback = self.parse
    #             )
    #     except AttributeError:
    #         pass
    
    # def parse_listings(self,response):
    #     postcode = response.meta.get('postcode')
    #     title = response.meta.get('title')
    #     address = response.meta.get('address')

    #     features = {
    #         'Address': address,
    #         'Listing Title / Heading': title,
    #         'postcode': postcode,
    #         'Rent $ First Listed': response.xpath("(//p[@class='price'])[1]/span[1]/text()").get(),
    #         'Rent $ Per Month/Weak' : response.xpath("(//p[@class='price'])[1]/span[1]/text()").get(),
    #         'Date Property Removed': response.xpath("//div[@class='letting-details']/ul/li[1]/text()").get(),
    #         'Agency Name' : response.xpath('//*[@id="property-actions"]/div/div[1]/div/a/div[2]/h2/text()').get(),
    #         'Agent_address' : response.xpath('//*[@id="property-actions"]/div/div[1]/div/a/div[2]/div/text()').get().strip(),
    #         'listing_link': response.url,
    #         'Contact Number': response.xpath('//*[@id="property-actions"]/div/div[1]/div/div/div[2]/text()').get(),
    #         'Features' : str(response.xpath("//ul[@class='property-features']/li/descendant::text()").getall()).strip(),
    #         'Property Description' : cleanUp(str(response.xpath("//div[@id='description-text']/descendant::text()").getall())).replace('\\n','').replace('','')

    #     }
    #     yield features

    #     with open('For_Rent.csv', 'a', newline='', encoding='utf-8') as f:
    #             writer = csv.DictWriter(f, self.column_names)
    #             writer.writerow(features)

    


#run scraper
process = CrawlerProcess()
process.crawl(forRent)
process.start()