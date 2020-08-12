# -*- coding: utf-8 -*-
import scrapy


class PropertyScraperSpider(scrapy.Spider):
    name = 'property_scraper'
    allowed_domains = ['www.samtrygg.se']
    start_urls = ['https://www.samtrygg.se/']

    base_url = 'https://www.samtrygg.se/RentalObject/NewSearch'

    headers = {
        'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.58',
        'cookie': '.ASPXANONYMOUS=b_XM7x-n1gEkAAAAZTJjNTY0ZDQtMzVhNi00ODFmLTkzZDQtM2Y1MmRhZjE3YTI4LPix5tdrvKwwcnJwqEeXWc3RWAtgyd28urCjqHm4Reo1; _ga=GA1.2.477490575.1597225871; _gid=GA1.2.1381664640.1597225871; _vwo_uuid_v2=D1C81876362519D5FF49EFB7A628F972C|c392565894d10efecc264de768152182; _hjid=ad964e22-eb63-46d2-83c0-f73ea4a5c04a; _hjIncludedInPageviewSample=1; __ca__chat=sw9c7oGr8scT; cto_bundle=FO_dhV9vYlU4S2xVbHZic2llRmFpdkVYdmR5Q044MnBIdXp2ZTVIZzVPMmZaVE9mZHBTb05UcUxvU2V5TVVtT0Q0S3FwczNJaTBBUEpwdXhZanNrTXFZMVpwJTJCblIlMkJGQzNQSURGS3V1VFZuV0JERk5QN1FOM2RBb0ZvMzBnZ2lKbVhjS282dnIyUERGU0hNVXJOeUFIYU9DUThBJTNEJTNE; mp_2a6c1441f45b68d8dac010f9938a8688_mixpanel=%7B%22distinct_id%22%3A%20%22173e214abc72e6-0848696fb7df54-7e647c66-e1000-173e214abc8749%22%2C%22%24device_id%22%3A%20%22173e214abc72e6-0848696fb7df54-7e647c66-e1000-173e214abc8749%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D'
    }

    def start_requests(self):
        yield scrapy.Request(
            url=self.base_url,
            headers=self.headers,
            callback=self.parse_links
        )

    def parse_links(self, res):
        cards = res.xpath("//div[@class='owl-carousel owl-theme show-nav-hover']/div/a")

        for card in cards:
            link = card.xpath(".//@href").get()
            
            yield scrapy.Request(
                url=link,
                headers=self.headers,
                callback=self.parse_listings
            )
    
    def parse_listings(self,res):
        print('\n\n\nRESPONE' , res.text)
