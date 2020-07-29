# -*- coding: utf-8 -*-
import scrapy


class RoomsSpider(scrapy.Spider):
    name = 'rooms'
    allowed_domains = ['www.spareroom.co.uk']

    def clean_output(self, data):
        try:
            return data.strip()
        except AttributeError:
            return ''

    def start_requests(self):
        yield scrapy.Request(
            url='https://www.spareroom.co.uk/flatshare/?offset=0',
            callback= self.parse,
            headers= {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.44'
            }
        )

    def parse(self, response):
        main_rooms = response.xpath("//ul[@class='listing-results ']/li[@class='listing-result']")
        for room in main_rooms:
            link = room.xpath(".//article/header[1]/a/@href").get()

            abosolute_link = response.urljoin(link)

            yield scrapy.Request(url = abosolute_link , callback = self.parse_rooms, meta={'link':link}, headers={
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.44'
            })

    def parse_rooms(self,response):
        link = response.request.meta['link']
        main = response.xpath("//div[@class='listing__content grid-8-4-4']")
        for one in main:
            yield {
                'Room_url' :response.urljoin(link),
                'Share_Type': one.xpath("normalize-space(.//section[@class='feature feature--details']/ul/li/text())").get(),
                'Street': one.xpath("normalize-space(.//section[@class='feature feature--details']/ul/li[2]/text())").get(),
                'Area': one.xpath("normalize-space(.//section[@class='feature feature--details']/ul/li[3]/text())").get(),
                'Double/en_suit_Price': self.clean_output(one.xpath(".//ul[@class='room-list']/li[1]/strong/text()").get()),
                'Double_Price' : self.clean_output(one.xpath(".//ul[@class='room-list']/li[2]/strong/text()").get()),
                'Aavailabe' : self.clean_output(one.xpath(".//section[@class='feature feature--availability']/dl/dd[1]/text()").get()),
                'Minimum_term' : self.clean_output(one.xpath(".//section[@class='feature feature--availability']/dl/dd[2]/text()").get()),
                'Maximum_term' : self.clean_output(one.xpath(".//section[@class='feature feature--availability']/dl/dd[3]/text()").get()),
                'Deposit_room_1': self.clean_output(one.xpath(".//section[@class='feature feature--extra-cost']/dl/dd[1]/text()").get()),
                'Deposit_room_2': self.clean_output(one.xpath(".//section[@class='feature feature--extra-cost']/dl/dd[2]/text()").get()),
                'Billing_Include': self.clean_output(one.xpath(".//section[@class='feature feature--extra-cost']/dl/dd[3]/text()").get()),
                'Furnishing': self.clean_output(one.xpath(".//section[@class='feature feature--amenities']/dl/dd[1]/span/text()").get()),
                'Parking': self.clean_output(one.xpath(".//section[@class='feature feature--amenities']/dl/dd[2]/span/text()").get()),
                'Garage': self.clean_output(one.xpath(".//section[@class='feature feature--amenities']/dl/dd[3]/span/text()").get()),
                'Garden/Terrace': self.clean_output(one.xpath(".//section[@class='feature feature--amenities']/dl/dd[4]/span/text()").get()),
                'balcony/patio': self.clean_output(one.xpath(".//section[@class='feature feature--amenities']/dl/dd[5]/span/text()").get()),
                'Disabled_access': self.clean_output(one.xpath(".//section[@class='feature feature--amenities']/dl/dd[6]/span/text()").get()),
                'Living_room': self.clean_output(one.xpath(".//section[@class='feature feature--amenities']/dl/dd[7]/span/text()").get()),
                'Broadband': self.clean_output(one.xpath(".//section[@class='feature feature--amenities']/dl/dd[8]/span/text()").get()),
                'Current_house_hold_Flatmates': self.clean_output(one.xpath(".//section[@class='feature feature--current-household']/dl/dd[1]/text()").get()),
                'Current_house_hold_Total_rooms': self.clean_output(one.xpath(".//section[@class='feature feature--current-household']/dl/dd[2]/text()").get()),
                'Current_house_hold_Smoker': self.clean_output(one.xpath(".//section[@class='feature feature--current-household']/dl/dd[3]/text()").get()),
                'Current_house_hold_Any_pet': self.clean_output(one.xpath(".//section[@class='feature feature--current-household']/dl/dd[4]/text()").get()),
                'Current_house_hold_Language': self.clean_output(one.xpath(".//section[@class='feature feature--current-household']/dl/dd[5]/text()").get()),
                'Current_house_hold_Occupation': self.clean_output(one.xpath(".//section[@class='feature feature--current-household']/dl/dd[6]/text()").get()),
                'Current_house_hold_Gender': self.clean_output(one.xpath(".//section[@class='feature feature--current-household']/dl/dd[7]/text()").get()),
                'New_flatmate_preferences_Couples_OK?' : self.clean_output(one.xpath(".//section[@class='feature feature--household-preferences']/dl/dd[1]/span/text()").get()),
                'New_flatmate_preferences_Smoking_OK?' : self.clean_output(one.xpath(".//section[@class='feature feature--household-preferences']/dl/dd[2]/span/text()").get()),
                'New_flatmate_preferences_Pets_OK?' : self.clean_output(one.xpath(".//section[@class='feature feature--household-preferences']/dl/dd[3]/span/text()").get()),
                'New_flatmate_preferences_Occupation' : self.clean_output(one.xpath(".//section[@class='feature feature--household-preferences']/dl/dd[4]/text()").get()),
                'New_flatmate_preferences_Housing_Benefit' : self.clean_output(one.xpath(".//section[@class='feature feature--household-preferences']/dl/dd[5]/span/text()").get()),
                'New_flatmate_preferences_References?' : self.clean_output(one.xpath(".//section[@class='feature feature--household-preferences']/dl/dd[6]/span/text()").get()),
                'New_flatmate_preferences_Gender' : self.clean_output(one.xpath(".//section[@class='feature feature--household-preferences']/dl/dd[7]/text()").get()),
                'image_url': response.urljoin(one.xpath(".//dl[@class='landscape']/dt/a/@href").get())

            }
        