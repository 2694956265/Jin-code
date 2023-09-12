import requests
import json
#设置URL
url = "https://fanyi.baidu.com/sug"
#设置UA伪装
headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/117.0.0.0 XMLHttpRequest"
}
word = input("请输入一个单词")
data = {
    "kw" : word
}
#发送qingqiu
reponse = requests.post(url=url,data=data,headers=headers)
#得到回应
re = reponse.json()
print(type(re))
print(re)
filename = word + '.json'
# 保存文档
f = open(filename,'w',encoding='utf-8')
json.dump(re,fp=f,ensure_ascii=False)
f.close()