import requests
from urllib.parse import urlencode  # 解决编码问题
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep




def selenium_test():
    req_url = "https://fe-api.zhaopin.com/c/i/sou?start=0&pageSize=90&cityId=%E5%8C%97%E4%BA%AC&salary=0%2C0&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=%E5%A4%A7%E5%81%A5%E5%BA%B7&kt=3&_v=0.12973194&x-zp-page-request-id=9bf58a63b73746ea9fd0cb8bd75560b9-1572848879239-667477&x-zp-client-id=0470c445-5e49-43bc-b918-0330e0ead9ee"
    # 设置chrome浏览器无界面模式

    chrome_options.add_argument('--headless')
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    browser = webdriver.Chrome(options=options)

    # 开始请求
    browser.get(req_url)
    sleep(5)
    # 打印页面网址
    print(browser.page_source)
    # 关闭浏览器
    browser.close()
    # 关闭chromedriver进程
    browser.quit()

selenium_test()