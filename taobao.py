import requests
import pandas as pd
import numpy as np
from lxml import etree

headers = {
    # "Accept-Encoding": "Gzip",  # 使用gzip压缩传输数据让访问更快
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    # "Cookie": cookie
    }

# page:[0,44,88,132]
def get_html(page):
    url =f'https://s.taobao.com/search?q=%E5%8F%A3%E7%BA%A2&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.jianhua.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&s={page}'
    r = requests.get(url, headers=headers)
    r_html = etree.HTML(r.text)
    return print(r_html)

def get_data():
    df = pd.DataFrame(columns=['价格','名称', '商家', '地区', '销量'])
    for page in np.arange(0,4)*44:
        r = get_html(page)
        r_html = etree.HTML(r.text)
        lis1 = r_html.xpath('//*[@id="mainsrp-itemlist"]/div/div/div[1]/div')
        lis2 = r_html.xpath('//*[@id="J_Itemlist_TLink_625127127506"]')
        for li1 in lis1:
            item1 = {
                "价格": li1.xpath('./div[2]/div[1]/div[1]/strong/text()'),  # 价格
                "商家": li1.xpath('./div[2]/div[3]/div[1]/a/span[2]/text()'),  # 店铺名
                "地区": li1.xpath('./div[2]/div[3]/div[2]/text()'),
                "销量": li1.xpath('./div[2]/div[1]/div[2]/text()'),
            }
            df = df.append(item1, ignore_index=True)
        for li2 in lis2:
            item2 = {
                '名称': li2.xpath('./text()')[1] + str(li2.xpath('./span[2]')) + li2.xpath('./text()')[2]
            }
            df = df.append(item2, ignore_index=True)
        print('第{}页数据已经采集'.format(page/44+1), end='')
    df.to_excel('淘宝采集数据.xlsx',index=None)

get_html(44)

'''
价格 //*[@id="mainsrp-itemlist"]/div/div/div[1]/div[1]/div[2]/div[1]/div[1]/strong
销量 //*[@id="mainsrp-itemlist"]/div/div/div[1]/div[1]/div[2]/div[1]/div[2]
//*[@id="J_Itemlist_TLink_625127127506"]/text()[1]
//*[@id="J_Itemlist_TLink_625127127506"]/span[2]
//*[@id="J_Itemlist_TLink_625127127506"]/text()[2]
商家 //*[@id="mainsrp-itemlist"]/div/div/div[1]/div[1]/div[2]/div[3]/div[1]/a/span[2]
地区 //*[@id="mainsrp-itemlist"]/div/div/div[1]/div[1]/div[2]/div[3]/div[2]
'''