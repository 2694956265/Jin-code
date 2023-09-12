import requests
from bs4 import BeautifulSoup
import pandas
import re
url = "https://www.biquge.co/0_998/"
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}
def get_novel():
    res = requests.get(url=url,headers=headers)
    res.encoding  ="gbk"
    soup = BeautifulSoup(res.text,"html.parser")
    so = soup.find("div",id="list").find_all("dd")
    data=list()
    for content in so[295:] :
        content = content.find("a")
        if not content:
            continue
        # print(content)
        data.append(("https://www.biquge.co%s" %(content["href"]),content.get_text()))
    return data
        # urls = content.get("href")
        # ur = "https://www.biquge.co%s" %(urls)
        # print(ur)
        # # print(ur)
        # rese = requests.get(url=ur, headers=headers).text.encode('iso-8859-1')
        # sou = BeautifulSoup(rese.text, "html.parser")
        # s = sou.find("div", class_="bookname").find("h1").get_text()
        # bsoup = sou.find("div", id="content").get_text()
        # print(s)
        # with open("%s.txt" % (s), "w") as f:
        #     f.write(bsoup)
def get_cha(url):
    r =requests.get(url=url,headers=headers)
    r.encoding="gbk"
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.find("div",id = "content").get_text().replace("\xa0","")
#.replace(u"\xa0","")

if __name__ == '__main__':
   for cha in get_novel():
       url,title = cha
       print(title)
       title = re.sub(r"[?\\/|<>:*\"]", "", title)
       with open("%s.txt"%title,"w",encoding="utf-8") as f:
           f.write(get_cha(url))


