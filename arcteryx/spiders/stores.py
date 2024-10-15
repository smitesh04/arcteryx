import scrapy


class StoresSpider(scrapy.Spider):
    name = "stores"
    allowed_domains = ["."]
    start_urls = ["https://."]

    def parse(self, response):
        pass
