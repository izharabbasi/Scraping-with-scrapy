# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from shutil import which
import string


class YlpSpider(scrapy.Spider):
    name = "ylp"
    alphabets = string.ascii_lowercase
    allowed_domains = ["gelbeseiten.de"]
    start_urls = ['https://www.gelbeseiten.de/Suche/Elektronik/Bundesweit']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59',
    }

    custom_settings = {
        # 'FEED_FORMAT': 'csv',
        # 'FEED_URI': 'Data.csv',
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'DOWNLOAD_DELAY': 1
    }

    def __init__(self):
        driver = webdriver.Chrome()
        driver.get('https://www.gelbeseiten.de/Suche/Elektronik/Bundesweit')

    def parse(self, response):
        #companies = response.xpath('//*[@class="name m08_name"]')

        for company in response.css('article'):
            name = company.xpath(
                './/span[@itemprop="name"]//text()').extract_first()
            address = company.xpath(
                './/span[@itemprop="streetAddress"]//text()').extract_first()
            postalcode = company.xpath(
                './/span[@itemprop="postalCode"]//text()').extract_first()
            addressLocality = company.xpath(
                './/span[@itemprop="addressLocality"]//text()').extract_first()
            phone = company.xpath(
                './/span[@class="nummer"]//text()').extract_first()
            mail = company.xpath(
                './/a[@class="link email_native_app"]/@href').extract()
            branchen = company.xpath(
                './/div[@data-role="branchen"]/div/span/text()').extract_first()

            yield{'Name': name, 'Address': address, 'PLZ': postalcode, 'Ort': addressLocality, 'Tel': phone, 'Mail': mail, 'Branche': branchen}


# Run Spider
process = CrawlerProcess()
process.crawl(YlpSpider)
process.start()
