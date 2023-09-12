import json
import requests
#设置URL
url = "http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword"
#UA
headers ={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}
#设置参数
i = 1
word = input("请输入一个地址")
for i in range(1,6):
    param = {
        "cname":"" ,
        "pid":"",
        "keyword": word,
        "pageIndex": i,
        "pageSize": 10
    }
    reponse = requests.post(url=url,data=param,headers=headers)
    print(reponse.text)
    with open("KFC.html",'w',encoding='utf-8') as fd:
        fd.write(reponse.text)

    with open("KFCA.json", 'w', encoding='utf-8') as f:
        json.dump(reponse.text,fp=f,ensure_ascii=False)