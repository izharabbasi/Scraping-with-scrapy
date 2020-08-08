import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import urllib
import json

class Agents(scrapy.Spider):
    name = 'Agents'

    base_url = 'https://www.onthemarket.com/agents/'

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'data.csv'
    }