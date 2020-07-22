# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BooksComSpider(CrawlSpider):
    name = 'books.com'
    allowed_domains = ['books.toscrape.com']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40'

    def start_requests(self):
        yield scrapy.Request(url='http://books.toscrape.com', headers={
            'User-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//article[@class='product_pod']/h3/a"), callback='parse_item', follow=True,process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="//li[@class='next']/a"), process_request='set_user_agent')
    )

    def set_user_agent(self,request):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            'name': response.xpath("//div[@class='col-sm-6 product_main']/h1/text()").get(),
            'price': response.xpath("//div[@class='col-sm-6 product_main']/p[1]/text()").get(),
            'availability': response.xpath("(//div[@class='col-sm-6 product_main']/p[2]/text())[2]").get().strip(),
            'warning': response.xpath("//div[@class='alert alert-warning']/text()").get(),
            'tax': response.xpath("//tr[5]/td/text()").get()
        }
