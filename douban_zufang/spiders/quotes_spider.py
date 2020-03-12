import scrapy
from scrapy.selector import Selector
from  douban_zufang.items import ZufangItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        base_url = 'https://www.douban.com/group/search?cat=1013&q='
        places = [
            '常兴花园',
            '金宝花园',
            '仓前锦福苑',
            '南山市场',
            '华府苑',
            '康达苑',
            '康乐村',
            '大陆庄园',
            '荔苑小区',
            '荔芳小区'            
        ]

        for place in places:
            yield scrapy.Request(url=base_url+place, callback=self.parse)

    def parse(self, response):
        
        item = ZufangItem()
        selector = Selector(response)
        table = selector.xpath('/html/body/div[3]/div[1]/div/div[1]/div[3]/table/tbody/tr')

        for line in table:
            title_digist = line.xpath('./td[1]/a/text()').extract()[0]
            title = line.xpath('./td[1]/a/@title').extract()[0]
            content = line.xpath('./td[1]/a/@href').extract()[0]
            update_date = line.xpath('./td[2]/span/text()').extract()[0]
            group = line.xpath('./td[4]/a/text()').extract()[0]

            item['title'] = title
            item['title_digist'] = title_digist
            item['content'] = content
            item['update_date'] = update_date
            item['group'] = group
            yield item
        
        # 暂时只爬一页
        # nextLink = selector.xpath('//span[@class="next"]/link/@href').extract()
        # if nextLink:
        #     nextLink = nextLink[0]
        #     print(nextLink)
        #     yield scrapy.Request(nextLink, callback=self.parse)            
