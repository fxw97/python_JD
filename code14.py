
import requests  # 导入网络请求模块
import pandas    # 导入pandas模块
from lxml import etree  # 导入HTML解析模块

ip_table = pandas.read_excel('ip.xlsx')  # 读取代理IP文件内容
ip = ip_table['ip']                      # 获取代理ip列信息
# 头部信息
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/72.0.3626.121 Safari/537.36'}
# 循环遍历代理IP并通过代理发送网络请求
for i in ip:
    proxies = {'http': 'http://{ip}'.format(ip=i),
               'https': 'https://{ip}'.format(ip=i)}
    try:
        response = requests.get('http://202020.ip138.com/',
                                headers=headers,proxies=proxies,timeout=2)
        if response.status_code==200:   # 判断请求是否成功,请求成功说明代理IP可用
            response.encoding='utf-8'     # 进行编码
            html = etree.HTML(response.text)  # 解析HTML
            info = html.xpath('/html/body/p[1]//text()')
            print(info)                 # 输出当前ip匿名信息
    except Exception as e:
        pass
        # print('错误异常信息为：',e)    # 打印异常信息
