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
                self.savefile.write(name)
                self.savefile.write('\n');                        
                dangdangprice = response.css('b.d_price span::text').extract()[0];
                self.savefile.write(dangdangprice)
                self.savefile.write('\n');   
                mprice = response.css('span#originalPriceTag::text').extract()[0];
                self.savefile.write(mprice);
                self.savefile.write('\n');   
                basicinfo = response.css('div.book_messbox div.show_info_right::text').extract();
#                self.savefile.write(basicinfo)
                for b in basicinfo:
                   self.savefile.write(b);
                   self.savefile.write('\n');
                #pub = basicinfo[1];
                #print 'pub'+str(pub);
                #pubtime= basicinfo[2];
                #print 'pubtime'+str(pubtime); 
                #isbn= basicinfo[3];
                #print 'isbn'+str(isbn);
		authorintro =response.xpath('//div[contains(@id,"authorintro")]/div[contains(@class,"descrip")]').extract()
                self.savefile.write(''.join(authorintro))
                self.savefile.write('\n')
                allinfo= response.css('textarea[style*="height:0px;border-width:0px"]').extract();
                for info in allinfo:
                    self.savefile.write(info);
                    self.savefile.write('\n');
                self.savefile.close()
		#json.dump({"title": titles[num],"time": times[num],"author": authors[num],"star": stars[num][-4],"text": texts[num]}, self.savefile,ensure_ascii=False)


