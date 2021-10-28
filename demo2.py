import requests
import pandas as pd
from lxml import etree
import time
import random

headers = {
    "Accept-Encoding": "Gzip",  # 使用gzip压缩传输数据让访问更快
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
    # "Cookie": cookie
    }

# 设置代理
# 提取代理API接口，获取1个代理IP
api_url = "https://kps.kdlapi.com/api/getkps/?orderid=993533458201919&num=1&pt=1&sep=1"

# 获取API接口返回的代理IP
proxy_ip = requests.get(api_url).text

# 用户名密码认证(私密代理/独享代理)
username = "1550505935"
password = "5en34gmt"
# proxy = {
#     "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip},
#     "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip}
# }


# 网页是动态刷新的虽然页面1,2显示的url链接中page是1,3。但实际上第一页中前30个商品为page1，后30个商品为page2
def get_html(page):
    url = f'https://search.jd.com/Search?keyword=%E5%8F%A3%E7%BA%A2&qrst=1&wq=%E5%8F%A3%E7%BA%A2&stock=1&pvid=148fb7e5c10b4f879ef1e245c89ecb24&page={page}'
    r = requests.get(url, headers=headers)
    time.sleep(random.randint(1, 3))
    return r

# 获取总评数和好评率
def get_comments(pid):
    comment_url = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds="
    comment_url += pid
    comment_r = requests.get(comment_url,headers=headers)
    time.sleep(random.randint(3, 5))
    comment_sum = comment_r.json()["CommentsCount"][0] # 总评数，平均得分，好评数，默认好评，好评率，追评数，视频晒单数，差评数，中评数
    return comment_sum

def get_data():
    # 京东商城页面一页有两个page，所以采集前10页数据，page参数为1-20
    for page in range(37,41):
        r = get_html(page)
        r_html = etree.HTML(r.text)
        lis = r_html.xpath('//li[contains(@class,"gl-item")]')
        for i in lis:
            ID = i.xpath('./@data-sku')[0]
            name_temp = i.xpath('./div/div[@class="p-name p-name-type-2"]/a/em/text()')
            name_temp = [x for x in name_temp if x != ' ']
            name = ''.join(name_temp)
            price = i.xpath('./div/div[@class="p-price"]/strong/i/text()')[0]
            store_name = i.xpath('./div/div[@class="p-shop"]/span/a/text()')[0]
            self_run = ''.join(i.xpath('./div/div[@class="p-icons"]/i/text()'))
            url_list = i.xpath('./div/div[@class="p-commit"]/strong/a/@href')[0]
            comment_sum = get_comments(ID)
            CommentCount = comment_sum['CommentCountStr']
            GoodRate = comment_sum['GoodRate']
            df = pd.DataFrame({'ID':ID,
                               'name':name,
                               'price':price,
                               'store_name':store_name,
                               'self_run':self_run,
                               'url_list':url_list,
                               'CommentCount':CommentCount,
                               'GoodRate':GoodRate
                               },index=[0])
            print(df)
            df.to_csv('京东口红信息.csv',index=False,header=False,mode='a')
        print(f'第{page}页数据已经采集')

# 运行爬虫程序
get_data()