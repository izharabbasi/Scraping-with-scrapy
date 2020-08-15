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
        while driver.find_element_by_xpath("//a[@id='next']"):
            next_page = driver.find_element_by_xpath("//a[@id='next']")
            try:
                next_page.click()
            except:
                break
            
            driver.implicitly_wait(10)
            self.responses.append(driver.page_source)
           
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
                
                        
    def parse_listing(self,response):
        for r in self.responses:
            resp = Selector(text=r)
            listings = resp.xpath("//section[@class='main-content property-section']/div[1]")
            for lists in listings:
                features = {
                    'title': lists.xpath(".//div[@class='description add-content']/h1/text()").get(),
                    'address': lists.xpath(".//div[@class='description add-content']/div/h2/a/text()[2]").getall(),
                        #'address' : response.xpath("//a[@id='js-scroll-to-map']/text()[2]").get().strip(),
                        #'description': str(response.xpath("//p[@itemprop='description']/text()").get().replace('\n','').strip()),
                        #'Monthly_rent' : response.xpath('//*[@id="property"]/div[1]/div[2]/div[2]/div/div[1]/h5/span/text()').get().strip(),
                    #'Accomodation': list(filter(None,[
                    #     text.replace('\n','').strip()
                    #     for text in 
                    #     resp.css("div[class='boendet ammenities row'] *::text").getall()
                    # ])),
                    # 'Amenities': list(filter(None,[
                    #     text.replace('\n','').strip()
                    #     for text in 
                    #     resp.css("div[class='ammenities row'] *::text").getall()
                    # ])),
                    }
                yield features


    
        


            
            
    
    
