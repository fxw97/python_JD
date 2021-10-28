import pandas as pd

data = pd.read_csv('京东口红信息.csv')

# 给数据加上白头
data.columns = ['ID','name','price','store_name','self_run','url_list','CommentCount','GoodRate']

print(data.drop_duplicates())