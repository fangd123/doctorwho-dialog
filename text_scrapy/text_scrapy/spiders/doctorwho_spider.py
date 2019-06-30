import scrapy
import html2text
from pathlib import Path
class QuotesSpider(scrapy.Spider):
    name = "doctorwho"
    base_url = "http://chakoteya.net/DoctorWho/"
    def start_requests(self):
        urls = [f'http://chakoteya.net/DoctorWho/episodes{x}.html' for x in range(1,14)]
        urls += [f'http://chakoteya.net/DoctorWho/episodes{x}.htm' for x in range(1,14)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        episodes = response.xpath('//table/tbody/tr/td/font/a/@href').getall()
        episode_names = response.xpath('//table/tbody/tr/td/font/a/text()').getall()
        title = response.xpath('//head/title/text()').get()
        with open(f'../text/episodes/{title}.txt','w',encoding='utf-8') as f:
            for name in episode_names:
                f.write(f'{name}\n')
        for episode in episodes:
            if episode.startswith('..'):
                episode = episode[3:]
                yield scrapy.Request(url='http://chakoteya.net/' + episode, callback=self.one_parse)
            yield scrapy.Request(url=self.base_url+episode, callback=self.one_parse)

    def one_parse(self,response):
        texts = response.text
        texts = html2text.html2text(texts)
        title = response.xpath('//title/text()').get()
        title = title.strip().replace('\r\n',' ')
        title = title.replace('\t',' ')
        refer_url = bytes.decode(response.request.headers.getlist('Referer')[0])
        refer_url = refer_url.split('/')[-1].split('.')[0]
        dir_p = Path(f'../text/stories/{refer_url}')
        dir_p.mkdir(exist_ok=True)
        with open(f'../text/stories/{refer_url}/{title}.txt','w',encoding='utf-8') as f:
            f.write(texts)
