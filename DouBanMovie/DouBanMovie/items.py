# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanmovieItem(scrapy.Item):
    pageurl = scrapy.Field()
    numcomment = scrapy.Field()
    commentlist = scrapy.Field()
    pass

class Comment(scrapy.Item):
    pageurl = scrapy.Field()	
    userurl = scrapy.Field()
    support = scrapy.Field()
    against = scrapy.Field()
    daterec = scrapy.Field()
    replyno = scrapy.Field()
    pass