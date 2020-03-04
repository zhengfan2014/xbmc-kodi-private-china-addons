#b站爬番剧列表
import json
import requests
import re
from bs4 import BeautifulSoup

url = 'https://m.bilibili.com/bangumi/play/ss29366'
    
headers = {'user-agent' : 'Mozilla/5.0 (Linux; Android 10; Z832 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36'}
rec = requests.get(url,headers=headers)
soup = BeautifulSoup(rec.text, 'html.parser')
htmll = soup.find_all('script')


#切出番剧信息的json
cutjson =str(rec.text)
str1 = cutjson.find('window.__INITIAL_STATE__=')
str2 = cutjson.find(';(function(){var s;')
videoinfojson = cutjson[str1+25:str2]
#print(videoinfojson)

j = json.loads(videoinfojson)
#j是字典
k = j['epList']
print(len(k))
for index in range(len(k)):
    item = k[index]
    print('视频标题：')
    print(item['long_title'])
    print('视频图片：')
    print(item['cover'])
    print('视频地址：')
    print(item['link'])
    print('---'*30)