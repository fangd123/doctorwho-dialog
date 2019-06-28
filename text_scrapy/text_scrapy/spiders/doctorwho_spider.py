import scrapy
import html2text

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
        with open(f'{title}.txt','w',encoding='utf-8') as f:
            for name in episode_names:
                f.write(f'{name}\n')
        # for episode in episodes:
        #     if episode.startswith('..'):
        #         episode = episode[3:]
        #         yield scrapy.Request(url='http://chakoteya.net/' + episode, callback=self.one_parse)
        #     yield scrapy.Request(url=self.base_url+episode, callback=self.one_parse)

    def one_parse(self,response):
        texts = response.text
        texts = html2text.html2text(texts)
        title = response.xpath('//title/text()').get()
        with open(f'/Users/fangwenda/Documents/doctorwho-dialog/text/{title}.txt','w',encoding='utf-8') as f:
            f.write(texts)
