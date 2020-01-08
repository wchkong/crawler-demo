import requests
from urllib.parse import urlencode  # 解决编码问题
from urllib import request
import json
from http import cookiejar


# 起始页，城市名，岗位词
def get_page(offset,cityName,keyWord):

    # 有反爬，添加一下header
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        #'cookie':'_uab_collina=157838852737843474627389; acw_tc=2760821415783885259256152e2648934c7f2176ea85c1d86e77cebd190b14; FSSBBIl1UgzbN7N443S=f1OmOQLwj1LqCC3AyF6nkaiUZjDYJlJjZwgRnwFFPrzESIZKg50Pqr.m_OY0j0t8; u_asec=099%23KAFEoGEKEVGEhGTLEEEEEpEQz0yFD6NcSrOYZ6fwDu94W60EScy5Z60FZf7TEEiStEE7BYFETEEEbOKhE7Eht3alluZdsEFEp3iSlldx7GCqt37MlXZdtyJStTLtsyaGC3iSh3nP%2F3wIt37MlXZddqgoE7EIt37Er0RGnzJrE7Eht%2FMF16eHAYFwEU1ldzhdCwUQrjDt9yRBNOEQPwD7%2F6ZncR7n3MesDzXANsjtLO%2Fcvs4WbFs3Wf4icR1a1Q2tAspXvTYs%2BOnK%2Fp7Cv%2FbuQ2x24g82GIRAGVeo8VIulVhN4g82I7RsVPcYUjcV1bZDAsCXhKIulu2NhTcsPSWq4X4QbL8S1SZnSzWk8TqRCWJ1bweSPSSTuoYibyXZaYeWGCedcRITlXBwbOMQ6US7rfGnc%2BedaY%2FzAKYi6yfpgsJfqsEVbbopbQWk8TcDLGJAGVe%2B8zIulVkg4g82UJlsVPc%2B8zI0ldwNGT82UKOs3rh48zI084I1doc2I0biLqlzZgc%2FcVWu3XBBvKr08E1ldUek3i%2BkaYeaDzMVbOY31W9iNO7CvYTpbUoobTr0xvlvSTUybOEExs1EbiFoqoPlQf7yhwhol9sgDg4ohgaE9un980CkhatlQ6XyFaCk5qsV8L2SbL93lyn0vgY28sWpQ6x2NzeC%2FGwVa04Ab00pEcBfNg%2B08yQRVIhGqzCC1dCYDw%2BVJ0ftxshobw%2BSHDwqPfUQPwoB%2BUZVNOhBPKXcL2hXrieGcodTVqIQbRcCgYCrCVWohTcpwpw0zwpX4Lsl42xxh0UoY%2F%2F8SVCy4gvlEuwHh0UgU3buQ21gFs8Ga7e8nVQM4gvl3zXvFsrncMGwO6CCcyxCiMeALK2MFsRRws9kcOxn6GJtVocAPsMQ14ZPuyGQbzstl%2FpBPLYZPAE6bfdWpOGQ1GJVCTqDPahJ1sLXbw8CpYeRWoxMFsksE9%2F8SWp24gvlErwHh0eY8lbuQ2x24g82G3sAGVeY8zIulVh44g82I7RsVPqg8AcDaGJvG2dsvgYtlry98V8MvRdsOIFtcKMQ1UrAvw8CrRURLe16PwpXvFzRQf8GhV4A9nsLDArCbKARCuxJqjGAqvllQfoMq0Ckl%2FlLSjG2JTAlEcymvKMyhnulQt7i3KMta%2FZnZsxC6aOtwR16hTeyhIelQ6kk8OI2E3nYSahANLFElraThK80hErubfECvRpCWEFE5Y745EThsiza0JmfvhBD0HUaBFuf0RANIwEbkfMu%2BwD4kL0B1ZWcqiTo3mvkqUYb0HUVmStGe1A4kLH6maynfkVxIYP05c7DBwD4D4Gu%2B1b%2BfxRuE7EFNIaHF7%3D%3D; FSSBBIl1UgzbN7N443T=4pwaJpy_JLRjRDcEl35Phm8QPOxBRMxAAPqGChjJeaFoSwtr8EZa6z6_6wVRfUGEcbke_lLw3xzrvc4p1shbVbA1TZK5d7X826PFcrEWNBQE67miKIkCKXdbglAsMYj15pKi2fQZHR8UUyEZk.aUUOzwEvVgvw.sgtA0krwKlux71VOwrDwtnpjZPDvg9W8gmwE78UTHisSlCLy.kXX5zBuKL3ATF9Pea0NxrwR6AcmtUwolw7BnygYJ8Bd6tsW4Wn4OCZk_FV.grOeWxGt7Tex8Jrv_URm.ciAUJZwC42Unpl7BOFx.yohcoZqeMg.qM0Mg',
        #'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        #"origin": "https://sou.zhaopin.com",
        #"referer": "https://sou.zhaopin.com/?jl=530&sf=0&st=0&kw=" + '%e5%a4%a7%e5%81%a5%e5%ba%b7' + "&kt=3",
    }

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
        resp = requests.get(url, headers=headers, timeout=5)
        print(resp.text)
        if 202 == resp.status_code:
            cookie = resp.cookies
            req = request.Request(url, headers=headers)
            request.HTTPCookieProcessor(cookie)
            opener = request.build_opener(request.HTTPCookieProcessor(cookie))
            response = opener.open(req)
            print(response.read())

        if 200 == resp.status_code:  # 状态码判断
            print(resp.json())
            return resp.json()
    except requests.ConnectionError:
        print('请求出错')
        return None


def get_information(json_page):
    if json_page.get('data'):
        results = json_page.get('data').get('results')
        print(results)
        for result in results:
            yield {  # yield 是一个类似 return 的关键字，迭代一次遇到yield时就返回yield后面(右边)的值。

                'number': result.get('number'),  # 编号
                'jobName': result.get('jobName'),  # 岗位名称
                'city': result.get('city').get('display'),  # 城市地区
                'company': result.get('company').get('name'),  # 公司名字
                # 'welfare':result.get('welfare'),              #福利信息
                'workingExp': result.get('workingExp').get('name'),  # 工作经验
                'salary': result.get('salary'),  # 薪资范围
                'eduLevel': result.get('eduLevel').get('name')  # 学历
            }
    print('success!')

def write_to_file(content):
    # print('dict:',type(content))
    with open('result.txt', 'a', encoding='utf-8') as f:
        # print(type(json.dumps(content)))
        f.write(json.dumps(content, ensure_ascii=False) + '\n')  # 将字典或列表转为josn格式的字符串



def main(offset):
    json_page = get_page(offset, cityName, keyWord)  # 发送请求，获得json数据
    contentList = get_information(json_page)  # 提取json数据对应的字段内容

    for content in contentList:  # 循环持久化
        write_to_file(content)
        # save_data_sql(content)             # 在数据库新建表以后在打开这个


if __name__ == '__main__':
    cityName = str(input('请输入查找的地区：'))
    keyWord = str(input('请输入查找的职位关键字：'))
    needPage = int(input('请输入要爬取的页数(页/90条)：'))
    # 控制爬取的页数
    for i in range(needPage):
        main(offset=90 * i)  # 分析url知首页是90开始的，翻页是其倍数。


