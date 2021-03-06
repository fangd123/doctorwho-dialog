import scrapy
import html2text
import json
class QuotesSpider(scrapy.Spider):
    name = "bbc-char1"
    base_url = "https://www.bbc.co.uk"
    char_names = set()
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    }
    def start_requests(self):
        urls = ['https://www.bbc.co.uk/programmes/articles/Dl87bYjhKrF2MHQM7StFXQ/characters']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        chars = response.xpath('//a[@class="block-link__overlay-link promotion__link"]/@href').getall()
        titles = response.xpath('//a[@class="block-link__overlay-link promotion__link"]/text()').getall()
        for url,name in zip(chars,titles):
            new_url = self.base_url + url
            if 'Doctors' in name or 'Characters' in name:
                callback = self.one_more_parse
            else:
                callback = self.one_parse


            if 'https' in url:
                new_url = url
            elif 'http' in url:
                new_url = url.replace('http', 'https')

            yield scrapy.Request(url=new_url, callback=callback)

    def one_more_parse(self,response):
        urls = response.xpath('//a[@class="br-blocklink__link"]/@href').getall()
        for url in urls:
            if 'http' in url:
                url = url.replace('http', 'https')
                yield scrapy.Request(url=url, callback=self.one_more_parse)
            else:
                yield scrapy.Request(url=self.base_url + url, callback=self.one_parse)

    def one_parse(self,response):
        name = response.xpath('//div[@class="prog-layout prog-layout__primary component programmes-page--topboxed"]/h1/text()').get()
        texts = response.xpath('//div[@class="prog-layout prog-layout__primary component programmes-page--topboxed"]/div/p/text()').get()
        des = response.xpath('//tr/td//text()').getall()
        des = list(filter(lambda x:x.strip() != '',des))
        des_dict = dict()
        i = 0
        while i < len(des) - 1:
            des_dict[des[i].strip()[:-1]] = des[i+1].strip()
            i += 2
        des_dict['name'] = name
        des_dict['des'] = texts
        print(des_dict)
        with open(f'../text/characters/{name}.txt','w',encoding='utf-8') as f:
            json.dump(des_dict,f)
