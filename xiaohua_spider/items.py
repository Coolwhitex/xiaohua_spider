# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaohuaSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    age = scrapy.Field()
    cons = scrapy.Field()
    specialty = scrapy.Field()
    school = scrapy.Field()
    prof = scrapy.Field()
    title= scrapy.Field()
