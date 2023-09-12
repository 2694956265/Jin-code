import requests
import re
from bs4 import BeautifulSoup

# 首页的URL
url = 'http://cic.tju.edu.cn/szdw/szmd/azmjs.htm'

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

# 发送GET请求
response = requests.get(url=url,headers=headers)

# 设置正确的文本编码
response.encoding = "utf-8"

# 解析HTML
soup = BeautifulSoup(response.text, 'html.parser')

# 找到所有教师的链接, 这里需要你根据实际的HTML结构来定位和选择
teacher_link = soup.find('div',class_="con_list_body")
teachers = teacher_link.find_all('a',target='_blank')
for teacher in teachers:
    get_tlink = teacher['href']
    # print(teacher.get_text())
    print("-"*40)
    url1 = get_tlink
    url2 =  str(url1)
    url3 = url2.strip("../../")
    response1 = requests.get(url="http://cic.tju.edu.cn/"+url3,headers=headers)
    response1.encoding = "utf-8"
    soup1 = BeautifulSoup(response1.text,"html.parser")
    gt=soup1.find("div",class_="v_news_content")
    gt1 = gt.find_all("p")
    for g in gt1:

        print(g.get_text().replace(u'\xa0', ''))