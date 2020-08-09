import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import urllib
import json

class CommercialSale(scrapy.Spider):
    name = 'commercial_sale'

    base_url = "https://www.fundainbusiness.nl/alle-bedrijfsaanbod/"

    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52",
        'cookie' : 'ASPXANONYMOUS=xZvh_I78IFmhVwcJXfBv3dmVv9xSURzAkQ9NtSPDJqpvGZGf_yVzgwfeKkYKABJ6-uswsN7ayxo-pQmajnEcwvH19YCRsTf31dTwHnwMmFwy_1i2BNWBuexIe1bEru74PWDD8yKwNszdFQMUG8jXDjuV8hI1; sr=0%7cfalse; SNLB3=01-007; html-classes=js; optimizelyEndUserId=oeu1596998177462r0.5067296431643598; ak_bmsc=7FA4F047DF133A94EB6C003282EE2696B81CDAC40D5700001A42305FCF98F12B~pl2y2KpNpeQXf2/DkrIkAjClgfaIsP6iNBnnEr7SdL1EuQL5zXx+EqCFaOuZfZcf0PnDHdz8WGWtD1KdV3uTZC+74aGj1ziK0kJNzn8jSoAzljqoqZy6JSmjJafQCNu0csbq6KuTNjJol8Oy6JmMEjUCbA4pzo30hmMiqwLPvljsQM1sJ/hlGU8vf3/FuynEs437+U74glb1slWXdeKiB/JD7aVkZp/qQiv/Dp2gunuo8kBY/vXDO8Pfws16SvsfQv; _gcl_au=1.1.1091044010.1596998186; _ga=GA1.2.2115117388.1596998187; _gid=GA1.2.680745437.1596998187; sessionstarted=true; OptanonAlertBoxClosed=2020-08-09T18:36:37.169Z; eupubconsent=BO34pYTO34pYTAcABBNLDW-AAAAyN7_______9_-____9uz_Ov_v_f__33e8__9v_l_7_-___u_-23d4u_1vf99yfmx-7etr3tp_47ues2_Xurf_71__3z3_9pxP78E89r7335EQ_v-_t-b7BCHN_Y2v-8K96lPKACE; objectnotfound=objectnotfound=false; fonts-loaded=true; ajs_anonymous_id=%22ada12710-b2ad-419c-bc23-d7d2748f197f%22; lzo=fib=%2falle-bedrijfsaanbod%2f1016%2fpermaand%2f%2b5km%2f; __RequestVerificationToken=HZ_-0s7hqCD7CTp39IZSRlPqPnsmtyZD85_LhjUfiLwr2-Cn_s7HG0pwscNeAMhVXhiopQN19WsCbgx6cvxnLmBBcxU1; OptanonConsent=isIABGlobal=false&datestamp=Sun+Aug+09+2020+23%3A39%3A04+GMT%2B0500+(Pakistan+Standard+Time)&version=6.3.0&landingPath=NotLandingPage&groups=F01%3A1%2CF02%3A1%2CF03%3A1%2CF05%3A1%2CBG9%3A1&hosts=&geolocation=PK%3B&AwaitingReconsent=false; bm_sv=505A26CB2E3BB65C7B91B4DA6378741F~NktKD+NB/K/Y0qgpUaIr/aCdft1CO4VXdaIYCWJI87BXXhnD0sMYmH7v4gyul/wsNzGKHEpl8QEq9XDcWHZMvXPKvUKX0BvA8z0MAxNwTxwByJewWFlOO9kjwTV14GvAnY0+PZTOZtvZsBpJGvFTkeXKHa5uziLIVcuLYlKZ0yQ=; _gat_UA-3168440-17=1; _dd_s=logs=1&id=6f0f4cac-42f5-46fe-b26e-0720a090e1e7&created=1596998179637&expire=1596999272030',
        'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }

    custom_settings = {
        'FEDD_FORMAT': 'csv',
        'FEED_URI': 'Data.csv'

        'CONCURRENT_REQUESTS_PER_DOMAIN' : 2,
        'DOWNLOAD_DELAY' : 1
    }
    #current page
    current_page = 0

    #Scraper entry point
    def start_requests(self):
        for postcode in range(1000,10000):
            print(postcode)


    #run scraper

    process = CrawlerProcess()
    process.crawl(CommercialSale)
    process.start()


