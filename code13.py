
import requests  # 导入网络请求模块
from lxml import etree  # 导入HTML解析模块
import pandas as pd  # 导入pandas模块
ip_list = []  # 创建保存ip地址的列表

def get_ip(url,headers):
    # 发送网络请求
    response = requests.get(url,headers=headers)
    response.encoding = 'utf-8'  # 设置编码方式
    if response.status_code == 200:  # 判断请求是否成功
        html = etree.HTML(response.text)  # 解析HTML
        # 获取所有带有IP的li标签
        li_all = html.xpath('//li[@class="f-list col-lg-12 col-md-12 col-sm-12 col-xs-12"]')
        for i in li_all:                  # 遍历每行内容
            ip = i.xpath('span[@class="f-address"]/text()')[0]  # 获取ip
            port = i.xpath('span[@class="f-port"]/text()')[0]  # 获取端口
            ip_list.append(ip+':'+port)     # 将ip与端口组合并添加至列表当中
            print('代理ip为：', ip, '对应端口为：', port)
# 头部信息
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/72.0.3626.121 Safari/537.36'}
if __name__ == '__main__':
    ip_table = pd.DataFrame(columns=['ip'])  # 创建临时表格数据
    for i in range(1,5):
        # 请求地址
        url = 'https://www.dieniao.com/FreeProxy/{page}.html'.format(page=i)
        get_ip(url,headers)
    ip_table['ip'] = ip_list  # 将提取的ip保存至excel文件中的ip列
    # 生成xlsx文件
    ip_table.to_excel('ip.xlsx', sheet_name='data')
