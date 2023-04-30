import scrapy


class GroupSpider(scrapy.Spider):
    name = "group"
    allowed_domains = ["51.250.32.185"]
    start_urls = ["http://51.250.32.185/"]

    def parse(self, response):
        pass
