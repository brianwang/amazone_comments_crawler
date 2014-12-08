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
		name = ''.join(response.css('span[id=productTitle]::text').extract()).strip(' \t\n\r')
		print name
		auth = '@@'.join(response.css('div[id=byline] a::text').extract()).strip('\t\r\n');
		print auth
		pubtime = response.css('h1[id=title] span:nth-child(3) ::text').extract()[0][2:]
		print pubtime
		listprice= response.css('div[id=soldByThirdParty] span::text').extract()[0][1:]
		print listprice
		price= response.css('span[class="a-color-secondary a-text-strike"]::text').extract()[0][1:]
		print price
		titles = response.css('td.bucket div.content ul li b::text').extract()
		print titles
		detail1 = response.css('td.bucket div.content ul li::text').extract()
		print detail1
		detail ='@@'.join(detail1).replace('\n','').replace(u"\xa0",'').replace(' ','').replace('@@@@','@@').split('@@')
		print detail
		pub = detail[0]
		print pub
		if titles[2] == u'丛书名:':
			print '2 is cong shu ming'
			print '丛书名';
			pages = detail[3]
			readerage =detail[4][:-1].split('-')
			print readerage
			lang = detail[5]
			pagesize = detail[6]
			isbn = detail[7]
			size = detail[9]
			rank = detail[16]
			reader_age_from = readerage[0]
			reader_age_to = readerage[1]
		#self.savefile.write(''.join(detail));
		elif detail1[1] == u'\xa0' and detail1[2].find(u'岁') != -1:
			print '1 is sui'
			pages = '0y'
			readerage =detail[1][:-1].split('-')
			lang = detail[2]
			pagesize = detail[3]
			isbn = detail[4]
			size = detail[6]
			rank = detail[13]
		elif titles[1] == u'丛书名:':
			print '1 is cong shu ming'
			pages = detail[1]
			for i in range(0,len(detail)-1):
				print detail[i]		
			readerage =detail[2][:-1].split('-')
			print readerage
			lang = detail[3]
			pagesize = detail[4]
			isbn = detail[5]
			size = detail[7]
			rank = detail[14]
		else:
			pages = detail[1]
			#print detail[2][:-1];
			readerage =detail[2][:-1].split('-')
			lang = detail[3]
			pagesize = detail[4]
			isbn = detail[5]
			size = detail[7]
			rank = detail[14]
		try:
			reader_age_from = readerage[0]
			reader_age_to = readerage[1]
		except:
			print 'readerage error:'
			print readerage
			reader_age_to = 0
			reader_age_from = 0
		rank=rank[rank.find(u'第')+1:-2]
		print rank
		aid = response.meta['aid']
		url= response.meta['url']+"product-description/"+aid
		print url
		sql = 'insert into amazone_book(id,name,author,pubtime,realprice,price,\
			reader_age_from,reader_age_to,pub,\
			pages,lang,isbn,rank,size,pagesize,\
			content) \
			values(\''+aid+'\',\''+name+'\',\''+auth+'\',\''+pubtime+'\','+listprice+','+price+','+reader_age_from+','\
				+reader_age_to+',\''+pub+'\','+pages[:-1]+',\''+lang+'\',\''+isbn+'\',\''+rank\
				+'\',\''+size+'\','+str(pagesize)+',';
		yield Request(url, callback=self.parseBookDescription,dont_filter=True,meta={"aid":aid,'sql':sql})

	def parseBookDescription(self, response):
		aid = response.meta['aid']
		sql = response.meta['sql']
		content =response.css('div[class=content]').extract()[0].replace('\'','"').strip(' \t\n\r')
		sql += '\''+content+'\');';
		self.savefile.write(sql);
		#self.cur.execute(sql)


