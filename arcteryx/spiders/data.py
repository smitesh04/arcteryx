import datetime
import json
from typing import Iterable
import datetime
import scrapy
import os
from scrapy import Request
from scrapy.cmdline import execute as ex
from arcteryx.db_config import DbConfig
from arcteryx.common_func import create_md5_hash, page_write, headers
from arcteryx.items import ArcteryxItem
today_date = datetime.datetime.today().strftime('%d_%m_%Y')

obj = DbConfig()

class DataSpider(scrapy.Spider):
    name = "data"

    # allowed_domains = ["."]/
    # start_urls = ["https://."]
    def start_requests(self):
        obj.cur.execute(f"select * from {obj.store_links_table} where status=0")
        rows = obj.cur.fetchall()
        for row in rows:
            link = row['link']
            hashid = create_md5_hash(link)
            pagesave_dir = rf"C:/Users/Actowiz/Desktop/pagesave/{obj.database}/{today_date}"
            file_name = fr"{pagesave_dir}/{hashid}.html"
            row['hashid'] = hashid
            row['pagesave_dir'] = pagesave_dir
            row['file_name'] = file_name



            if os.path.exists(file_name):
                yield scrapy.Request(url='file:///' + file_name, callback=self.parse, cb_kwargs=row)
            else:
                yield scrapy.Request(url=link, headers=headers(), callback=self.parse, cb_kwargs=row)

    def parse(self, response, **kwargs):

        file_name = kwargs['file_name']
        pagesave_dir = kwargs['pagesave_dir']
        if not os.path.exists(file_name):
            page_write(pagesave_dir, file_name, response.text)
        script_text = response.xpath('//script[@type="application/ld+json" and contains(text(),'"LocalBusiness"')]/text()').get()
        script_text = script_text.strip()
        script_jsn = json.loads(script_text)
        store_name = script_jsn['name']
        phone = script_jsn['telephone']
        street_address = script_jsn['address']['streetAddress']
        city = script_jsn['address']['addressLocality']
        region = script_jsn['address']['addressRegion']
        postalcode = script_jsn['address']['postalCode']
        lat = script_jsn['geo']['latitude']
        lng = script_jsn['geo']['longitude']

        opening_hours_list = list()

        opening_hours_list_jsn = script_jsn['openingHoursSpecification']
        for opening_hours_ in opening_hours_list_jsn[:2]:
            dayofweek_list = opening_hours_['dayOfWeek']
            for dayofweek in dayofweek_list:
                opens = opening_hours_['opens']
                closes = opening_hours_['closes']
                opening_hours_list.append(f'{dayofweek.capitalize()}: {opens}-{closes}')
        opening_hours = ' | '.join(opening_hours_list)

        direction_url = f"https://www.google.com/maps/dir/?api=1&destination={lat},{lng}"


        item = ArcteryxItem()
        item['store_no'] = ''
        item['name'] = store_name
        item['latitude'] = lat
        item['longitude'] = lng
        item['street'] = street_address
        item['city'] = city
        item['state'] = region
        item['zip_code'] = postalcode
        item['county'] = city
        item['phone'] = phone
        item['open_hours'] = opening_hours
        item['url'] = kwargs['link']
        item['provider'] = "Arcteryx"
        item['category'] = "Apparel And Accessory Stores"
        item['updated_date'] = datetime.datetime.today().strftime("%d-%m-%Y")
        item['country'] = "US"
        item['status'] = "Open"
        item['direction_url'] = direction_url
        item['pagesave_path'] = file_name

        yield item


if __name__ == '__main__':
    ex('scrapy crawl data'.split())
