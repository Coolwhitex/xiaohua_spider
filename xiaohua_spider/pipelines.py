# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


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
        try:
            sql = """INSERT INTO xiaohua(name, age, cons, spicialty, school, prof) VALUES ('{}','{}','{}', '{}', '{}', '{}')""".format(item['name'], item['age'], item['cons'], item['specialty'], item['school'], item['prof'])
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
            return
        finally:
            self.close()
