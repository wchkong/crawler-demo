# -*- coding:utf-8 -*-
import re
import os
import requests
from lxml import html
from urllib import parse
import csv
import xlrd
from copy import copy

# 搜索关键字，这里只爬取了数据挖掘的数据，读者可以更换关键字爬取其他行业数据
city = {"北京": '010000',
        "上海": '020000',
        "广州": '030200',
        "深圳": '040000',
        "成都": '090200', }
#北京 010000
#上海 020000
#广州 030200
#深圳 040000
#成都 090200

# 伪装爬取头部，以防止被网站禁止
headers = {'Host': 'search.51job.com',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)\
         Chrome/63.0.3239.132 Safari/537.36'}


# 获取职位详细页面
def get_links(page, city_code, key):
    url = 'http://search.51job.com/list/'+ str(city_code) +',000000,0000,00,9,99,' + key + ',2,' + str(page) + '.html'
    r = requests.get(url, headers, timeout=10)
    s = requests.session()
    s.keep_alive = False
    r.encoding = 'gbk'
    reg = re.compile(r'class="t1 ">.*? <a target="_blank" title=".*?" href="(.*?)".*? <span class="t2">', re.S)
    links = re.findall(reg, r.text)
    return links


# 多页处理，下载到文件
def get_content(link, writer):
    r1 = requests.get(link, headers, timeout=10)
    s = requests.session()
    s.keep_alive = False
    r1.encoding = 'gb2312'
    t1 = html.fromstring(r1.text)
    # print(link)
    job = t1.xpath('//div[@class="tHeader tHjob"]//h1/text()')[0].strip()
    print(job)
    company = t1.xpath('//p[@class="cname"]/a/text()')[0].strip()
    # print(company)
    salary = t1.xpath('//div[@class="cn"]//strong/text()')[0].strip()
    # print(salary)
    area = t1.xpath('//p[@class="msg ltype"]/text()')[0].strip()
    # print(area)
    experience = t1.xpath('//p[@class="msg ltype"]/text()')[1].strip()
    # print(experience)
    education = t1.xpath('//p[@class="msg ltype"]/text()')[2].strip()
    # print(education)
    company_type = t1.xpath('//p[@class="at"]/text()')[0].strip()
    # print(company_type)
    company_size = t1.xpath('//p[@class="at"]/text()')[1].strip()
    # print(companyscale)
    direction = t1.xpath('//div[@class="com_tag"]/p/a/text()')[0].strip()
    # print(direction)
    address = t1.xpath('//div[@class="bmsg inbox"]//text()')[2].strip()
    describe = t1.xpath('//div[@class="bmsg job_msg inbox"]//text()')
    # print(describe)
    writer.writerow((link, job, company, salary, area, experience, education, company_type, company_size,
                     direction, address, describe))
    return True


def write_excel_xls_append(items, file_name, path):
    index = len(items)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path + file_name)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for i in range(0, index):
        item = items[i]
        # 追加写入数据，注意是从i+rows_old行开始写入
        new_worksheet.write(i + rows_old, 0, item['link'])
        new_worksheet.write(i + rows_old, 1, item['job'])
        new_worksheet.write(i + rows_old, 2, item['company'])
        new_worksheet.write(i + rows_old, 3, item['salary'])
        new_worksheet.write(i + rows_old, 4, item['area'])
        new_worksheet.write(i + rows_old, 5, item['experience'])
        new_worksheet.write(i + rows_old, 6, item['education'])
        new_worksheet.write(i + rows_old, 7, item['companyType'])
        new_worksheet.write(i + rows_old, 8, item['companySize'])
        new_worksheet.write(i + rows_old, 9, item['direction'])
        new_worksheet.write(i + rows_old, 10, item['address'])
        new_worksheet.write(i + rows_old, 11, item['describe'])

    new_workbook.save(path + file_name)  # 保存工作簿
    print("追加数据成功！")


def main():
    # 主调动函数
    # 爬取前三页信息
    cityName = str(input('请输入查找的地区：'))
    keyWord = str(input('请输入查找的职位关键字：'))
    needPage = int(input('请输入要爬取的页数(页/50条)：'))
    # 编码调整，如将“数据挖掘”编码成%25E6%2595%25B0%25E6%258D%25AE%25E6%258C%2596%25E6%258E%2598
    key = parse.quote(parse.quote(keyWord))

    # .csv文件，进行写入操作
    file_name = cityName+'-'+keyWord+'.csv'
    path = './前程无忧/'
    if not os.path.exists(path):
        os.mkdir(path)
    csvFile = open(path + file_name, 'w', newline='')
    writer = csv.writer(csvFile)
    writer.writerow(('link', 'job', 'company', 'salary', 'area', 'experience', \
                     'education', 'companyType', 'companySize', 'direction', 'address', 'describe'))

    for i in range(1, needPage + 1):
        print('正在爬取第{}页信息'.format(i))
        city_code = city.get(cityName, '000000')
        links = get_links(i + 1, city_code, key)
        for link in links:
            try:
                get_content(link, writer)
            except:
                print("数据有缺失值")
                continue
    # 关闭写入文件
    csvFile.close()


if __name__ == '__main__':
    main()
