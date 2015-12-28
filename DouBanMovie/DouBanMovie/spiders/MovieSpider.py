# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.utils.url import urljoin_rfc
from DouBanMovie.items import DoubanmovieItem, CommentElem, TimeRecord

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
import csv

reload(sys)
sys.setdefaultencoding('utf-8')

def OutPutToJSON(mydata):
    # filename
    filefulldirname = 'data/' + mydata['filename'] + '.json'
    # specify json data
    datalist = []
    for elem in mydata['datalist']:
        new_elem = {'title': elem['title'], 'pageurl': elem['pageurl'], 'score': elem['score'], 'support': elem['support'], 'against': elem['against'], 'replyno': elem['replyno'], 'timerec': {'year': elem['timerec']['year'], 'month': elem['timerec']['month'], 'day': elem['timerec']['day'], 'hour': elem['timerec']['hour'], 'minute': elem['timerec']['minute'], 'second': elem['timerec']['second']}}
        datalist.append(new_elem)
    jsondata = {'filename': mydata['filename'], 'title': mydata['title'], 'pageurl': mydata['pageurl'], 'total' : mydata['total'], 'cnt5': mydata['cnt5'], 'cnt4': mydata['cnt4'], 'cnt3': mydata['cnt3'], 'cnt2': mydata['cnt2'], 'cnt1': mydata['cnt1'], 'datalist': datalist}
    # write
    with codecs.open(filefulldirname,'wb','utf-8') as f:
        f.write(json.dumps(jsondata, ensure_ascii=False))
    f.close()

# there is decoding bug when decoding Chinese characters
def OutPutToCSV(mydata):
    # filename
    filefulldirname = 'data/' + mydata['filename'] + '.csv'
    # write
    with open(filefulldirname, 'wb') as csvfile:
        csvfile.write(codecs.BOM_UTF8) 
        spamwriter = csv.writer(csvfile, dialect = 'excel')
        spamwriter.writerow(['pageurl', 'score', 'support', 'against', 'replyno', 'year', 'month', 'day', 'hour', 'minute', 'second'])
        for elem in mydata['datalist']:
            spamwriter.writerow([elem['pageurl'], elem['score'], elem['support'], elem['against'], elem['replyno'], elem['timerec']['year'], elem['timerec']['month'], elem['timerec']['day'], elem['timerec']['hour'], elem['timerec']['minute'], elem['timerec']['second']])
    csvfile.close()
    '''
    # test
    with open('data/egg2.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile,dialect='excel')
        spamwriter.writerow(['a', '1', '1', '2', '2'])
        spamwriter.writerow(['b', '3', '3', '6', '4'])
        spamwriter.writerow(['c', '7', '7', '10', '4'])
        spamwriter.writerow(['d', '11','11','11', '1'])
        spamwriter.writerow(['e', '12','12','14', '3'])
    '''

