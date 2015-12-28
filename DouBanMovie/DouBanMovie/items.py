# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanmovieItem(scrapy.Item):
    filename = scrapy.Field()
    title = scrapy.Field()
    pageurl = scrapy.Field()
    total = scrapy.Field()
    cnt5 = scrapy.Field()
    cnt4 = scrapy.Field()
    cnt3 = scrapy.Field()
    cnt2 = scrapy.Field()
    cnt1 = scrapy.Field()
    datalist = scrapy.Field()
    pass

class CommentElem(scrapy.Item):
    title = scrapy.Field()
    pageurl = scrapy.Field()	
    #userurl = scrapy.Field()
    score = scrapy.Field()
    support = scrapy.Field()
    against = scrapy.Field()
    replyno = scrapy.Field()
    timerec = scrapy.Field()
    pass

class TimeRecord(scrapy.Item):
    year = scrapy.Field()
    month = scrapy.Field()
    day = scrapy.Field()
    hour = scrapy.Field()
    minute = scrapy.Field()
    second = scrapy.Field()
    pass