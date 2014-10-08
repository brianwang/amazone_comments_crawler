# -*- coding=UTF-8 -*-
import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
import json
import codecs,sys
import MySQLdb as mdb
import sys
import uuid
#reload(sys)
#sys.setdefaultencoding('utf-8')
class AmazoneSpider(scrapy.Spider):
        name = "amazone"
        allowed_domains = ["amazone.cn"]
        start_urls = []
        savefile=''	
        con = ''
        def __init__(self,domain=None):
                #self.con = mdb.connect('localhost', 'root', 'admin', 'huiben');
                self.start_urls = ["http://www.amazon.cn/s?ie=UTF8&page=1&rh=n%3A658409051%2Cp_n_fulfilled_by_amazon%3A326314071"]
                filename = str(uuid.uuid1());
                print filename;
		self.savefile = codecs.open(filename,'w','utf-8')

	def parse(self, response):
		 #title=response.css('div[id*=result_]').extract()
		 #print title;
		 #title=response.css('.newaps').extract()
		 #title=response.xpath('//div[contains(@id,"result_")]').extract()
		 title=response.xpath('//div[contains(@class,"productTitle")]/a/@href').extract()
		 for t in title:
			ridx = t.rfind('/');
			aid = t[ridx:]
			#print aid
			#print ridx;
			url= t[:ridx]+"/product-description"+aid
			#print url;
			yield Request(url, callback=self.parseBook,dont_filter=True)
#		page=response.xpath('//span[contains(@class,"paging")]/a[last()-1]/text()').extract();	
#		page =1
	#	for p in range(1,page):
		#	url = "http://www.amazon.cn/s/ref=lp_658409051_pg_"+str(p)+"?rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658409051&page="+str(p)+"&ie=UTF8&qid=1412177207"
			#print url;
			#yield Request(url, callback=self.parseBook,dont_filter=True)

	def parseBook(self, response):
		name = ''.join(response.css('span[id=btAsinTitle] span::text').extract()).strip(' \t\n\r')
		print name
		listprice= response.css('span[id=listPriceValue]::text').extract()[0][2:]
		print listprice
		price= response.css('span[id=actualPriceValue] b::text').extract()[0][2:]
		print price
		content =response.css('div[class=content]').extract()[0].replace('\'','"').strip(' \t\n\r')
		#print content;
		sql = 'insert into aaa values(\''+name+'\','+listprice+','+price+',\''+content+'\')'
		self.savefile.write(sql);
		


