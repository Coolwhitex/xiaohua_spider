# -*- coding: utf-8 -*-
import scrapy
import time
from xiaohua_spider.items import XiaohuaSpiderItem
from scrapy import Request


class XiaohuaSpider(scrapy.Spider):
    name = 'xiaohua'
    allowed_domains = ['xiaohuar.com']
    start_urls = ['http://www.xiaohuar.com/hua/']

    # 存放待爬取的url，scrapy会自动去重和重试失败链接，我们只需考虑忘url集合中添加为爬取的url
    # url_set = set()

    def parse(self, response):
        """
        请求首页图集列表之后得到列表页，解析获得详情页地址
        :param response:
        :return:
        """
        # 首先重写parse，否则父类会报Not Implement
        img_list = response.xpath('//*[@class="img"]/a/@href').extract()
        for href in img_list:
            # if href in self.url_set:
            #     print('链接已存在')
            #     continue
            # else:
                # self.url_set.add(href)
        # for link in self.url_set:
            yield Request(
                url=href,
                callback=self.parser_list
            )

        # 获取下一页
        for x in range(1, 11):
            url = f'http://www.xiaohuar.com/list-1-{x}.html'
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )

    def parser_list(self, response):
        """
        解析列表页，获取照片详情页链接
        :param response:
        :return:
        """
        # 标题
        title = response.xpath('//div[@class="div_h1"]/h1/text()').extract()[0]
        trs = response.xpath('//div[@class="infodiv"]/table/tbody/tr')
        # 姓名
        name = trs[0].xpath('./td[2]/text()').extract()[0]
        # 年龄
        age = trs[1].xpath('./td[2]/text()').extract()
        if len(age) == 0:
            age = '保密'
        else:
            age = age[0]
        # 星座
        cons = trs[2].xpath('./td[2]/text()').extract()
        if len(cons) == 0:
            cons = '保密'
        else:
            cons = cons[0]
        # 专业
        specialty = trs[3].xpath('./td[2]/text()').extract()
        if len(specialty) == 0:
            specialty = '保密'
        else:
            specialty = specialty[0]
        # 学校
        school = trs[4].xpath('./td[2]/text()').extract()
        if len(school) == 0:
            school = '保密'
        else:
            school = school[0]
        # 职业
        prof = trs[5].xpath('./td[2]/text()').extract()
        if len(prof) == 0:
            prof = '保密'
        else:
            prof = prof[0]

        # item = XiaohuaSpiderItem()
        # item['name'] = name
        # item['age'] = age
        # item['cons'] = cons
        # item['specialty'] = specialty
        # item['school'] = school
        # item['prof'] = prof
        # yield item

        link = response.xpath('//div[@class="post_entry"]/ul[@class="photo_ul"]/li/div/a/@href').extract()
        for href in link:
            pass
            # yield 相当于同步函数里的返回值，callback相当于方法嵌套调用，只不过这两个关键字表现异步处理过程。yield生成请求对象（还没有发送请求）到队列中，框架从队列里取一个对象去请求，得到相应后再交给回调函数处理。

            yield Request(
                url=href,
                callback=self.parse_detail,
                meta={'title': title}
            )

    def parse_detail(self, response):
        """
        解析照片详情页
        :return:
        """
        img_urls = response.xpath('//div[@class="pic_img_gallery ad-thumbs"]/ul/li/div/a/@href').extract()
        for img_url in img_urls:
            img_name = img_url.split('/')[-1]   # 哈希加密的照片名  20180902vVvfvLzZ50.jpg
            item = XiaohuaSpiderItem()
            item['img_url'] = img_url
            item['img_name'] = img_name
            item['title'] = response.meta.get('title')

            # print(item['title'])
            # print(img_url, img_name)
            yield item

