#31行没get_text()
import requests
from bs4 import BeautifulSoup
import pandas
import pprint
import json
import openpyxl
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}
all_datas = []
htmls = []
#这个是获取这十页的网址
def download_htmls():
    for i in range(0,250,25):
        url = f"https://movie.douban.com/top250?start={i}&filter="
        res = requests.get(url=url,headers=headers,timeout=3)
        if res.status_code != 200:
            raise Exception("error")
        else:
            print(f"现在的url是{url}")
            htmls.append(res.text)
    return htmls

#解析每一页
def parse_single_html(html):
    soup = BeautifulSoup(html,"html.parser")
    artical_items = soup.find("div",class_="article").find("ol",class_="grid_view").find_all("div",class_="item")
    datas=[]
    for artical_item in artical_items:
        rank = (artical_item.find("div",class_="pic").find("em")).get_text()
        info = (artical_item.find("div",class_="info"))
        title =(info.find("div",class_="hd").find("span",class_="title").get_text())
        stars=(info.find("div",class_="star").find_all("span"))
        rating_star = stars[0]["class"][0]
        rating_num = stars[1].get_text()
        comment = stars[3].get_text()
        datas.append({
            "rank":rank,
            "title": title,
            "rating_star": rating_star.replace("rating","").replace("-t",""),
            "rating_num": rating_num,
            "comment": comment.replace("人评价","")
        })
    return datas

if __name__ == '__main__':
    download_htmls()
    for i in range(0,10):
        pprint.pprint(parse_single_html(htmls[i]))
    for html in htmls:
        all_datas.extend(parse_single_html(html))
        print("all_data",all_datas)
    df = pandas.DataFrame(all_datas)
    print(df)
    df.to_excel("豆瓣电影top250.xlsx")




