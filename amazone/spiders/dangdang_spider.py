# -*- coding=UTF-8 -*-
import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
import json
import codecs,sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
class CommentSpider(scrapy.Spider):
	name = "dangdang"
	allowed_domains = ["dangdang.com"]
	start_urls = []
	itemid =''
	savefile=''	

	def __init__(self, itemid='', domain=None):
		#super(MySpider, self).__init__(*args, **kwargs)
		self.itemid = itemid
		self.start_urls = [""]
		self.savefile = codecs.open(itemid,'w','utf-8')

	def parse(self, response):
		result = [];
		page=response.xpath('//li[contains(@class,"line")]/a/text()').extract();	
                if len(page) == 0:
                    page = 1
                else:
                    page=int(page[0])
                print 'page:'+str(page);
                if page > 100:
                    page=50
		for p in range(1,page):
			url = "http://www.amazon.cn/product-reviews/"+self.itemid+"/ref=cm_cr_pr_top_link_"+str(p)+"?ie=UTF8&pageNumber="+str(p)+"&showViewpoints=0&sortBy=byRankDescending"
			print url;
			yield Request(url, callback=self.parseComment,dont_filter=True)

	def parseComment(self, response):
		print 'parseComment';
		titles =response.xpath('//span[contains(@style,"vertical-align:middle;")]/b/text()').extract()
		times =response.xpath('//span[contains(@style,"vertical-align:middle;")]/nobr/text()').extract()
		authors=response.xpath('//a[contains(@href,"http://profile.amazon.cn/gp/pdp/profile")]/span/text()').extract()
		stars=response.css('span[class*=s_star_]').xpath('./@class').extract()
		texts=response.css('.reviewText').xpath('./text()').extract()
		for num in range(0,len(titles)): 
			json.dump({"title": titles[num],"time": times[num],"author": authors[num],"star": stars[num][-4],"text": texts[num]}, self.savefile,ensure_ascii=False)


