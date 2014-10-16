# -*- coding=UTF-8 -*-
import scrapy
from scrapy.xlib.pydispatch import dispatcher
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
from scrapy.signalmanager  import SignalManager
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
	cur = ''
	def __init__(self,domain=None):
		self.con = mdb.connect('localhost', 'root', 'admin', 'huiben');
		self.cur=self.con.cursor()
		self.start_urls = ["http://www.amazon.cn/s?ie=UTF8&page=1&rh=n%3A658409051%2Cp_n_fulfilled_by_amazon%3A326314071"]
		filename = str(uuid.uuid1());
		print filename;
		self.savefile = codecs.open(filename,'w','utf-8')
		SignalManager(dispatcher.Any).connect(self.closed_handler, signal=scrapy.signals.spider_closed);
                
	def closed_handler(self, spider):
		print "close spider";
		self.savefile .close();
		self.cur.close();
		self.con.close();
	
				
	def parse(self, response):
		title=response.xpath('//div[contains(@class,"productTitle")]/a/@href').extract()
		for t in title:
			ridx = t.rfind('/')+1;
			aid = t[ridx:]
			#print aid
			#print ridx;
			#url = t[:ridx]+"/"+aid;
			url = 'http://www.amazon.cn/%E5%9B%BE%E4%B9%A6/dp/'+aid
			#print url;			
			yield Request(url, callback=self.parseBook,dont_filter=True,meta={"aid":aid,'url': t[:ridx]})
			
	def parseBook(self,response):
		name = ''.join(response.css('span[id=btAsinTitle] span::text').extract()).strip(' \t\n\r')
		print name
		listprice= response.css('span[id=listPriceValue]::text').extract()[0][2:]
		print listprice
		price= response.css('span[id=actualPriceValue] b::text').extract()[0][2:]
		print price
		detail = response.css('td.bucket div.content ul li::text').extract()
		print detail
		#self.savefile.write(''.join(detail));
		pub = detail[0]
		print pub
		pages = detail[1]
		print pages
		readerage =explode(detail[2][-1],'-')
		reader_age_from = readerage[0]
		print reader_age_from
		reader_age_to = readerage[1]
		print reader_age_to
		lang = detail[3]
		print lang
		pagesize = detail[4]
		isbn = detail[5]
		size = detail[6]
		rank = detail[11]
		aid = response.meta['aid']
		url= response.meta['url']+"product-description/"+aid
		print url
		sql = 'insert into amazone_book(id,name,realprice,price,\
			reader_age_from,reader_age_to,pub,\
			page,lang,isbn,rank,size,pagesize,\
			content,) \
			values(\''+aid+'\',\''+name+'\','+listprice+','+price+','+reader_age_from+','\
				+reader_age_to+',\''+pub+'\','+page+',\''+lang+'\',\''+isbn+'\','+rank
		yield Request(url, callback=self.parseBookDescription,dont_filter=True,meta={"aid":aid})

	def parseBookDescription(self, response):
		aid = response.meta['aid']
		name = ''.join(response.css('span[id=btAsinTitle] span::text').extract()).strip(' \t\n\r')
		print name
		listprice= response.css('span[id=listPriceValue]::text').extract()[0][2:]
		print listprice
		price= response.css('span[id=actualPriceValue] b::text').extract()[0][2:]
		print price
		content =response.css('div[class=content]').extract()[0].replace('\'','"').strip(' \t\n\r')
		#print content;
		sql = 'insert into amazone_book values(\''+aid+'\',\''+name+'\','+listprice+','+price+',\''+content+'\')'
		self.savefile.write(sql);
		#self.cur.execute(sql)


