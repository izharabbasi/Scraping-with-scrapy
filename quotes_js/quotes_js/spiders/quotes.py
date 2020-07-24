# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']

    script = '''
        function main(splash, args)
        splash.private_mode_enabled = false
        headers = {
            ['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40'
        }
        splash:set_custom_headers(headers)
        assert(splash:go(args.url))
        assert(splash:wait(1))
        splash:set_viewport_full()
        return splash:html()
    end
    '''
    def start_requests(self):
        yield SplashRequest(url='http://quotes.toscrape.com/js', callback=self.parse, endpoint='execute', args={
            'lua_source': self.script
        })

    def parse(self, response):
        quotes = response.xpath("//div[@class='quote']")
        for quote in quotes:
            yield {
                'Content': quote.xpath(".//span[1]/text()").get(),
                'Author': quote.xpath(".//span[2]/small/text()").get(),
                'Tags': quote.xpath(".//div/a/text()").getall()
            }
        next_page = response.urljoin(response.xpath("//li[@class='next']/a/@href").get())
        if next_page:
            yield SplashRequest(url=next_page, callback=self.parse, endpoint='execute', args={
                'lua_source': self.script
            })
