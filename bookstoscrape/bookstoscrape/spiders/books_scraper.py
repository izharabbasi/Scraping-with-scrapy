# -*- coding: utf-8 -*-
import scrapy


class BooksScraperSpider(scrapy.Spider):
    name = 'books_scraper'
    allowed_domains = ['books.toscrape.com']

    def start_requests(self):

        yield scrapy.Request(url='http://books.toscrape.com/', callback=self.parse, headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40'
        })
    
    def parse(self,response):
        books = response.xpath("//article[@class='product_pod']/h3/a")
        for book in books:
            name = book.xpath(".//text()").get(),
            link = response.urljoin(book.xpath(".//@href").get())
            
            yield response.follow(url=link, callback=self.books_parse, meta = {"book_name":name})
        next_page = response.xpath("//li[@class='next']/a/@href").get()

        if next_page:
            yield response.follow(url=next_page, callback=self.parse, headers={
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40'
            })
    def books_parse(self,response):
        name = response.request.meta["book_name"]
        main = response.xpath("//div[@class='col-sm-6 product_main']")
        for b in main:
            yield {
                'book_name':name,
                'price':b.xpath(".//p[1]/text()").get(),
                'in_stock':b.xpath(".//p[@class='instock availability']/text()[2]").get().strip(),
                'warning':b.xpath(".//div[@class='alert alert-warning']/text()").get(),
            }






