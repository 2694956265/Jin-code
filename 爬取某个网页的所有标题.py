import requests
from bs4 import BeautifulSoup
import re
from urils import url_manager

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

cookies ={
    "captchakey":"14a54079a1",
    "captchaExpire" : "1548852352"
}
#设置初始的根url
root_url =  "http://www.crazyant.net"

#初始化了url管理器
urls = url_manager.UrlManager()
urls.add_new_url(root_url)
#打开一个文本
f = open("./title.txt","w",encoding="utf-8")

#不断运行url管理器
while urls.has_new_url():
    url = urls.get_url()
    response = requests.get(url=url, headers=headers,cookies=cookies,timeout=3)
    #判断response是否有效
    if response.status_code != 200:
        print(f"出错啦，这个回应的状态码可不对哦，这个url是{url}")
        continue
    #开始用soup分析
    soup = BeautifulSoup(response.text,"html.parser")
    #找出这里的超链接
    title = soup.title.string
    f.write(f"{url} {title}\n")
    f.flush()
    print(f"已成功写入,{url} {title}{len(urls.new_urls)}")

    #继续寻找其他的超链接
    searchs = soup.find_all("a")
    rules = r'^http://www.crazyant.net/\d*.html$'
    for search in searchs:
        s = search.get("href")
        if s is None:
            continue
        if re.match(rules,s)  :
            urls.add_new_url(s)
f.close()



