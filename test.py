d =['','剧情','喜剧','恐怖','','伦理','']
d_dropna = list(filter(None, d))    #去除列表空值，非常简单好用

ls = ['a','b','c']
print(''.join(ls)) # 'abc'
'''
注意： 
空字符串 会被程序判定为 False 
'''