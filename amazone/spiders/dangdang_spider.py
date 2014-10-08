# -*- coding=UTF-8 -*-
import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
import json
import codecs,sys
import uuid
#reload(sys)
#sys.setdefaultencoding('utf-6')
class CommentSpider(scrapy.Spider):
	name = "dangdang"
	allowed_domains = ["dangdang.com"]
        start_urls = ["http://category.dangdang.com/cp01.41.41.00.00.00.html"]
	savefile=''	

	def __init__(self, domain=None):
		#super(MySpider, self).__init__(*args, **kwargs)
                filename = str(uuid.uuid1())
                print filename;
		self.savefile = codecs.open(filename,'w','utf-8')

	def parse(self, response):
		urls=response.xpath('//li[contains(@class,"line")]/div/a/@href').extract();	
                #print urls;
                #for url in urls:
                #    print url
		yield Request(urls[0], callback=self.parseBook,dont_filter=True)

	def parseBook(self, response):
                name = response.css("div[name=Title_pub] h1::text").extract()[0]
                print name;
                dangdangprice = response.css('b.d_price span::text').extract()[0];
                print dangdangprice
                mprice = response.css('span#originalPriceTag::text').extract()[0];
                print mprice;
                basicinfo = response.css('div.book_messbox div.show_info_right::text').extract();
                print basicinfo
                for b in basicinfo:
                    print b;
                #pub = basicinfo[1];
                #print 'pub'+str(pub);
                #pubtime= basicinfo[2];
                #print 'pubtime'+str(pubtime); 
                #isbn= basicinfo[3];
                #print 'isbn'+str(isbn);
                abstract = response.css('span#abstract_all').extract()[0];
                print abstract
		authorintro =response.xpath('//div[contains(@id,"authorintro")]/div[contains(@class,"descrip")]').extract()
                print authorintro
                mediafeedback = response.css('span#mediafeedback_all').extract()[0];
                print mediafeedback;
		#json.dump({"title": titles[num],"time": times[num],"author": authors[num],"star": stars[num][-4],"text": texts[num]}, self.savefile,ensure_ascii=False)


