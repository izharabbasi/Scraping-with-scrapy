# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector


class PropertyScraperSpider(scrapy.Spider):
    name = 'property_scraper'
    allowed_domains = ['www.samtrygg.se']

    base_url = 'https://www.samtrygg.se/RentalObject/NewSearch'

    headers = {
        'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.58',
        'content-type': 'text/html; charset=utf-8'
    }

    def start_requests(self):
        yield SeleniumRequest(
            url=self.base_url,
            wait_time=3,
            headers=self.headers,
            callback=self.parse_links
        )

    def parse_links(self, response):
        cards = response.xpath("//div[@class='owl-carousel owl-theme show-nav-hover']/div/a")

        for card in cards:
            link = card.xpath(".//@href").get()

            yield SeleniumRequest(
                url= link,
                wait_time=3,
                headers=self.headers,
                callback=self.parse

            )
        next_page = response.xpath('//*[@id="next"]/@href').get()
        if next_page:
            yield scrapy.Request(
                url=next_page,
                headers=self.headers,
                callback=self.parse_links
            )
            
            
    def parse(self,response):
        features = {
            'title': response.xpath('//*[@id="property"]/div[1]/div[1]/div[2]/h1/text()').get(),
            'image_url': response.xpath("//a[@itemprop='contentUrl']/@href").getall(),
            'address' : response.xpath("//a[@id='js-scroll-to-map']/text()[2]").get().strip(),
            'description': response.xpath("//p[@itemprop='description']/text()").get().strip(),
            'Monthly_rent' : response.xpath('//*[@id="property"]/div[1]/div[2]/div[2]/div/div[1]/h5/span/text()').get().strip(),
            'Accomodation': list(filter(None,[
                text.replace('\n','').strip()
                for text in 
                response.css("div[class='boendet ammenities row'] *::text").getall()
            ])),
            'Amenities': list(filter(None,[
                text.replace('\n','').strip()
                for text in 
                response.css("div[class='ammenities row'] *::text").getall()
            ])),
        }
        yield features

        print(features)

    
        


            
            
    
    
