# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest


class TableSpider(scrapy.Spider):
    name = 'table'

    def start_requests(self):
        yield SeleniumRequest(
            url = 'https://www.iayt.org/search/newsearch.asp',
            wait_time= 3,
            screenshot=True,
            callback=self.parse,
            headers={
                'User_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.44'
            }
        )



    def parse(self, response):
        driver = response.meta['driver']

        print(driver.page_source)

        table = response.xpath("//table[@style='width:100%;border-collapse:collapse;border:none;']/tbody/tr")

        for tr in table:
            yield {
                'name': tr.xpath(".//td[@style='width:75%;border:none;']/div[1]/a[1]/text()").get(),
                'url': tr.xpath(".//td[@style='width:75%;border:none;']/div[1]/a[1]/@href").get()
                
            }

        driver.save_screenshot("image.png")

