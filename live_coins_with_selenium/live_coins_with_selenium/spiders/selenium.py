# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from shutil import which


class SeleniumSpider(scrapy.Spider):
    name = 'selenium'
    allowed_domains = ['www.livecoin.net']
    start_urls = ['https://www.livecoin.net/en/']

    def __init__(self):
        chrome_option = Options()
        chrome_option.add_argument("--headless")
        chrome_path = which("chromedriver.exe")

        driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_option)
        driver.set_window_size(1920,1080)
        driver.get("https://www.livecoin.net/en")

        tab = driver.find_element_by_xpath("//div[@class='filterPanel___2zFYQ']/div[6]")
        tab.click()
        driver.implicitly_wait(1)

        self.html = driver.page_source

        driver.close()

    def parse(self, response):
        resp = Selector(text = self.html)
        currencies = resp.xpath("//div[@class='ReactVirtualized__Grid__innerScrollContainer']/div")
        for currency in currencies:
            yield {
                'name': currency.xpath(".//div[1]/div/text()").get(),
                'volume(24)': currency.xpath(".//div[2]/span/text()").get(),
                'Last_price': currency.xpath("./div[3]/span/text()").get(),
            }