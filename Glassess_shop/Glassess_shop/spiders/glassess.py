# -*- coding: utf-8 -*-
import scrapy


class GlassessSpider(scrapy.Spider):
    name = 'glassess'
    allowed_domains = ['www.glassesshop.com']
    start_urls = ['https://www.glassesshop.com/bestsellers']

    def start_requests(self):
        yield scrapy.Request(url='https://www.glassesshop.com/bestsellers', callback=self.parse ,headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40'
        })
    
    def clean_output(self, data):
        try:
            return data.strip()
        except AttributeError:
            return ''

    def parse(self, response):
        glassess_main = response.xpath("//div[@id='product-lists']/div")
        for glasses in glassess_main:
            yield {
                'Prouct_name': self.clean_output(glasses.xpath(".//div[@class='p-title']/a/text()").get()),
                'price': glasses.xpath(".//div[@class='p-title-block']/div[2]/div/div[2]/div/div/span/text()").get(),
                'product_url': glasses.xpath(".//div[@class='product-img-outer']/a/@href").get(),
                'image_url': glasses.xpath(".//div[@class='product-img-outer']/a/img[1]/@src").get()
            }
