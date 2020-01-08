"""
   名称：智联招聘职业数据分析

   简介：https://fe-api.zhaopin.com/c/i/sou?start=0&pageSize=90&cityId=765&kw=爬虫&kt=3
        1.start=0
            为页数,一页90个数据,0`89
        2.pageSize=90
            这个不用变,90就好
        3.cityId=765
            城市的id,可以换这个id获取不同城市的职业信息
        4.kw=爬虫
            想要爬取的职业
        5.  kt=3
            这个不用变,3就好
"""
import json
import random
import re
import time

import pymysql
import requests
from fake_useragent import UserAgent
from pandas.io.sql import table_exists

from cityID import City
from proxy import Proxy_ip

# 文字转换拼音
from pypinyin import lazy_pinyin


class Zlspider():
    def __init__(self):
        self.url = "https://fe-api.zhaopin.com/c/i/sou?"
        self.headers = {
            'User-Agent': UserAgent().chrome,
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://sou.zhaopin.com'
        }
        self.jobName = None
        self.db = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='zhilian',
            charset='utf8'
        )
        self.cur = self.db.cursor()
        self.num = 0

    def get_html(self, start, cityId, kw):
        data = {
            'start': start,
            'pageSize': 90,
            'cityId': cityId,
            'kw': kw,
            'kt': '3'
        }
        name_list = lazy_pinyin(kw)
        name = ''
        for i in name_list:
            name += i
        self.jobName = name
        print(self.jobName)
        html = requests.get(self.url, headers=self.headers, params=data, proxies=self.http(), timeout=20)
        time.sleep(random.randint(1, 3))
        # 获取的元素为json字符串
        json_response = html.content.decode()
        # 转换为python字典
        dict_response = json.loads(json_response)
        print(dict_response)
        self.parse_data(dict_response)

    def parse_data(self, dict_response):
        # print('*' * 25 + dict_response['data']['results']['city']['display'] + '*' * 25)
        for i in dict_response['data']['results']:
            self.num += 1
            print(self.num)
            # 职位编号
            if i['number']:
                number = i['number']
            else:
                number = "无填写"
            # 职位名称
            if i['jobName']:
                jobName = i['jobName']
            else:
                jobName = "无填写"
            # 薪水
            if i['salary']:
                salary = i['salary']
            else:
                salary = "无填写"
            # 工作经验
            if 'workingExp' in i.keys():
                workingExp = i['workingExp']['name']
            else:
                workingExp = '无填写'
            # 学历要求
            if i['eduLevel']['name']:
                eduLevel = i['eduLevel']['name']
            else:
                eduLevel = "无填写"
            # 公司名称
            if i['company']['name']:
                company = i['company']['name']
            else:
                company = "无填写"
            # 公司类型(民营,外企,国企)
            if i['company']['type']['name']:
                type = i['company']['type']['name']
            else:
                type = "无填写"
            # 　公司地址：
            if i['city']['display']:
                city = i['city']['display']
            else:
                city = "无填写"
            # 招聘状态:
            if i['timeState']:
                timeState = i['timeState']
            else:
                timeState = "无填写"
            print(number, city, jobName, salary, workingExp, eduLevel, company, type, timeState)

            sql = "show tables;"
            self.cur.execute(sql)
            tables = [self.cur.fetchall()]
            table_list = re.findall('(\'.*?\')', str(tables))
            table_list = [re.sub("'", '', each) for each in table_list]
            print(table_list)

            if self.jobName not in table_list:
                print("%s数据库不存在,正在创建" % self.jobName)
                sql_createTb = "create table zhilian.%s(number varchar(50) not null primary key,city varchar(30) null,jobName varchar(50) null,salary varchar(20) null,workingExp varchar(20) null,edulevel varchar(10) null,company varchar(50) null,type varchar(10) null,timeState varchar(10) null) CHARACTER SET utf8 " % self.jobName
                print(sql_createTb)
                self.cur.execute(sql_createTb)
                self.db.commit()
                print("%s数据库创建成功,正在插入" % self.jobName)
                self.insert_sql(city, company, eduLevel, jobName, number, salary, timeState, type, workingExp)

            else:
                print("%s数据库已存在,正在插入" % self.jobName)
                self.insert_sql(city, company, eduLevel, jobName, number, salary, timeState, type, workingExp)

        # if table_exists(self.cur, self.jobName) != 1:
        #         print("%s数据库不存在,正在创建" % self.jobName)
        #         sql_createTb = "create table zhilian.%s(number varchar(50) not nullprimary key,city varchar(30) null,jobName varchar(50) null,salary varchar(20) null,workingExp varchar(20) null,edulevel varchar(10) null,company varchar(50) null,type varchar(10) null,timeState varchar(10) null)" % self.jobName
        #         self.cur.execute(sql_createTb)
        #         self.db.commit()
        #         print("%s数据库创建成功,正在插入" % self.jobName)
        #         self.insert_sql(city, company, eduLevel, jobName, number, salary, timeState, type, workingExp)
        # else:
        #     print("%s数据库已存在,正在插入" % self.jobName)
        #     self.insert_sql(city, company, eduLevel, jobName, number, salary, timeState, type, workingExp)

    def insert_sql(self, city, company, eduLevel, jobName, number, salary, timeState, type, workingExp):
        sel = r"select number from zhilian.%s where number ='%s'" % (self.jobName, number)
        print(sel)
        r = self.cur.execute(sel)
        if not r:
            print("正在插入数据库")
            ins = r"insert into zhilian.%s values ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                self.jobName, number, city, jobName, salary, workingExp, eduLevel, company, type, timeState)
            print(ins)
            self.cur.execute(ins)
            self.db.commit()
        else:
            print("数据库中已存在")

    def http(self):
        P = Proxy_ip()
        # proxies = P.get_ip()
        proxies = {'http': 'http://119.82.252.25:33573', 'https': 'https://51.15.94.201:3128'}
        print(proxies)
        return proxies

    def run(self):
        kw = input('请输入您要爬取的职业:')
        city = City()
        for c_id in city.con_code():
            for i in range(0, 181, 90):
                self.get_html(start=i, cityId=c_id, kw=kw)

        self.cur.close()
        self.db.close()


if __name__ == '__main__':
    zl = Zlspider()
    zl.run()
