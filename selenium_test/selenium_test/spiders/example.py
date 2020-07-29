# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys

class ExampleSpider(scrapy.Spider):
    name = 'example'
    
    def start_requests(self):
        yield SeleniumRequest(
            url='https://www.duckduckgo.com',
            wait_time=3,
            screenshot= True,
            callback= self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']

        search_input = driver.find_element_by_xpath("//input[@id='search_form_input_homepage']")
        search_input.send_keys("hello world")
        btn = driver.find_element_by_xpath("//input[@id='search_button_homepage']")
        btn.click()

        html = driver.page_source

        resp = Selector(text=html)

        links = resp.xpath("//div[@class='result__extras__url']/a")
        for link in links:
            yield {
                'url': link.xpath(".//@href").get()
            }

