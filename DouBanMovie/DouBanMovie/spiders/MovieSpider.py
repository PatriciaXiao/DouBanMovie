# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.utils.url import urljoin_rfc
from DouBanMovie.items import DoubanmovieItem

import string
import os
import codecs
import sys
import urllib2
import urllib
import lxml.html
from bs4 import BeautifulSoup
import ssl 
import json
import re

reload(sys)
sys.setdefaultencoding('utf-8')


class MoviespiderSpider(scrapy.Spider):
    name = "MovieSpider"
    #allowed_domains = ["http://movie.douban.com/"]
    start_urls = (
        #'http://www.http://movie.douban.com//',
        'http://movie.douban.com/subject/26320029/reviews?start=0&filter=&limit=20',
    )

    def parse(self, response):
        # item definition
        data_elem = DoubanmovieItem()
        # requests
        parser = scrapy.http.Request(response.url, callback=self.parse_page)
        parser.meta['MyData'] = data_list
        yield parser
        # output

    def parse_page(self, response):
        mycontent = response.meta['MyData']
        # parse a page
        print response.url
        raw_input("debug:" + response.url)
        # list of comments
        response_content = response.xpath('//*[@id="content"]/div/div[1]/div[1]/div').extract()
        raw_input("debug: list length%d\n" % len(response_content))
        # for each comment
        for i in range(len(response_content)):
            # title
            comment_title = response.xpath('//*[@id="content"]/div/div[1]/div[1]/div[' + str(i + 1) + ']/div[1]/h3/a[2]/@title').extract()[0]
            raw_input("debug: ")
            print comment_title
            # url
            comment_url = response.xpath('//*[@id="content"]/div/div[1]/div[1]/div[' + str(i + 1) + ']/div[1]/h3/a[2]/@href').extract()[0]
            raw_input("debug: ")
            print comment_url
            # stars
            stars_score_str = response.xpath('//*[@id="content"]/div/div[1]/div[1]/div[' + str(i + 1) + ']/div[1]/div/span/@class').extract()[0]
            stars_score_str = re.findall("\d+", stars_score_str)[0]
            stars_score = string.atoi(stars_score_str) # 10 for a star
            # date
            date_string = response.xpath('//*[@id="content"]/div/div[1]/div[1]/div[' + str(i + 1) + ']/div[1]/div/text()').extract()[1].strip(' \r\n-|\\/=><').split(' ')[0]
            year = string.atoi(date_string.split('-')[0])
            month = string.atoi(date_string.split('-')[1])
            day = string.atoi(date_string.split('-')[2])
            # time
            time_string = response.xpath('//*[@id="content"]/div/div[1]/div[1]/div[' + str(i + 1) + ']/div[1]/div/text()').extract()[1].strip(' \r\n-|\\/=><').split(' ')[-1]
            hour = string.atoi(time_string.split(':')[0])
            minute = string.atoi(time_string.split(':')[1])
            second = string.atoi(time_string.split(':')[2])
            # supports & againsts
            total_agree = response.xpath('//*[@id="content"]/div/div[1]/div[1]/div[' + str(i + 1) + ']/div[2]/div[1]/div[1]/span/text()').extract()[0].split('/')[-1]
            total_agree_m_against = response.xpath('//*[@id="content"]/div/div[1]/div[1]/div[' + str(i + 1) + ']/div[2]/div[1]/div[1]/span/text()').extract()[0].split('/')[0]
            supports = string.atoi(total_agree)
            againsts = supports - string.atoi(total_agree_m_against)
            print supports
            print againsts
            # response
            num_responses = 0
            total_responses = response.xpath('//*[@id="content"]/div/div[1]/div[1]/div[' + str(i + 1) + ']/div[2]/div[1]/div[1]/a/text()').extract()
            if (len(total_responses) > 0):
                num_responses = string.atoi(re.findall("\d+", total_responses[0])[0])
            print "responses:"
            print num_responses
        # next page
        nextpage_href = response.xpath('//*[@id="paginator"]/a/@href').extract()
        len_list = len(nextpage_href)
        if (len_list == 1 or len_list == 3):
            nextpage_url = response.url.split("?")[0] + nextpage_href[len_list - 1]
            nextpage = scrapy.http.Request(nextpage_url, callback=self.parse_page)
            yield nextpage
        else:
            return
