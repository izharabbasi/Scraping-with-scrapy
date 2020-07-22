# -*- coding: utf-8 -*-
import scrapy


class DealsSpider(scrapy.Spider):
    name = 'deals'
    allowed_domains = ['www.tinydeal.com']

    def start_requests(self):
        yield scrapy.Request(url='https://www.tinydeal.com/specials.html', callback=self.parse, headers={
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40'
        })

    def parse(self, response):
        deals_main = response.xpath("//ul[@class='productlisting-ul']/div/li")
        for deal in deals_main:
            yield {
                'name': deal.xpath(".//a[@class='p_box_title']/text()").get(),
                'product_url': response.urljoin(deal.xpath(".//a[@class='p_box_title']/@href").get()),
                'actual_price': deal.xpath(".//div[@class='p_box_price']/span[1]/text()").get(),
                'discounted_price': deal.xpath(".//div[@class='p_box_price']/span[2]/text()").get(),
                'shipping': deal.xpath(".//div[@class='p_box_price']/a/text()").get()
            }

        next_page = response.xpath("//a[@class='nextPage']/@href").get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse, headers={
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40'
            })
