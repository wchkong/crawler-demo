from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

caps = webdriver.DesiredCapabilities().FIREFOX
caps['marionette'] = True
binary = FirefoxBinary(r'/Applications/Firefox.app/Contents/MacOS/firefox')
# 这是下载在mac中的火狐可执行文件的默认地址
driver = webdriver.Firefox(firefox_binary=binary, capabilities=caps,
                           executable_path='/Users/kongweichang/Downloads/geckodriver')
url = 'https://www.baidu.com/'
# 可以改成你想显示的网页
driver.get(url)