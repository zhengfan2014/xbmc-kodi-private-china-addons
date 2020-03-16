
#编辑推荐视频列表
import json 
import requests
from bs4 import BeautifulSoup

url = 'https://www.taptap.com/webapiv2/video/v1/refresh?type=editors_choice&from=1&limit=10&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC'
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
rec = requests.get(url,headers=headers)
#print(rec.text)
j = json.loads(rec.text)
#print(j['data'])

for index in range(len(j['data']['list'])):
  imgurl = j['data']['list'][index]['image']['url']
  id = j['data']['list'][index]['id']
  print(j['data']['list'][index]['title'])
  print('http' + imgurl[5:])
  print('https://taptap.com/video/' + str(id))







#为你推荐视频列表
import json 
import requests
from bs4 import BeautifulSoup

url = 'https://www.taptap.com/webapiv2/video/v1/refresh?type=recommend&from=0&limit=30&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC'
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
rec = requests.get(url,headers=headers)
#print(rec.text)
j = json.loads(rec.text)
#print(j['data'])

for index in range(len(j['data']['list'])):
  imgurl = j['data']['list'][index]['data']['image']['url']
  id = j['data']['list'][index]['data']['id']
  print(j['data']['list'][index]['data']['title'])
  print('http' + imgurl[5:])
  print('https://taptap.com/video/' + str(id))






#由视频链接爬出视频m3u8

import json 
import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.taptap.com/video/1310782'
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
rec = requests.get(url,headers=headers)
rectext = rec.text
str1 = rectext.find('{url:B,url_h265:')
str2 = rectext.find(',url_expires:C}')
#print(rectext[str1+17:str2-1])
mainm3u8 = rectext[str1+17:str2-1]
#print(type(mainm3u8))
mainm3u8 = mainm3u8.replace(r'\u002F','/')


#print(mainm3u8)
#j = json.loads(rec.text)
#print(j['data'])

rec = requests.get(mainm3u8,headers=headers)
rectext = rec.text
#print(rectext)

prule = re.compile(r'\d+[p|k]\d?\d?')   # 查找数字
pname = prule.findall(rectext)

urlrule = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')   # 查找数字
m3u8url = urlrule.findall(rectext)
cuttext = rectext
#print(m3u8url)
for index in range(len(m3u8url)):
  print(pname[index])
  print(m3u8url[index])
  print('-----------'*30)