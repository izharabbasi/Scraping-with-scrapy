# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import urllib

class CommercialSpider(scrapy.Spider):
    #spider name
    name = 'Commercial'
    allowed_domains = ['www.onthemarket.com']
    
    base_url = 'https://www.onthemarket.com/for-sale/property/da1'

    #search Query params
    params = {
        'page' : '0',
        'radius' : '3.0'
        }
    #headers 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52'
    }
    
















    def parse(self, response):
        pass
