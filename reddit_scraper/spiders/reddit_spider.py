from collections import defaultdict
from unidecode import unidecode

import scrapy
import urlparse
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from reddit_scraper.items import RedditItem



class RedditSpider(scrapy.Spider):
    name = "reddit"
    allowed_domains = ["reddit.com"]
    start_urls = [
        "https://www.reddit.com/r/all/rising/"
    ]

    global sub_freq 
    sub_freq = defaultdict(int)


    def __init__(self):
        dispatcher.connect(self.close_spider, signals.spider_closed)

    def close_spider(self, spider):
        global sub_freq
        subs_with_one_post = 0
        one_post_subs = []

        data_top = ""

        f = open('r_all_rising.what', 'wb')
        for sub, freq in sorted(sub_freq.iteritems(),key=lambda (k,v): v,reverse=True):
            if freq == 1:
                one_post_subs.append(sub)
            else:
                data_top += str(unidecode(sub[3:])) + " "
                data_top += str('{:.0%}'.format(freq/25.0)) + "\n"

        f.write(data_top)

        if len(one_post_subs) > 0:
            data_one_posts = str(len(one_post_subs)) + " subs w 4%"
            data_incl = " incl:\n"
            f.write(data_one_posts)
            current_len = len(data_top) + len(data_one_posts) + len(data_incl)
            data = ""
            for sub in one_post_subs:
                current_data = str(unidecode(sub[3:])) + "\n"
                current_len += len(current_data)
                if(current_len <= 140):
                    data += current_data

            if data:
                f.write(data_incl)
                f.write(data)

        f.close()

    def parse(self, response):
        global sub_freq
        for sel in response.xpath('//div[@class="content"]/div/div[@id="siteTable"]/div[contains(@onclick,"click_thing(this)")]'):
            item = RedditItem()
            item['rank'] = sel.xpath('span[@class="rank"]/text()').extract()
            item['subreddit'] = sel.xpath('div[2]/p[2]/a[2]/text()').extract()
            item['num_comments'] = sel.xpath('div[2]/ul/li[@class="first"]/a/text()').extract()
            #TODO should be able to get sub w/o for in loop
            for sub in item['subreddit']:
                sub_freq[sub] += 1

            yield item

        #this code is for going to next page & scraping there
        #next_page = response.xpath('//div[@class="content"]/div/div[@id="siteTable"]/div[51]/span[1]/span[@class="next-button"]/a/@href').extract()[0]
        #43 is  len of "https://www.reddit.com/r/all/rising/?count="
        #page_num = int(next_page[43:next_page.index("&")])
        #if next_page and page_num < 50:
        #    yield scrapy.Request(next_page, self.parse)
