# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DemoSunItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    number = scrapy.Field()
    situation = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    in_url = scrapy.Field()
    content_text = scrapy.Field()
    content_pic = scrapy.Field()