class MoviespiderSpider(scrapy.Spider):
    name = "MovieSpider"
    #allowed_domains = ["http://movie.douban.com/"]
    start_urls = (
        #'http://www.http://movie.douban.com//',
        #'http://movie.douban.com/subject/26320029/reviews?start=0&filter=&limit=20', # 万万没想到
        #'http://movie.douban.com/subject/20376577/reviews?start=0&filter=&limit=20', # 小时代
        #'http://movie.douban.com/subject/24721493/reviews?start=0&filter=&limit=20', # 小时代2
        #'http://movie.douban.com/subject/24847340/reviews?start=0&filter=&limit=20', # 小时代3
        #'http://movie.douban.com/subject/24847343/reviews?start=0&filter=&limit=20', # 小时代4
        #'http://movie.douban.com/subject/25907063/reviews?start=0&filter=&limit=20', # 盗墓笔记
        #'http://movie.douban.com/subject/24827406/reviews?start=0&filter=&limit=20', # 鬼吹灯 九层妖塔
        #'http://movie.douban.com/subject/3077412/reviews?start=0&filter=&limit=20', # 鬼吹灯 寻龙诀
        #'http://movie.douban.com/subject/25710912/reviews?start=0&filter=&limit=20', # 港囧
        #'http://movie.douban.com/subject/25964071/reviews?start=0&filter=&limit=20', # 夏洛特烦恼
        #'http://movie.douban.com/subject/1292052/reviews?start=0&filter=&limit=20', # 肖申克的救赎
        #'http://movie.douban.com/subject/1291546/reviews?start=0&filter=&limit=20', # 霸王别姬
        #'http://movie.douban.com/subject/1292063/reviews?start=0&filter=&limit=20', # 美丽人生
        #'http://movie.douban.com/subject/25745752/reviews?start=0&filter=&limit=20', # 左耳
        #'http://movie.douban.com/subject/26366465/reviews?start=0&filter=&limit=20', # 我的少女时代
        #'http://movie.douban.com/subject/20326665/reviews?start=0&filter=&limit=20', # 星球大战 原力觉醒
        "http://movie.douban.com/subject/1309078/reviews", # 星球大战 前传3 #没有2星
    )

    def parse(self, response):
        # page title
        movie = response.xpath('//*[@id="content"]/h1/text()').extract()[0]
        print movie
        #raw_input("")
        # overall level
        num0 = re.findall("\d+", response.xpath('//*[@id="content"]/div/div[2]/div[1]/ul/li[1]/a/span/text()').extract()[0])[-1]
        num5 = re.findall("\d+", response.xpath('//*[@id="content"]/div/div[2]/div[1]/ul/li[2]/a/span/text()').extract()[0])[-1]
        num4 = re.findall("\d+", response.xpath('//*[@id="content"]/div/div[2]/div[1]/ul/li[3]/a/span/text()').extract()[0])[-1]
        num3 = re.findall("\d+", response.xpath('//*[@id="content"]/div/div[2]/div[1]/ul/li[4]/a/span/text()').extract()[0])[-1]
        #num2 = re.findall("\d+", response.xpath('//*[@id="content"]/div/div[2]/div[1]/ul/li[5]/a/span/text()').extract()[0])[-1]
        #num1 = re.findall("\d+", response.xpath('//*[@id="content"]/div/div[2]/div[1]/ul/li[6]/a/span/text()').extract()[0])[-1]
        num1 = re.findall("\d+", response.xpath('//*[@id="content"]/div/div[2]/div[1]/ul/li[5]/a/span/text()').extract()[0])[-1]
        print num0
        print num1
        # item definition
        moviedata = DoubanmovieItem()
        moviedata['filename'] = response.url.split('/')[4] # 26320029
        moviedata['title'] = movie
        moviedata['pageurl'] = response.url
        moviedata['total'] = num0
        moviedata['cnt5'] = num5
        moviedata['cnt4'] = num4
        moviedata['cnt3'] = num3
        #moviedata['cnt2'] = num2
        moviedata['cnt2'] = 0
        moviedata['cnt1'] = num1
        data_list = [] # data_elem = CommentElem()
        moviedata['datalist'] = data_list
        # requests
        parser = scrapy.http.Request(response.url, callback=self.parse_page)
        parser.meta['MovieData'] = moviedata
        yield parser

    def parse_page(self, response):
        endflag = 0 # if to stop (往后都是折叠问题)
        # inherite data
        moviedata = response.meta['MovieData']
        # parse a page
        print response.url
        # raw_input("debug:" + response.url)
        # list of comments
        response_content = response.xpath('//*[@id="content"]/div/div[1]/div[1]/div').extract()
        # raw_input("debug: list length%d\n" % len(response_content))
        # for each comment
        for i in range(len(response_content)):
            # title
            comment_title_cand = response.xpath('//*[@id="content"]/div/div[1]/div[1]/div[' + str(i + 1) + ']/div[1]/h3/a[2]/@title').extract()
            if (len(comment_title_cand) > 0):
                comment_title = comment_title_cand[0]
            else:
                comment_title = "null"
                endflag = 1
            # raw_input("debug: ")
            # print comment_title
            # if end
            if endflag==1:
                raw_input("finished %s; press any key to continue" %moviedata['pageurl'])
                OutPutToJSON(mydata=moviedata)
                OutPutToCSV(mydata=moviedata)
            # urls
            comment_url = response.xpath('//*[@id="content"]/div/div[1]/div[1]/div[' + str(i + 1) + ']/div[1]/h3/a[2]/@href').extract()[0]
            # user_url = response.xpath('//*[@id="content"]/div/div[1]/div[1]/div[' + str(i + 1) + ']/div[1]/div/a/@href').extract()[0]
            # raw_input("debug: ")
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
            # put item into data list
            new_comment = CommentElem()
            new_comment['title'] = comment_title
            new_comment['pageurl'] = comment_url
            # new_comment['userurl'] = user_url
            new_comment['score'] = stars_score
            new_comment['support'] = supports
            new_comment['against'] = againsts
            new_comment['replyno'] = num_responses
            new_comment['timerec'] = TimeRecord()
            new_comment['timerec']['year'] = year
            new_comment['timerec']['month'] = month
            new_comment['timerec']['day'] = day
            new_comment['timerec']['hour'] = hour
            new_comment['timerec']['minute'] = minute
            new_comment['timerec']['second'] = second
            moviedata['datalist'].append(new_comment)
            #print new_comment
            #raw_input("pause for debug")
        # next page
        nextpage_href = response.xpath('//*[@id="paginator"]/a/@href').extract()
        len_list = len(nextpage_href)
        if (len_list == 1 or len_list == 3):
            nextpage_url = response.url.split("?")[0] + nextpage_href[len_list - 1]
            nextpage = scrapy.http.Request(nextpage_url, callback=self.parse_page)
            nextpage.meta['MovieData'] = moviedata
            yield nextpage
        else:
            raw_input("finished %s; press any key to continue" %unicode(moviedata['title']))
            OutPutToJSON(mydata=moviedata)
            OutPutToCSV(mydata=moviedata)
        