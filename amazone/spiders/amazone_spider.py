# -*- coding=UTF-8 -*-
import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.http import Request
import json
import codecs,sys
import MySQLdb as mdb
import sys


#reload(sys)
#sys.setdefaultencoding('utf-8')
class AmazoneSpider(scrapy.Spider):
        name = "amazone"
        allowed_domains = ["amazone.cn"]
        start_urls = []
        itemid =''
        savefile=''	
        con = ''
        def __init__(self, itemid='', domain=None):
                self.con = mdb.connect('localhost', 'root', 'admin', 'huiben');
                self.itemid = itemid
                self.start_urls = ["http://www.amazon.cn/product-reviews/"+itemid+"/ref=cm_cr_dp_see_all_top?ie=UTF8&showViewpoints=1&sortBy=byRankDescending"]
                self.savefile = codecs.open(itemid,'w','utf-8')

        def parse(self, response):
            result = [];
                page=response.xpath('//span[contains(@class,"paging")]/a[last()-1]/text()').extract();	
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
                try:
                   cur = con.cursor()
                   cur.execute("insert into books(amazoneid,name,) values()")

                except mdb.Error, e:
                    print "Error %d: %s" % (e.args[0],e.args[1])
                            sys.exit(1)

                finally:    
                    if con:    
                        con.close()
                print 'parseComment';
                titles =response.xpath('//span[contains(@style,"vertical-align:middle;")]/b/text()').extract()
                times =response.xpath('//span[contains(@style,"vertical-align:middle;")]/nobr/text()').extract()
                authors=response.xpath('//a[contains(@href,"http://profile.amazon.cn/gp/pdp/profile")]/span/text()').extract()
                stars=response.css('span[class*=s_star_]').xpath('./@class').extract()
                texts=response.css('.reviewText').xpath('./text()').extract()
                for num in range(0,len(titles)): 
                    json.dump({"title": titles[num],"time": times[num],"author": authors[num],"star": stars[num][-4],"text": texts[num]}, self.savefile,ensure_ascii=False)


