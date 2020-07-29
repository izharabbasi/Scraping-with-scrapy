# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class CoinsSpider(scrapy.Spider):
    name = 'coins'
    allowed_domains = ['www.livecoin.net']

    script = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            headers = {
                ['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40'
            }
            splash:set_custom_headers(headers)
            assert(splash:go(args.url))
            assert(splash:wait(1))
            other_tab = assert(splash:select_all(".filterPanelItem___2z5Gb "))
            other_tab[6]:mouse_click()
            splash:set_viewport_full()
            return splash:html()

        end
    '''
    def start_requests(self):
        yield SplashRequest(url='https://www.livecoin.net/en/', callback=self.parse, endpoint='execute', args={
            'lua_source': self.script
        })

    def parse(self, response):
        currencies = response.xpath("//div[contains(@class, 'ReactVirtualized__Table__row tableRow___3EtiS ')]")
        for currency in currencies:
            yield {
                'Name': currency.xpath(".//div[1]/div/text()").get(),
                'volume(24h)': currency.xpath(".//div[2]/span/text()").get(),
                'last_price': currency.xpath(".//div[3]/span/text()").get()
            }

