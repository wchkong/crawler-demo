import csv
import time

import requests
from fake_useragent import UserAgent


class Zhilian():
    def __init__(self):
        self.headers = {
            'User-Agent': str(UserAgent().random),
        }
        self.proxies = {"http": "http://121.232.194.196:9000"}
        self.base_url = 'https://fe-api.zhaopin.com/c/i/sou'
        self.info = []

    def send_request(self,params):
        response = requests.get(self.base_url, params=params, headers=self.headers,proxies=self.proxies)
        json_ = response.json()
        return json_

    def parse(self,json_):
        nodes = json_.get('data').get('results')
        if nodes == []:
            # 结束标志
            return 'finish'
        for node in nodes:
            item = {}
            # 职位名
            item['name'] = node.get('jobName')
            # 薪资
            item['salary'] = node.get('salary')
            # 地点
            item['place'] = node.get('city').get('display')
            # 经验
            if node.get('workingExp') != None:
                item['experience'] = node.get('workingExp').get('name')
            else:
                item['experience'] = ''
            # 学历
            item['degree'] = node.get('eduLevel').get('name')
            # 公司名
            item['company'] = node.get('company').get('name')
            # 详细信息url
            item['next_url'] = node.get('positionURL')
            self.info.append(item)

    def save(self):
        data = [info.values() for info in self.info]
        with open('jobs.csv', 'a+', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(data)

    def main(self):
        start = 90
        while True:
            params = {
                'start': start,
                'pageSize': '90',
                'cityId': '653',
                'kw': 'python',
                'kt': '3',
            }
            json_ = self.send_request(params)
            flag = self.parse(json_)
            print(str(start // 90) + '------OK')
            start += 90
            if flag == 'finish':
                break
        self.save()


if __name__ == '__main__':
    zl = Zhilian()
    zl.main()