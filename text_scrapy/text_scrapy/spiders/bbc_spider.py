import scrapy
import html2text

class QuotesSpider(scrapy.Spider):
    name = "bbc"
    base_url = "https://www.bbc.co.uk"
    def start_requests(self):
        url = 'https://www.bbc.co.uk/programmes/articles/26lPl8SMrCtDvM3k3H9nLW2/the-doctors'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        doctors = response.xpath('//a[@class="block-link__overlay-link promotion__link"]/@href').getall()
        doctor_names = [name.split('/')[-1] for name in doctors]
        for doctor in doctors:
            if doctor[0] != "h":
                yield scrapy.Request(url=self.base_url+doctor, callback=self.one_parse)
            else:
                yield scrapy.Request(url=doctor, callback=self.one_parse)

    def one_parse(self,response):
        name = response.xpath('//div[@class="prog-layout prog-layout__primary component programmes-page--topboxed"]/h1/text()').get()
        texts = response.xpath('//div[@class="prog-layout prog-layout__primary component programmes-page--topboxed"]/div/p/text()').get()
        with open(f'../text/{name}.txt','w',encoding='utf-8') as f:
            f.write(texts)
