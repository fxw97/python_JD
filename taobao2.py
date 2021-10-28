# 配置浏览器驱动： chrome浏览器的版本 指定版本下载浏览器驱动 放到环境的指定位置 添加到环境变量C:\Program Files\Google\Chrome\Application 重启电脑
# 安装谷歌浏览器插件xpath-helper
from selenium import webdriver
import random
import time
import pandas as pd


def search_product(keyword):
    # 根据关键字搜索商品
    driver.find_element(by = 'xpath',value = '//*[@id="q"]').send_keys(keyword) # find_element_by_xpath()已经弃用了，现在使用的是find_element()
    # 为了避免淘宝检测selenium,设置1-3秒的等待时间，模拟用户的操作
    time.sleep(random.randint(1,3))

    # 点击搜索按钮
    driver.find_element('xpath','//*[@id="J_TSearchForm"]/div[1]/button').click()
    time.sleep(random.randint(1,3))

    # 解决登陆,selenium没有缓存
    driver.find_element('xpath','//*[@id="fm-login-id"]').send_keys('1550505935@qq.com')
    time.sleep(random.randint(1, 3))
    driver.find_element('xpath','//*[@id="fm-login-password"]').send_keys('fxwFXW1997')
    time.sleep(random.randint(1, 3))
    driver.find_element('xpath','//*[@id="login-form"]/div[4]/button').click()
    time.sleep(random.randint(1, 3))

# 解析多个商品数据
def parse_data():
    divs = driver.find_elements('xpath','//div[@class="grid g-clearfix"]/div/div') # 获取所有的div标签
    for div in divs:
        name = div.find_element('xpath', ".//div[@class='row row-2 title']/a").text
        price = ''.join(div.find_element('xpath', ".//div[@class='price g_price g_price-highlight']/strong").text)
        deal= div.find_element('xpath', ".//div[@class='deal-cnt']").text
        shop_name = div.find_element('xpath', ".//div[@class='shop']/a/span[2]").text
        location = div.find_element('xpath', ".//div[@class='location']").text
        url = div.find_element('xpath', ".//div[@class='pic']/a").get_attribute('href')
        name_list.append(name)
        price_list.append(price)
        deal_list.append(deal)
        shop_name_list.append(shop_name)
        location_list.append(location)
        url_list.append(url)

# 翻页
def turn_page(i):
    driver.find_element('xpath','//*[@id="mainsrp-pager"]/div/div/div/ul/li[{}]/a'.format(i)).click()
    time.sleep(random.randint(5, 8))

# 输入商品名
word = input('请输入你要搜索商品的关键字:')

# 创建一个谷歌浏览器的对象
driver = webdriver.Chrome()

# 修改浏览器属性，绕过滑块验证码
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                       {'source':'''Object.defineProperty(navigator,'webdriver',{get:()=>undefined})'''})
# 执行浏览器操作
driver.get('https://www.taobao.com/')
'''
执行浏览器自动化操作：
用户平常怎么操作浏览器页面，咱们代码的逻辑和用户操作界面的逻辑大致一致
'''
driver.implicitly_wait(10) # 智能化等待：页面渲染加载过程需要时间
driver.maximize_window() # 最大化浏览器

# 建立用于存放数据的列表
name_list = []
price_list = []
deal_list = []
shop_name_list = []
location_list = []
url_list = []

# 1.调用搜索商品的函数
search_product(word)

for page in range(2,9):
    # 2.查找商品数据并保存在各列表中
    parse_data()

    # 3.翻页
    turn_page(page+1)

data = pd.DataFrame([name_list,
                     price_list,
                     deal_list,
                     shop_name_list,
                     location_list,
                     url_list],
                    index=['name','price','deal','shop_name','location','url'],columns=None)

data_final = data.T
data_final.to_csv('淘宝前8页耳机数据.csv',encoding='gbk',index=False)