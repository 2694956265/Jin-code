import requests
from bs4 import BeautifulSoup
import pandas
import lxml
url = "http://tianqi.2345.com/Pc/GetHistory"
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

def get_data_weather(year,month):
    all_data = []
    for ye in range(year - 9, year + 1):
        for mo in range(1,13):
            if ye == year and mo > month :
                break
            else:
                params ={
                    "areaInfo[areaId]": 54527,
                    "areaInfo[areaType]": 2,
                    "date[year]": ye,
                    "date[month]": mo
                }
                res = requests.get(url=url,headers=headers,params=params)
                if res.status_code != 200 :
                    raise Exception("error")
                else:
                    html = res.json()["data"]#字典->字符串
                    # print(html)
                    print(type(html),type(res.json()))
                    rd = pandas.read_html(html)[0]#列表->dataframe
                    print(type(rd),type(pandas.read_html(html)))
                    print(rd)
                    print(ye, mo)

                    all_data.append(rd)
                    # print(type(all_data))
    return all_data
if __name__ == '__main__':
    all_data = get_data_weather(2023,9)
    # df = pandas.DataFrame(all_data)
    # df.to_excel("天津近十年的天气.xlsx",index=False)
    pandas.concat(all_data).to_excel("天津十年天气.xlsx",index=False)