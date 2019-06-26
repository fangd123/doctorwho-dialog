import scrapy


class QuotesSpider(scrapy.Spider):
    name = "doctorwho"

    def start_requests(self):
        urls = [f'http://chakoteya.net/DoctorWho/episodes{x}.htm' for x in range(1,14)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
