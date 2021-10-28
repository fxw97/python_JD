import requests
import pandas as pd
from lxml import etree
import time
import json
import re

headers = {
    # "Accept-Encoding": "Gzip",  # 使用gzip压缩传输数据让访问更快
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    # "Cookie": cookie
    }

def get_html(page):
    url =f'https://search.jd.com/Search?keyword=%E5%8F%A3%E7%BA%A2&qrst=1&stock=1&pvid=d74f7d2a716342d58a6e6240eaea2b99&page={page}'
    r = requests.get(url, headers=headers, timeout=6)
    return r


# 获取评论信息
def get_comment(productId):
    time.sleep(3)
    url = 'https://club.jd.com/comment/skuProductPageComments.action?'
    params = {
        'callback': 'fetchJSON_comment98',
        'productId': productId,
        'score': 0,
        'sortType': 6,
        'page': 0,
        'pageSize': 10,
        'isShadowSku': 0,
        'fold': 1,
    }

    r = requests.get(url, headers=headers, params=params, timeout=6)
    comment_data = re.findall(r'fetchJSON_comment98\((.*)\)', r.text)[0]
    comment_data = json.loads(comment_data)
    comment_summary = comment_data['productCommentSummary']

    return comment_summary

def get_data():
    df = pd.DataFrame(columns=['productId', 'price', 'name', 'shop', '自营'])
    for page in range(1,41):
        r = get_html(page)
        r_html = etree.HTML(r.text)
        lis = r_html.xpath('.//li[@class="gl-item"]')
        for li in lis:
            item = {
                "productId": li.xpath('./@data-sku')[0],  # id
                "price": li.xpath('./div/div[@class="p-price"]/strong/i/text()')[0],  # 价格
                "name": ''.join(li.xpath('./div/div[@class="p-name p-name-type-2"]/a/em/text()')),  # 商品名
                "shop": li.xpath('./div/div[@class="p-shop"]/span/a/text()')[0],  # 店铺名
                "自营": li.xpath('./div/div[@class="p-icons"]/i/text()'),  # 自营
            }
            df = df.append(item, ignore_index=True)
        print(f'\r第{page}/40页数据已经采集', end='')
    df.to_excel('采集数据.xlsx',index=False)

get_data()