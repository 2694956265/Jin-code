import requests
#UA伪装
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}
#设置URL
url ="https://www.google.com/search"
kw =input("请输入你想查询的页面")
params = {
    "query": kw
}
#发送请求
reponse = requests.get(url= url,params=params,headers=headers)
#接收数据
page = reponse.text
#保存
with open(kw+'.html','w',encoding='utf-8') as f:
    f.write(page)