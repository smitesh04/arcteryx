import json
from typing import Iterable

import scrapy
from scrapy import Request
from scrapy.cmdline import execute as ex
from arcteryx.db_config import DbConfig
import re
obj = DbConfig()


class StoresSpider(scrapy.Spider):
    name = "stores"
    # allowed_domains = ["."]
    # start_urls = ["https://."]
    def start_requests(self):
        url = "https://stores.arcteryx.com/"
        url = "https://arcteryx.com/us/en/stores/find-a-store"

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': 'pxcts=33644e3f-8adf-11ef-b2c9-75f04e12a0b5; _pxvid=f08b32b3-8ade-11ef-9219-ca1de5417573; _px2=eyJ1IjoiMzJlODRlNDAtOGFkZi0xMWVmLTk5MDEtOGIwM2MyZTI5NzM3IiwidiI6ImYwOGIzMmIzLThhZGUtMTFlZi05MjE5LWNhMWRlNTQxNzU3MyIsInQiOjE3Mjg5ODc5NzI3MjEsImgiOiJkNmRlN2ZkNzEyOTNlN2Y5ZjkyODA4YWEzYzg0YjYxNDNlMDFlYzZlNDAwZDNmODFhZDhmYTQ1YzA3OTkyZjk1In0=; forterToken=59f4249a13b54a38ac7498523f1aeb20_1728987673685__1i_21ck; s_ecid=MCMID%7C16122402688279020860908523584001961972; AMCVS_DFBF2C1653DA80920A490D4B%40AdobeOrg=1; AMCV_DFBF2C1653DA80920A490D4B%40AdobeOrg=179643557%7CMCIDTS%7C20012%7CMCMID%7C16122402688279020860908523584001961972%7CMCAID%7CNONE%7CMCOPTOUT-1728994875s%7CNONE%7CMCAAMLH-1729592475%7C7%7CMCAAMB-1729592475%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CMCSYNCSOP%7C411-20019%7CvVersion%7C5.5.0; _hjSessionUser_33114=eyJpZCI6IjE3OTEwZWE0LWI3ZjktNTIwMy1iYTg0LTBjZDY2NjI3NWUyYSIsImNyZWF0ZWQiOjE3Mjg5ODc2ODE3ODAsImV4aXN0aW5nIjp0cnVlfQ==; _hjSession_33114=eyJpZCI6IjE3MDQ1NGM2LWUzYzYtNDFkNi04OGY0LTNmNTE1M2UwOWI2NiIsImMiOjE3Mjg5ODc2ODE3ODIsInMiOjEsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; _fbp=fb.1.1728987681913.654228913116702350; _pin_unauth=dWlkPVl6ZG1aakpsTVdNdFlqVXdaQzAwWldZNExUbGhOakF0TXpsa01UazVZalprWTJFMQ; _uetsid=39d684d08adf11efb6ecc7247536210f; _uetvid=39d6b8a08adf11efb6b79f99bc1f3482; _rdt_uuid=1728987682638.f6b082f2-6797-4f79-8ef1-93f790a04313; s_cc=true; _tt_enable_cookie=1; _ttp=rIBPTUAkWum7gO0FtaxoNdCb_rp; _br_uid_2=uid%3D4434055671272%3Av%3D15.0%3Ats%3D1728987683891%3Ahc%3D1; _scid=21r3qRmsUlQ3N8duT3xe0MVvsyOlnPL9; _scid_r=21r3qRmsUlQ3N8duT3xe0MVvsyOlnPL9; _gid=GA1.2.1132803228.1728987711; lg_session_v1=eyJpdiI6Im1zaEp2bnBSa1JOcjVaVVU0NEhBeXVYVHVWVkhzNTZYcmg3Q0tMTXlrUnc9IiwidmFsdWUiOiJcL1NaaktMRWFcL3VtZVB3Z1J4YWt5RXRodVdLWHpNWGhoQit1VEVGUk9Zc1AzQTJSYmVla1poanNkZUxpNkQwUDdnSHBnQ2xwWGwwOEtkdFVxNG1YZ2FBPT0iLCJtYWMiOiIwNmJiNWQ0MTE1NGM1MDI4MDY2ZGFlMTJiNjMzMTAyOTRlMWM5YjVjYjI1ZjA0ZGYzOGRiMzIwODIyZTJjOTNmIn0%3D; _ga_5LSDYDWHDT=GS1.1.1728987709.1.1.1728987750.0.0.0; _ga_9XF088BE08=GS1.1.1728987710.1.1.1728987750.0.0.0; _ga=GA1.2.616547763.1728987710; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Oct+15+2024+15%3A52%3A30+GMT%2B0530+(India+Standard+Time)&version=202409.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=61d84cdf-8a47-4d28-adb9-e0d44d145b6f&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        }

        yield scrapy.Request(url, headers=headers, callback=self.parse)


    def parse(self, response):
        script = response.xpath("//script[@type='application/ld+json']/text()").get()

        script = script.strip()
        jsn = json.loads(script)
        for store in jsn:
            link = store['url']
            obj.insert_store_links_table(link)
            print(link)





if __name__ == '__main__':
    ex('scrapy crawl stores'.split())