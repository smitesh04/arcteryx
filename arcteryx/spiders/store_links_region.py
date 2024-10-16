import scrapy
from scrapy.cmdline import execute as ex
from arcteryx.db_config import DbConfig
obj = DbConfig()


class StoreLinksRegionSpider(scrapy.Spider):
    name = "store_links_region"
    # allowed_domains = ["."]
    start_urls = ["https://stores.arcteryx.com/regions"]

    def parse(self, response):
        region_links = response.xpath("//div[@id='US']//a/@href").getall()
        for link in region_links:

            link = f"https://stores.arcteryx.com{link}"
            obj.insert_store_links_region_table(link)




if __name__ == '__main__':
    ex("scrapy crawl store_links_region".split())

