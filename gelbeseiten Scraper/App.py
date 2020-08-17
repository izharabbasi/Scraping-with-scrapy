# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from scrapy.selector import Selector
import urllib
import time
import re

def cleanUp(inputString):
    if inputString:
        return re.sub('[\n\t\t\t]','',inputString).strip()



class YlpSpider(scrapy.Spider):
    name = "ylp"
    keyword = 'Elektronik'
    city = '/Berlin'
    radius = '?umkreis=2958'
    allowed_domains = ["gelbeseiten.de"]
    start_urls = ['https://www.gelbeseiten.de/Suche/Elektronik/Stuttgart']

    base_url = 'https://www.gelbeseiten.de/Suche/'
    url = base_url + keyword + city + radius

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59',
    }

    custom_settings = {
        #'FEED_FORMAT': 'csv',
        #'FEED_URI': 'Data.csv',
        #'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        #'DOWNLOAD_DELAY': 1
    }

    res = []

    def __init__(self):
        driver = webdriver.Chrome()
        driver.get(self.url)
        self.res.append(driver.page_source)
        time.sleep(3)
        try:
            while True:
                try:
                    loadMoreButton = driver.find_element_by_xpath(
                        '//*[@id="mod-LoadMore--button"]')
                    time.sleep(2)
                    loadMoreButton.click()
                    time.sleep(5)
                    self.res.append(driver.page_source)
                except Exception as e:
                    print(e)
                    break
        except:
            pass
        print("Complete")
        time.sleep(2)
        driver.quit()

    def parse(self, response):
        for r in self.res:
            resp = Selector(text=r)

        companies = resp.xpath("//article[@class='mod mod-Treffer']")
        for company in companies:
            yield {
            'name' : company.xpath(".//h2[@data-wipe-name='Titel']/text()").get(),
            'address' : str(company.xpath(".//p[@data-wipe-name = 'Adresse']/descendant-or-self::text()").getall()).replace('\\n\\t\\t\\t','').replace('\\n\\t\\t','').replace('\\t','').replace('\\xa0','').strip(),
            'postalcode' : re.compile(r'\d+').findall(cleanUp(company.xpath(".//address/p/span[1]/text()").get())),
            'addressLocality' : cleanUp(company.xpath('.//address/p[1]/text()[1]').get()),
            'phone' : company.xpath(".//p[@class='mod-AdresseKompakt__phoneNumber']/text()").get(),          
            'mail' : str(company.xpath(".//a[@class='contains-icon-email gs-btn']/@href").get()).replace('?subject=Anfrage%20%C3%BCber%20Gelbe%20Seiten','').replace('mailto:','').strip(),     
            'branchen' : cleanUp(company.xpath(".//p[@class='d-inline-block mod-Treffer--besteBranche']/text()").get())
            }



# Run Spider
process = CrawlerProcess()
process.crawl(YlpSpider)
process.start()
