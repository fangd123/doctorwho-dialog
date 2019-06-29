import scrapy
import html2text

class QuotesSpider(scrapy.Spider):
    name = "bbc-char"
    base_url = "https://www.bbc.co.uk"
    char_names = set()
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    }
    def start_requests(self):
        urls = ['https://www.bbc.co.uk/programmes/profiles/3vymXF3zvFmq8H2R9CtClKk/season-1-characters',
               'https://www.bbc.co.uk/programmes/profiles/4GFPW3Y2fHNcW1V3WV7GdF8/season-2-characters',
               'https://www.bbc.co.uk/programmes/profiles/1tgtYSz98D1kCtmBzNZCCzd/season-3-characters',
               'https://www.bbc.co.uk/programmes/profiles/l4FkfqdhmfLZY3B7x0LNlT/season-4-characters',
               'https://www.bbc.co.uk/programmes/profiles/1mmFKsD0RHtcKV66TsZLflk/season-5-characters',
               'https://www.bbc.co.uk/programmes/profiles/33Q85wMtkn1Jf0pq3frcGHl/season-6-characters',
               'https://www.bbc.co.uk/programmes/profiles/1R1wfzHkVvWMK4VXhP8rdyp/season-7-characters',
               'https://www.bbc.co.uk/programmes/profiles/54mfY1KY6p3fymVXw36jfqc/season-8-characters',
               'https://www.bbc.co.uk/programmes/profiles/3bWvqhL6LlN0BPvf2YnC1r8/season-9-characters',
               'https://www.bbc.co.uk/programmes/profiles/3cd4Z8Bm8JTMxsHNfMvX7Gh/season-10-characters',]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        chars = response.xpath('//a[@class="block-link__overlay-link"]/@href').getall()

        for name in chars:
            if name not in self.char_names:
                self.char_names.add(name)
                yield scrapy.Request(url=self.base_url+name, callback=self.one_parse)

    def one_parse(self,response):
        name = response.xpath('//div[@class="prog-layout prog-layout__primary component programmes-page--topboxed"]/h1/text()').get()
        texts = response.xpath('//div[@class="prog-layout prog-layout__primary component programmes-page--topboxed"]/div/p/text()').get()
        des = response.xpath('//div[@class="island--horizontal"]//text()').getall()
        des = list(filter(lambda x:x.strip() != '',des))
        with open(f'../text/{name}.txt','w',encoding='utf-8') as f:
            f.write(texts+'\n')
            for x in des:
                f.write(f'{x.strip()}\n')
