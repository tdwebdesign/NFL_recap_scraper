import scrapy


class EspnRecapSpider(scrapy.Spider):
    name = "ESPN_recap"
    allowed_domains = ["espn.com"]
    start_urls = ["https://espn.com"]

    def parse(self, response):
        pass
