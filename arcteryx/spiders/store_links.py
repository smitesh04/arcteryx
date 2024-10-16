from typing import Iterable

import scrapy
from scrapy import Request
from scrapy.cmdline import execute as ex
from arcteryx.db_config import  DbConfig
obj = DbConfig()


class StoreLinksSpider(scrapy.Spider):
    name = "store_links"
    # allowed_domains = ["."]
    # start_urls = ["https://."]
    def start_requests(self):
        obj.cur.execute(f"select * from {obj.store_links_region_table} where status=0")
        rows = obj.cur.fetchall()
        for row in rows:
            link = row['link']
            yield scrapy.Request(link, callback=self.parse, cb_kwargs=row)

    def parse(self, response, **kwargs):

        store_links = response.xpath('//div[@class="tiles wider"]/a/@href').getall()
        for link in store_links:
            link = f"https://stores.arcteryx.com{link}"
            obj.insert_store_links_table(link)
            obj.cur.execute(f"update {obj.store_links_region_table} set status=1 where link='{kwargs['link']}'")
            obj.con.commit()

if __name__ == '__main__':
    ex('scrapy crawl store_links'.split())
