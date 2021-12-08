import scrapy
from scrapy.selector import Selector
from doubanzufang.items import DoubanzufangItem

class ZufangSpider(scrapy.Spider):
    name = 'zufang'
    allowed_domains = ['www.douban.com']
    #start_urls = ['http://https://www.douban.com/']

    def start_requests(self):
        # 豆瓣小组 cat=1013
        base_url = 'https://www.douban.com/group/search?cat=1013&q='
        search_keywords = [
            '深圳租房'
        ]

        for keyword in search_keywords:
            yield scrapy.Request(url=base_url+keyword, callback=self.parse)

    def parse(self, response):
        items = response.css('tr.pl');

        for item in items:
            data = DoubanzufangItem()
            data['title'] = item.xpath('td[1]/a/text()').get()
            data['href'] = item.xpath('td[1]/a/@href').get()
            data['update_date'] = item.xpath('td[2]/@title').get()
            data['group'] = item.xpath('td[4]/a/text()').get()
            request = scrapy.Request(data['href'],
                             callback=self.parse_detail,
                             cb_kwargs=dict(data=data))
            yield request
            break

        return
        next_page = response.css('.next > a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)


    def parse_detail(self, response, data):
        texts = response.css('.rich-content > p::text').getall()
        content = ''.join(texts)
        data['content'] = content

        yield data
