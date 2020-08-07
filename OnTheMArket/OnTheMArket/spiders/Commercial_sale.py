# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import urllib
import json

class CommercialSpider(scrapy.Spider):
    #spider name
    name = 'Commercial_sale'
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
    
    #current page
    current_page = 1
    #postcodes list
    Postcodes = [] 

    def __init__(self):

        content = ''

        with open('Uk postcodes.json', 'r') as f:
            for line in f.read():
                content += line
        
        content = json.loads(content)

        print(content)




    def parse(self, response):
        pass
