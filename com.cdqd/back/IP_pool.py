import pymysql
import requests
from scrapy.selector import Selector

# 数据库连接
conn = pymysql.connect(host='192.168.3.226', port=3306, user='root', passwd='root', db='web_crawler', charset='utf8')
cursor = conn.cursor()


def crawl_ips():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/59.0.3071.115 Safari/537.36"}
    for i in range(1, 10):
        url = 'http://www.xicidaili.com/wt/{0}'.format(i)
        req = requests.get(url=url, headers=headers)
        selector = Selector(text=req.text)
        all_trs = selector.xpath('//*[@id="ip_list"]//tr')  # 共同前缀

        ip_lists = []
        for tr in all_trs[1:]:
            speed_str = tr.xpath('td[7]/div/@title').extract()[0]
            if speed_str:
                speed = float(speed_str.split('秒')[0])
            ip = tr.xpath('td[2]/text()').extract()[0]
            port = tr.xpath('td[3]/text()').extract()[0]
            proxy_type = tr.xpath('td[6]/text()').extract()[0].lower()
            ip_lists.append((ip, port, speed, proxy_type))

        for ip_info in ip_lists:
            cursor.execute(
                f"INSERT proxy_ip(ip,port,speed,proxy_type) VALUES('{ip_info[0]}','{ip_info[1]}',{ip_info[2]},"
                f"'{ip_info[3]}') "
            )
            conn.commit()

# crawl_ips()


#从数据库中随机取免费的IP地址，并且判断该IP地址的可用性。
class GetIP(object):
    # 删除无效的免费ip信息
    def delete(self, ip):
        #delete_sql = 'DELETE FROM proxy_ip WHERE ip="{0}"'.format(ip)
        delete_sql = 'UPDATE proxy_ip SET status = "0" WHERE ip="{0}"'.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def valid_ip(self, ip, port, proxy_type):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/59.0.3071.115 Safari/537.36"}
        try:
            proxies = {proxy_type: proxy_type + '://' + ip + ':' + port}
            req = requests.get('http://ip.chinaz.com/getip.aspx', headers=headers, proxies=proxies, timeout=5)
        except:
            print('invalid ip and port：' + ip)
            self.delete(ip)
            return False
        else:
            if 200 <= req.status_code < 300:
                # print('{0} effective ip~'.format(proxies))
                print(req.text)
                return True
            else:
                print('invalid ip and port')
                self.delete(ip)
                return False

    # 随机从数据库中取ip地址
    @property
    def get_random_ip(self):
        for i in range(1, 1000):
            random_ip = 'SELECT proxy_type,ip, port FROM proxy_ip WHERE id = '+str(i)+';'
            cursor.execute(random_ip)
            try:
                proxy_type, ip, port = cursor.fetchone()
                # 把获取到的ip地址通过拆包的方式分别复制给协议，IP以及端口，
                # 然后把这三个参数送给valid_ip方法做验证
                valid_ip = self.valid_ip(ip, port, proxy_type)
                if valid_ip:
                    return {proxy_type: proxy_type + '://' + ip + ':' + port}
                else:
                    continue
            except:
                continue



#crawl_ips()
proxy = GetIP()
print(proxy.get_random_ip)
