import requests
from urllib.parse import urlencode  # 解决编码问题
from selenium import webdriver
from time import sleep
import csv
import os
import json
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
'''由于反爬措施比较多破解比较麻烦，这里使用无头浏览器抓去'''


def selenium_request(req_url):
    #req_url = "https://fe-api.zhaopin.com/c/i/sou?start=0&pageSize=90&cityId=%E5%8C%97%E4%BA%AC&salary=0%2C0&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=%E5%A4%A7%E5%81%A5%E5%BA%B7&kt=3&_v=0.12973194&x-zp-page-request-id=9bf58a63b73746ea9fd0cb8bd75560b9-1572848879239-667477&x-zp-client-id=0470c445-5e49-43bc-b918-0330e0ead9ee"
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    profile = webdriver.FirefoxProfile()
    profile.set_preference('devtools.jsonview.enabled', False)

    caps = webdriver.DesiredCapabilities().FIREFOX
    caps['marionette'] = True
    binary = FirefoxBinary(r'/Applications/Firefox.app/Contents/MacOS/firefox')
    fox = webdriver.Firefox(firefox_binary=binary, capabilities=caps, firefox_profile=profile,
                           executable_path='geckodriver_path', options=options)
    # 开始请求
    fox.get(req_url)
    sleep(5)
    # 打印页面
    print(fox.page_source)
    page = fox.page_source
    # 关闭浏览器
    fox.close()
    # 关闭driver进程
    fox.quit()
    return page


# 起始页，城市名，岗位词
def get_page(offset,cityName,keyWord):

    #　构建参数组
    params = {
        'start': offset,
        'pageSize': '90',
        'cityId': cityName,
        'salary': '0,0',
        'workExperience': '-1',
        'education': '-1',
        'companyType': '-1',
        'employmentType': '-1',
        'jobWelfareTag': '-1',
        'kw': keyWord,
        'kt': '3',
        '_v': '0.66224377',
        'x-zp-page-request-id': '1b3a0940a8ca4307823234407b36a176-1578387239975-98564',
        'x-zp-client-id': '3f20c528-b46d-4a8b-8189-21e2e7a68495'
    }
    base_url = 'https://fe-api.zhaopin.com/c/i/sou?'
    url = base_url + urlencode(params) # 拼接url,要进行编码。
    print('爬取的URL为：', url)
    try:
        resp = selenium_request(url)
        resp = str(resp)
        json_str = resp.split("<pre>")[1].replace("</pre></body></html>", "")
        print(json_str)
        return json.loads(json_str)
    except requests.ConnectionError:
        print('请求出错')
        return None


def get_information(json_page):
    if json_page.get('data'):
        results = json_page.get('data').get('results')
        print(results)
        for result in results:
            link = result.get('positionURL'),  # 编号
            jobName = result.get('jobName'),  # 岗位名称
            #'jobType': result.get('jobName'),  # 岗位名称
            city = result.get('city').get('display'),  # 城市地区
            company = result.get('company').get('name'),  # 公司名字
            companyType = result.get('company').get('type').get('name'),  # 公司类型
            companySize = result.get('company').get('size').get('name'),  # 公司规模
            companyUrl = result.get('company').get('url')
            # 'welfare':result.get('welfare'),              #福利信息
            workingExp = result.get('workingExp')
            if workingExp is not None:
                workingExp = result.get('workingExp').get('name'),  # 工作经验
            salary = result.get('salary'),  # 薪资范围
            eduLevel = result.get('eduLevel').get('name')  # 学历
            writer.writerow((json.dumps(link, ensure_ascii=False),
                             json.dumps(jobName, ensure_ascii=False),
                             json.dumps(city, ensure_ascii=False),
                             json.dumps(company, ensure_ascii=False),
                             json.dumps(companyType, ensure_ascii=False),
                             json.dumps(companySize, ensure_ascii=False),
                             json.dumps(companyUrl, ensure_ascii=False),
                             json.dumps(workingExp, ensure_ascii=False),
                             json.dumps(salary, ensure_ascii=False),
                             json.dumps(eduLevel, ensure_ascii=False),
                             ))

    print('success!')


def main(offset):
    json_page = get_page(offset, cityName, keyWord)  # 发送请求，获得json数据
    get_information(json_page)  # 提取json数据对应的字段内容


if __name__ == '__main__':
    cityName = str(input('请输入查找的地区：'))
    keyWord = str(input('请输入查找的职位关键字：'))
    needPage = int(input('请输入要爬取的页数(页/90条)：'))
    # .csv文件，进行写入操作
    file_name = cityName + '-' + keyWord + '.csv'
    path = './智联招聘/'
    if not os.path.exists(path):
        os.mkdir(path)
    csvFile = open(path + file_name, 'w', newline='')
    writer = csv.writer(csvFile)
    writer.writerow(('link', 'jobName', 'city', 'company', 'companyType', 'companySize', 'companyUrl',
                     'workingExp', 'salary', 'eduLevel', 'direction', 'address', 'describe'))

    # 控制爬取的页数
    for i in range(needPage):
        main(offset=90 * i)  # 分析url知首页是90开始的，翻页是其倍数。

