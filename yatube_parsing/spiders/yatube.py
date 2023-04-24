import scrapy


class YatubeSpider(scrapy.Spider):
    name = "yatube"
    allowed_domains = ["51.250.32.185"]
    start_urls = ["http://51.250.32.185/"]

    def parse(self, response):
        for post in response.css('div.card-body'):
            # Заменили return на yield.
            text = ' '.join(t.strip() for t in post.css('p::text').getall()).strip()
            yield {
                'text': text,
                'author': post.css('.card-text strong::text').get(),
                'date': post.css('small.text-muted::text').get(),
            }

        # По CSS-селектору ищем ссылку на следующую страницу.
        next_page = response.xpath("//a[contains(., 'Следующая')]/@href").get()
        if next_page is not None:
            # Если ссылка нашлась, загружаем страницу по ссылке
            # и вызываем метод parse() ещё раз.
            yield response.follow(next_page, callback=self.parse)
