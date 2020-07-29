# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TopMovieSpider(CrawlSpider):
    name = 'top_movie'
    allowed_domains = ['www.imdb.com']
    
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc',headers={
            'User-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="(//div[@class='desc'])[2]/a"), process_request='set_user_agent')
    )

    def set_user_agent(self,request):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            'title': response.xpath("(//div[@class='title_wrapper']/h1/text())[1]").get(),
            'Released_year': response.xpath("//span[@id='titleYear']/a/text()").get(),
            'timming': response.xpath("normalize-space(//div[@class='subtext']/time/text())").get(),
            'rating': response.xpath("//div[@class='ratingValue']/strong/span/text()").get(),
            'genre': response.xpath("//div[@class='subtext']/a[1]/text()").get(),
            'User-agent': response.request.headers['User-Agent']
        }