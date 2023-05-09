import scrapy

from yatube_parsing.items import YatubeParsingItem


class YatubeSpider(scrapy.Spider):
    name = "yatube"
    allowed_domains = ["51.250.32.185"]
    start_urls = ["http://51.250.32.185/"]

    def parse(self, response):
        for post in response.css("div.card-body"):
            text = " ".join(t.strip()
                            for t in post.css("p::text").getall()).strip()
            data = {
                "text": text,
                "author": post.css(".card-text strong::text").get(),
                "date": post.css("small.text-muted::text").get(),
            }
            yield YatubeParsingItem(data)

        # По CSS-селектору ищем ссылку на следующую страницу.
        next_page = response.xpath(
            "//a[contains(., 'Следующая')]/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
