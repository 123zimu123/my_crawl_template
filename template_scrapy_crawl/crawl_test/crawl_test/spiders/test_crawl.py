# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

import re
class TestCrawlSpider(CrawlSpider):
    name = 'test_crawl'
    allowed_domains = ['circ.gov.cn']
    start_urls = ['http://circ.gov.cn/web/site0/tab5240/']

    #rules执行流程  根据allow提取对应的url，并发送对应的请求，并将请求之后得到的响应交给callback对应的函数来处理，若follow为true，则在得到的响应中继续提取这个满足这个rule的url
    rules = (
        Rule(LinkExtractor(allow=r'/web/site0/tab5240/info\d+\.htm'), callback='parse_item', follow=False),#allow的内容是详情页的url，对于详情页，我们重点关注内容，对内容进行提取（callback），详情页的url只会出现在列表页，详情页中不会出现，所以不要follow
        Rule(LinkExtractor(allow=r'/web/site0/tab5240/module14430/page\d+\.htm'),  follow=True),#allow的内容是列表页，对于列表页，需要在获得url响应中继续提取下一页（几页）
    )

    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        item['title'] = response.xpath("//title/text()").extract_first()
        item['date'] = response.xpath("//td[contains(text(),'发布时间')]/text()").extract_first()
        item['date'] = re.findall("20\d{2}-\d{2}-\d{2}",item['date'])

        print(item)
        return item
"""        
        也可以替换成这个
        item['data'] = response.body.decode("utf-8")
        item['data'] = re.findall("20\d{2}-\d{2}-\d{2}",item['data'])"""


