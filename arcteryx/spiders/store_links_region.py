import scrapy
from scrapy.cmdline import execute as ex
from 


class StoreLinksRegionSpider(scrapy.Spider):
    name = "store_links_region"
    # allowed_domains = ["."]
    start_urls = ["https://stores.arcteryx.com/regions"]

    def parse(self, response):
        region_links = response.xpath("//div[@id='US']//a/@href").getall()
        for link in region_links:

            link = f"https://stores.arcteryx.com{link}"

        print()


if __name__ == '__main__':
    ex("scrapy crawl store_links_region".split())

