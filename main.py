# coding=utf-8
import feedparser
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log
#from cw_amazone.spiders.book_spider import BookSpider
from amazone.spiders.comment_spider import CommentSpider

def setup_crawler(domain, spidername):
    spider_class = globals()[spidername]
    spider = spider_class(domain=domain)
    crawler = Crawler(Settings())
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
#setup_crawler("amazone.com","BookSpider");

python_wiki_rss_url = "http://www.amazon.cn/gp/rss/bestsellers/books/658409051/ref=zg_bs_658409051_rsslink"
#"http://www.amazon.cn/%E5%B0%91%E5%84%BF%E5%9B%BE%E4%B9%A6/b/ref=sa_menu_books_l2_b658409051?ie=UTF8&node=658409051",

feed = feedparser.parse( python_wiki_rss_url)

surl = [];
for item in feed['items']:
    #print item['title']+'\n';
        print item['link']+'\n';
        ids =item['guid'].split('_');
        print ids;
        #大属性节点的标识（比如top3儿童）
#	print ids[2];
        #亚马逊商品的唯一ID
	
#        surl.append("http://www.amazon.cn/product-reviews/"+ids[3]+"/ref=cm_cr_pr_top_link_1?ie=UTF8&pageNumber=1&showViewpoints=0&sortBy=byRankDescending");
        print surl;
        spider = CommentSpider(domain="amazone.com",itemid=ids[3])
        #spider.start_urls = surl;
        crawler = Crawler(Settings())
        crawler.configure()
        crawler.crawl(spider)
        crawler.start()
log.start()
reactor.run() # the script will block here

#print surl;
#spider = CommentSpider(domain="amazone.com")
#spider.start_urls = surl;
#crawler = Crawler(Settings())
#crawler.configure()
#crawler.crawl(spider)
#crawler.start()
#log.start()
#reactor.run() # the script will block here
