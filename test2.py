import requests
from bs4 import BeautifulSoup
url = "https://www.google.com/search?q=bilibili"
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}
res = requests.get(url=url,headers=headers)
re = res.text
soup = BeautifulSoup(re,"html.parser")
content = soup.find("h3",class_="LC20lb MBeuO DKV0Md")
if content is not None:
    print(content.get_text())
else:
    print("Content not found.")