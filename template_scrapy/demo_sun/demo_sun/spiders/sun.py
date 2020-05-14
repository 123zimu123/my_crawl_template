# -*- coding: utf-8 -*-
import scrapy
from demo_sun.items import DemoSunItem
import re
class SunSpider(scrapy.Spider):
    name = 'sun'
    allowed_domains = ['sun0769.com']
    start_urls = ['http://wz.sun0769.com/political/index/politicsNewest?id=1&type=4&page=0']

    def parse(self, response):
        li_list = response.xpath("//li[@class = 'clear']")
        for li in li_list:
            item = DemoSunItem()
            item['number'] = li.xpath("./span[@class = 'state1']/text()").extract_first()
            item['situation'] = li.xpath("./span[@class = 'state2']/text()").extract_first()
            item['title'] = li.xpath("./span[@class = 'state3']/a/text()").extract_first()
            item['date'] = li.xpath("/span[last()]/text()").extract_first()
            item['in_url'] = li.xpath("./span[@class = 'state3']/a/@href").extract_first()
            item['in_url'] = "http://wz.sun0769.com/"+item['in_url']
            yield scrapy.Request(item['in_url'],callback=self.parse_in,meta={"item":item})

        next_url = response.xpath("//a[contains(@class,'arrow-page prov_rota')]/@href").extract_first()
        next_url = "http://wz.sun0769.com/" + next_url
        yield scrapy.Request(next_url,callback=self.parse)

    def parse_in(self,response):
        item = response.meta["item"]
        item['content_text'] = response.xpath("//pre/text()").extract_first()
        item['content_pic'] = response.xpath("//div[contains(@class,'clear details')]/img/@src").extract_first()
        yield item