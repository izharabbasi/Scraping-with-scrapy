# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CoinsSpider(CrawlSpider):
    name = 'coins'
    allowed_domains = ['coinmarketcap.com']

    
    def start_requests(self):
        yield scrapy.Request(url='http://coinmarketcap.com', headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40'
        })
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@class='cmc-table__column-name sc-1kxikfi-0 eTVhdN']/a"), callback='parse_item', follow=True,process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="(//div[@class='cmc-table-listing__pagination-button-group cmc-button-group va78v0-0 RDZiS'])[2]/a[1]"),process_request='set_user_agent')
    )

    def set_user_agent(self,request):
        request.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40'
        return request

    def parse_item(self, response):
        yield {
            'name':response.xpath("//div[@class='cmc-details-panel-header sc-1extin6-0 gMbCkP']/h1/text()").get(),
            'price':response.xpath("//tbody[@class='cmc-details-panel-about__table']/tr[1]/td/text()").get(),
            'rank':response.xpath("//tbody[@class='cmc-details-panel-about__table']/tr[3]/td/text()").get(),
            'market_cap':response.xpath("//tbody[@class='cmc-details-panel-about__table']/tr[4]/td/text()").get()
        }
