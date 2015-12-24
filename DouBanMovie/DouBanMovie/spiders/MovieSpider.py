# -*- coding: utf-8 -*-
import scrapy


class MoviespiderSpider(scrapy.Spider):
    name = "MovieSpider"
    #allowed_domains = ["http://movie.douban.com/"]
    start_urls = (
        #'http://www.http://movie.douban.com//',
        
    )

    def parse(self, response):
        pass
