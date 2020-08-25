import scrapy
from scrapy.selector import Selector
import urllib
import json

class ForSale(scrapy.Spider):
    name = 'sale'

    base_url = 'https://www.onthemarket.com/for-sale/property/'

    params = {
        'page': '0',
        'radius': '3.0'
    }

    postcodes = []

    def __init__(self):
        content = ''

        with open('postcode.json', 'r') as f:
            for line in f.read():
                content += line
        
        print(self.postcodes.append(content))
