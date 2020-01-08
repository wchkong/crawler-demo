from urllib.parse import urlencode
import requests
import pymysql
import hashlib
import random
import time
from copy import copy
import xlrd
import json


# 经过分析_v就是一个随机的8位小数
# x-zp-page-request-id 由三部分组成，32位随机数据通过md5简单加密得到+ 当前时间戳 + 随机数6位
# 想办法用python简单实现所谓的加密算法x-zp-page-request-id
#from django.contrib.sites import requests

# 数据库连接
conn = pymysql.connect(host='192.168.3.226', port=3306, user='root', passwd='cdqd-passw0rd', db='web_crawler', charset='utf8')
cursor = conn.cursor()

key = '%e5%a4%a7%e5%81%a5%e5%ba%b7'.encode("utf-8").decode("latin1")
city = '530'
# 北京 530

# 1、生成一个随机32位数id
md5 = hashlib.md5()
id = str(random.random())
md5.update(id.encode('utf-8'))
random_id = md5.hexdigest()
#  2、生成当前时间戳
now_time = int(time.time() * 1000)
#  3、生成随机6位数
randomnumb = int(random.random() * 1000000)
# 组合代码生成x-zp-page-request-id
x_zp_page_request_id = str(random_id) + '-' + str(now_time) + '-' + str(randomnumb)
# print(x_zp_page_request_id)
# 生成_v
url_v = round(random.random(), 8)
print(url_v)
headers = {
        #"host": "fe-api.zhaopin.com",
        "origin": "https://sou.zhaopin.com",
        "referer": "https://sou.zhaopin.com/?jl=530&sf=0&st=0&kw=" + key + "&kt=3",
        "user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        # "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "accept-encoding": "gzip, deflate, br",
        "accept":"application/json, text/plain, */*",
    }


def get_page(start, key, city):
    params = {
        "start": str(start),
        "pageSize": "90",
        "cityId": city,
        "industry": "160400",
        # "salary": str("0,0"),
        "workExperience": "-1",
        "education": "-1",
        "companyType": "-1",
        "employmentType": "-1",
        "jobWelfareTag": "-1",
        "kw": key,  # 关键词
        "kt": "3",
        #"at": "d47e5b2c03e74fa7afa8df838182f953",
        #"rt": "20618b2b78f748d795ea879f51221a4e",
        '_v': url_v,
        "userCode": "1029652508",
        'x-zp-page-request-id': x_zp_page_request_id
    }
    # print()
    url = "https://fe-api.zhaopin.com/c/i/sou?" + urlencode(params, encoding='utf8')
    newurl = url.replace("25", "")
    # print(url.replace("25", ""))
    # ajax请求头参数
    # 这里的headers是一个全局变量，在该函数内为headers赋值
    headers = {
        "Host": "fe-api.zhaopin.com",
        "Origin": "https://sou.zhaopin.com",
        "Referer": "https://sou.zhaopin.com/?jl=489&in=160400&sf=0&st=0&kw=" + key + "&kt=3",
        "User-Agent": 'Baiduspider',
        # "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, br"
    }
    result_json = download_retry(newurl)
    return result_json


def download_retry(url):
    try:
        # 此时的数据库中的IP地址都是经过测试可用的
        # 从数据库中随机选择一个IP地址
        random_ip = 'SELECT proxy_type,ip, port FROM proxy_ip WHERE status = "1" AND id < "2000" ORDER BY RAND() LIMIT 1;'
        cursor.execute(random_ip)
        proxy_type, ip, port = cursor.fetchone()
        proxies = {proxy_type: proxy_type + '://' + ip + ':' + port}

        requests.packages.urllib3.disable_warnings()

        response = requests.post(url, headers=headers, proxies=proxies, timeout=5)
        result = json.loads(response.text)
        print(result)
        if response.status_code == 200:
            result = response.json()
        else:
            result = None
    except:
        raise ConnectionError
    return result


def get_content(json):
    if json is not None:
        items = []
        result_items = json.get("data").get("results")
        # print(result_items)
        for item in result_items:
            dic = {}
            dic['job_name'] = item['jobName']
            dic['company_name'] = item['company']['name']
            dic['work_place'] = item['city']['display']
            dic['salary'] = item['salary']
            dic['education'] = item['eduLevel']['name']
            dic['experience'] = item['workingExp']['name']
            dic['welfare'] = item['welfare']
            dic['job_href'] = item['positionURL']
            dic['company_href'] = item.get("company").get("url")
            items.append(dic)
        # print(items)
        return items


def write_excel_xls_append(items):
    index = len(items)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook("Job1.xls")  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for i in range(0, index):
        item = items[i]
        # 追加写入数据，注意是从i+rows_old行开始写入
        new_worksheet.write(i + rows_old, 0, item['job_name'])
        new_worksheet.write(i + rows_old, 1, item['company_name'])
        new_worksheet.write(i + rows_old, 2, item['work_place'])
        new_worksheet.write(i + rows_old, 3, item['salary'])
        new_worksheet.write(i + rows_old, 4, item['education'])
        new_worksheet.write(i + rows_old, 5, item['experience'])
        # str = ','.join(company_href[i])  # 用，将各福利连接起来
        new_worksheet.write(i + rows_old, 6, item['welfare'])
        new_worksheet.write(i + rows_old, 7, item['job_href'])
        new_worksheet.write(i + rows_old, 8, item['company_href'])
    new_workbook.save("Job1.xls")  # 保存工作簿
    print("追加数据成功！")


json_str = get_page(0, key, city)
write_excel_xls_append(json_str)
