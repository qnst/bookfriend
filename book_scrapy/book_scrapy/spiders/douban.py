# -*- coding: utf-8 -*-
import re
from datetime import datetime
import book_scrapy
from book_scrapy.items import DoubanItem
from scrpay import Spider

from book_scrapy import pipelines


class DoubanSpiderBase(Spider):
    allowed_domains = ["douban.com"]
    dr = re.compile(r'<[^>]+>|[\n\s\r]', re.S)

    # 提取小组url中的编号
    def get_group_id(self, url):
        # https://www.douban.com/group/26926/
        m = re.search("^https://www.douban.com/group/([^/]+)/$", url)
        if(m):
            return m.group(1)
        else:
            return 0

    # 提取帖子url中的编号
    def get_topic_id(self, url):
        # https://www.douban.com/group/topic/84606345/
        m = re.search("^https://www.douban.com/group/topic/([^/]+)/$", url)
        if(m):
            return m.group(1)
        else:
            return 0

    # 提取成员url中的编号
    def get_member_id(self, url):
        # https://www.douban.com/people/143391663/
        m = re.search("^https://www.douban.com/people/([^/]+)/$", url)
        if(m):
            return m.group(1)
        else:
            return 0

    # 保存到电脑
    def save_to_compute(self, response):
        # print self.get_title(response)
        filename = 'douban.html'
        self.log(filename)
        with open(filename, 'wb') as f:
            f.write(response.body)

    # 获取当前页面的title
    def get_title(self, response):
        return response.xpath('/html/head/title/text()').extract()[0]

    # rules = [
    #     # 如下规则会处理URL以/group/XXXX/为后缀的网页，调用parse_group_home_page为处理函数
    #     Rule(SgmlLinkExtractor(allow=('/group/[^/]+/$', )), callback='parse_group_home_page', process_request='add_cookie'),
    #     # 如下规则会抓取网页内容，并自动抓取网页中链接供下一步抓取，但不会处理网页的其他内容。
    #     Rule(SgmlLinkExtractor(allow=('/group/explore\?tag', )), follow=True, process_request='add_cookie'),
    # ]


class ZufangSpider(DoubanSpiderBase):
    name = "zufang"
    pipeline = [pipelines.MongodbStorePipeline]
    page_no = 1  # 当前页码
    page_count = 3  # 抓取多少页
    start_urls = (  # 超过一万人的租房小组
        'https://www.douban.com/group/beijingzufang/',  # 北京租房
        'https://www.douban.com/group/26926/',  # 北京租房豆瓣
        'https://www.douban.com/group/zhufang/',  # 北京无中介租房（寻天使投资合作）
        'https://www.douban.com/group/279962/',  # 北京租房（非中介）
        'https://www.douban.com/group/sweethome/',  # 北京租房（密探）
        'https://www.douban.com/group/257523/',  # 北京租房房东联盟(中介勿扰)
        'https://www.douban.com/group/cbdrent/',  # 北京CBD租房
        'https://www.douban.com/group/opking/',  # 北京个人租房
        'https://www.douban.com/group/276176/',  # 北京出租房（请自觉统一标题格式）
    )

    def parse(self, response):
        url = response.url
        group_id = self.get_group_id(url)

        trs = response.xpath('//table[@class="olt"]/tr')
        for tr in trs[2:]:
            topic_url = tr.xpath('td[@class="title"]/a/@href').extract()[0]
            author_url = tr.xpath('td[@nowrap="nowrap"]/a/@href').extract()[0]

            item = DoubanItem()
            item['title'] = tr.xpath('td[@class="title"]/a/@title').extract()[0]
            item['href'] = topic_url
            item['topic_id'] = self.get_topic_id(topic_url)
            item['group_id'] = group_id
            item['author_id'] = self.get_member_id(author_url)
            item['author_name'] = tr.xpath('td[@nowrap="nowrap"]/a/text()').extract()[0]

            tmp_list = tr.xpath('td[@nowrap="nowrap"]/text()').extract()
            if len(tmp_list) == 2:
                item['answer_count'] = tmp_list[0]
                item['last_answer_time'] = tmp_list[1]
            else:
                item['last_answer_time'] = tmp_list[0]

            item['scrapy_at'] = datetime.now()
            yield book_scrapy.Request(item['href'], self.parse_item, meta={'item': item})

        # 翻页  https://www.douban.com/group/26926/discussion?start=25
        if self.page_no < self.page_count:
            self.page_no += 1
            start = self.page_no*25
            next_page = '%sdiscussion?start=%s' % (url, start)
            self.log('xxxx%sxxx' % self.page_no)
            self.log(next_page)
            yield book_scrapy.Request(next_page, self.parse)

    # 帖子详细页
    def parse_item(self, response):
        item = response.meta['item']
        #  分析详情页面能够获取的数据
        html_content = response.xpath('//div[@class="topic-content"]').extract()[0]
        if isinstance(html_content, unicode):
            html_content.encode('utf-8')
        # content = self.dr.sub('', html_content)
        
        from lxml import etree, html
        content = html.document_fromstring(html_content).text_content()
        # print content

        item['content'] = content
        return item


class BookSpider(DoubanSpiderBase):
    name = "book"
    pipelines = [pipelines.SqliteStorePipeLine]