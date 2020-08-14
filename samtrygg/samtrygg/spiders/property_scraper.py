# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from shutil import which



class PropertyScraperSpider(scrapy.Spider):
    name = 'property_scraper'
    allowed_domains = ['www.samtrygg.se']

    start_urls = [
        'https://www.samtrygg.se/RentalObject/NewSearch'
    ]

    responses = []
 
    def __init__(self):
        chrome_path = which('chromedriver')
        driver = webdriver.Chrome(executable_path=chrome_path)
        driver.get('https://www.samtrygg.se/RentalObject/NewSearch')
        driver.implicitly_wait(10)
        self.responses.append(driver.page_source) 
        try:
            while driver.find_element_by_xpath("//a[@id='next']"):
                next_page = driver.find_element_by_xpath("//a[@id='next']")
                next_page.click()
                driver.implicitly_wait(10)
                self.responses.append(driver.page_source)
        except:
            driver.implicitly_wait(10)    
        driver.close()
        

    def parse(self, response):
        for r in self.responses:
            resp = Selector(text=r)
            cards = resp.xpath("//div[@class='owl-carousel owl-theme show-nav-hover']/div")

            for card in cards:
                link = card.xpath(".//a/@href").get()
                    
                yield scrapy.Request(
                    url= link,
                    callback=self.parse_listing,
                )
                break
                        
    def parse_listing(self,response):
        for r in self.responses:
            resp = Selector(text=r)
        features = {
            'title': resp.xpath('//*[@id="property"]/div[1]/div[1]/div[2]/h1/text()').get(),
            'image_url': resp.xpath("//a[@itemprop='contentUrl']/@href").getall(),
                #'address' : response.xpath("//a[@id='js-scroll-to-map']/text()[2]").get().strip(),
                #'description': str(response.xpath("//p[@itemprop='description']/text()").get().replace('\n','').strip()),
                #'Monthly_rent' : response.xpath('//*[@id="property"]/div[1]/div[2]/div[2]/div/div[1]/h5/span/text()').get().strip(),
            'Accomodation': list(filter(None,[
                text.replace('\n','').strip()
                for text in 
                resp.css("div[class='boendet ammenities row'] *::text").getall()
            ])),
            'Amenities': list(filter(None,[
                text.replace('\n','').strip()
                for text in 
                resp.css("div[class='ammenities row'] *::text").getall()
            ])),
            }
        yield features


    
        


            
            
    
    
