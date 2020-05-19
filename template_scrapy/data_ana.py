import pandas as pd
from pymongo import MongoClient

client = MongoClient()
collection = client['my_test']['crawl_sun']

data = collection.find()
data_list = []
for i in data:
    temp = {}
    temp["number"]= i["number"]
    temp["in_url"] = i["in_url"]
    temp["content_pic"] = i['content_pic']
    data_list.append(temp)

df = pd.DataFrame(data_list)
# print(df)

#显示头几行
print(df.head(1))


#展示df的概览
# print(df.info())
# print(df.describe())

