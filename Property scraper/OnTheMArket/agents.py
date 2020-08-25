import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import urllib
import json

class Agents(scrapy.Spider):
    name = 'Agents'

    base_url = 'https://www.onthemarket.com/agents/'

    params = {
        'page': '0',
        'radius': '40.0'
    }

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'data.csv'
    }

    headers = {
        'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52'
    }

    postcodes = []

    def __init__(self):
        content = ''

        with open(r'C:\Users\izhar\Projects\Property scraper\Right Move\postcode.json' , 'r') as f:
            for line in f.read():
                content += line
            
        for item in json.loads(content):
            self.postcodes.append(item['postcode'])

    def start_requests(self):

        for postcode in self.postcodes:
            next_postcode = self.base_url + postcode.lower() + '/?' + urllib.parse.urlencode(self.params)
            yield scrapy.Request(url=next_postcode, headers=self.headers, callback=self.parse_links,meta={'postcode':postcode})
            
            
    def parse_links(self,res):
        postcode = res.meta.get('postcode')
        cards = res.xpath("//h3[@class='agent-name']/a")
        for card in cards:
            links = res.urljoin(card.xpath(".//@href").get())
            yield scrapy.Request(url=links, headers=self.headers, callback=self.parse_agents,meta={'postcode':postcode})
        next_page = res.urljoin(res.xpath("//a[@title='Next page']/@href").get())
        try:
            if next_page:
                yield scrapy.Request(url=next_page, headers=self.headers, callback=self.parse_links,meta={'postcode':postcode})
        except AttributeError:
            pass
            

    def parse_agents(self,res):
        postcode = res.meta.get('postcode')
        
        features = {
            'postcode': postcode,
            'url': res.url,
            'name': res.xpath("//div[@class='pull-left']/h1/text()").get(),
            'address': res.xpath("//div[@class='pull-left']/p/text()").get(),
            'phone': str(res.xpath("//div[@class='agent-phone-link']/text()").get()).replace(' ', ''),
            'desc': str(res.css("div.desc *::text").getall()).replace('              ', '').replace('\\n','').strip().replace('  ', '')

        }
        yield features
    
#run Spider
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(Agents)
    process.start()

