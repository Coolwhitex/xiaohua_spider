# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import os
import urllib.request


class XiaohuaSpiderPipeline(object):
    def __init__(self):
        self.con = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='123456',
            db='xiaohua'
        )
        self.cursor = self.con.cursor()
        self.create_table()

    # 连接数据库
    def connect(self):
        self.con = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='123456',
            db='xiaohua'
        )
        self.cursor = self.con.cursor()

    # 关闭数据库    
    def close(self):
        self.con.commit()
        self.cursor.close()
        self.con.close()

    # 创建表
    def create_table(self):
        self.connect()
        # name, age, cons, specialty, school, prof
        sql = "CREATE TABLE IF NOT EXISTS xiaohua (id INTEGER PRIMARY KEY auto_increment, name VARCHAR(20), age VARCHAR (20), cons VARCHAR (20), spicialty VARCHAR (50), school VARCHAR (50), prof VARCHAR (20))"
        self.cursor.execute(sql)
        self.close()

    # 存数据库
    def process_item(self, item, spider):
        self.connect()
        # 检测要爬取的数据是否存在数据库
        try:
            sql1 = """SELECT id FROM xiaohua WHERE xiaohua.xiaohua.name='{}'""".format(item['name'])
            self.cursor.execute(sql1)
        except Exception as e:
            print(e)
            return
        res = self.cursor.fetchall()
        if res:
            print('数据已存在')
            return
        else:
            try:
                sql = """INSERT INTO xiaohua(name, age, cons, spicialty, school, prof) VALUES ('{}','{}','{}', '{}', '{}', '{}')""".format(item['name'], item['age'], item['cons'], item['specialty'], item['school'], item['prof'])
                self.cursor.execute(sql)
            except Exception as e:
                print(e)
                return
            finally:
                self.close()
                print(f"{item['name']}的信息存储完毕")


# 保存图片
class SaveImgPipeline(object):
    def process_item(self, item, spider):
        # 一个大型项目中间可能有多个spider和多个pipline，判断一下确保item进入对应的pipline中
        if spider.name == 'xiaohua':
            # print(item['title'], item['img_name'], item['img_url'])
            # 创建文件夹
            base_dir = os.path.join(os.path.dirname(__file__),'images')     # 项目根目录
            img_dir = os.path.join(base_dir, item['title'])         # 携带图集名路径
            if not os.path.exists(img_dir):
                os.makedirs(img_dir)   # 可以一次创建多层路径
            name = item['img_name']
            print(name)
            img_path = os.path.join(img_dir, name)      # 携带图片名的路径
            # 请求和保存图片
            img_url = item['img_url']
            if 'http' in img_url:
                url = img_url
            else:
                url = 'http://www.xiaohuar.com' + img_url
            urllib.request.urlretrieve(url, img_path)
            print(f'{url}下载成功')

