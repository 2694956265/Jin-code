import requests
from bs4 import BeautifulSoup
header = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}
res = requests.get("http://www.sina.com.cn",headers=header)
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text,"html.parser")
soups = soup.select('a')
for l in soups:
    print(l)


#print(res.text)
