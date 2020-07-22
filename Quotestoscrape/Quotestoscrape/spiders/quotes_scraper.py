# -*- coding: utf-8 -*-
import scrapy


class QuotesScraperSpider(scrapy.Spider):
    name = 'quotes_scraper'
    allowed_domains = ['quotes.toscrape.com']

    def start_requests(self):
        yield scrapy.Request(url='http://quotes.toscrape.com', callback=self.parse, headers={
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40'
        })

    def parse(self, response):
        quotes_main = response.xpath("(//div[@class='col-md-8'])[2]/div")

        for quote in quotes_main:
            yield {
                'content': quote.xpath(".//span[@class='text']/text()").get(),
                'author': quote.xpath(".//span[2]/small/text()").get(),
                'tags': quote.xpath(".//div[@class='tags']/a/text()").getall()
            }

        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page:
            yield response.follow(url=next_page,callback=self.parse, headers={
                'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40'
            })
