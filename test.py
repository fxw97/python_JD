import pandas as pd
df=pd.DataFrame(columns=['a','b','c'])
for i in range(1,4):
    dic={'a':1,'b':2,'c':3}
    data = pd.DataFrame(dic,index=[0])
    df = pd.concat([df,data],axis=0)
print(df)
