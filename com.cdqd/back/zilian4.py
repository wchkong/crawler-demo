from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pymysql

def get_main_page(keyword, city):
    fox = webdriver.Firefox(executable_path='/Users/kongweichang/Downloads/geckodriver')
    url = 'https://fe-api.zhaopin.com/c/i/sou?start=0&pageSize=90&cityId=%E5%8C%97%E4%BA%AC&salary=0%2C0&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=%E5%A4%A7%E5%81%A5%E5%BA%B7&kt=3&_v=0.12973194&x-zp-page-request-id=9bf58a63b73746ea9fd0cb8bd75560b9-1572848879239-667477&x-zp-client-id=0470c445-5e49-43bc-b918-0330e0ead9ee'
    fox.get(url)
    time.sleep(1)

    jl = fox.find_element_by_id('JobLocation')
    jl.clear()
    jl.send_keys(city)

    zl = fox.find_element_by_id('KeyWord_kw2')
    zl.clear()
    zl.send_keys(keyword)

    sj = fox.find_element_by_class_name('doSearch').click()
    time.sleep(3)
    get_everypage_info(fox, keyword, city)

def get_everypage_info(fox, keyword, city):
    fox.switch_to_window(fox.window_handles[-1])
    tables = fox.find_elements_by_tag_name('table')

    table_name = city + '_' + keyword
    conn = pymysql.Connect(host='127.0.0.1', port=3306, user='root', passwd='', db='python', charset='utf8')
    cursor = conn.cursor()

    sql = """CREATE TABLE IF NOT EXISTS %s(
                职位名称 CHAR(100),
                公司名称 CHAR(100),
                工作地点 CHAR(100),
                公司规模 CHAR(100),
                工作经验 CHAR(100),
                平均月薪 CHAR(100),
                学历要求 CHAR(100)
                 )default charset=UTF8""" % (table_name)
    cursor.execute(sql)

    for i in range(0, len(tables)):
        if i == 0:
            '''
            row = ['职位名称', '公司名称', '工作地点', '公司规模', '工作经验', '平均月薪', '学历要求', '职位描述']
            information.append(row)
            '''
        else:
            address, develop, jingyan, graduate, require = " ", " ", " ", " ", " "
            job = tables[i].find_element_by_tag_name('a').text
            company = tables[i].find_element_by_css_selector('.gsmc a').text
            salary = tables[i].find_element_by_css_selector('.zwyx').text

            spans = tables[i].find_elements_by_css_selector('.newlist_deatil_two span')
            for j in range(0, len(spans)):
                if "地点" in spans[j].get_attribute('textContent'):
                    address = (spans[j].get_attribute('textContent'))[3:]
                elif "公司规模" in spans[j].get_attribute('textContent'):
                    develop = (spans[j].get_attribute('textContent'))[5:]
                elif "经验" in spans[j].get_attribute('textContent'):
                    jingyan = (spans[j].get_attribute('textContent'))[3:]
                elif "学历" in spans[j].get_attribute('textContent'):
                    graduate = (spans[j].get_attribute('textContent'))[3:]

            require = (tables[i].find_element_by_css_selector('.newlist_deatil_last').get_attribute('textContent'))[8:]

            row = [job, company, address, develop, jingyan, salary, graduate, require]
            insert_row = ('insert into {0}(职位名称,公司名称,工作地点,公司规模,工作经验,平均月薪,学历要求) VALUES(%s,%s,%s,%s,%s,%s,%s)'.format(table_name))
            insert_data = (job, company, address, develop, jingyan, salary, graduate)
            cursor.execute(insert_row, insert_data)
            conn.commit()
            with open('%s职位描述.txt' % (table_name), 'a', encoding='utf-8') as f:
                f.write(require)

    print('此页已抓取···')
    conn.close()

    count = 0
    while count <= 10:
        try:
            next_page = fox.find_element_by_class_name('pagesDown-pos').click()
            break
        except:
            time.sleep(8)
            count += 1
            continue

    if count > 10:
        fox.close()
    else:
        time.sleep(1)
        get_everypage_info(fox, keyword, city)


if __name__ == "__main__":
    citys = ['上海', '深圳', '广州', '北京', '成都']   # '北京',   已爬取
    job = '数据挖掘分析'
    for city in citys:
        print(city)
        get_main_page(job, city)