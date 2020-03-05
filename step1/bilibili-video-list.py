import json
import requests
import re
from bs4 import BeautifulSoup

url = 'https://www.bilibili.com/video/av91222524'
#多p：https://www.bilibili.com/video/av84351845
#单p：https://www.bilibili.com/video/av91222524/
    
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
mheaders = {'user-agent' : 'Mozilla/5.0 (Linux; Android 10; Z832 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36'}
rec = requests.get(url,headers=headers)
soup = BeautifulSoup(rec.text, 'html.parser')
ifpnum = soup.find_all('div',class_='multi-page report-wrap-module report-scroll-module')
if ifpnum != []:
  print('多p')
  rec = requests.get('http://m'+url[11:],headers=mheaders)
  cutjson =str(rec.text)
  str1 = cutjson.find('window.__INITIAL_STATE__=')
  str2 = cutjson.find('if(window.__INITIAL_STATE__.abserver)')
  videoinfojson = cutjson[str1+25:str2-6]
  #print(videoinfojson)
  j = json.loads(videoinfojson)
  #j是字典
  k = j['reduxAsyncConnect']['videoInfo']['pages']
  #print(len(k))
  #图片
  print(j['reduxAsyncConnect']['videoInfo']['pic'])
  #名
  print(j['reduxAsyncConnect']['videoInfo']['title'])
  #介绍
  print(j['reduxAsyncConnect']['videoInfo']['desc'])
  for index in range(len(k)):
    duration = k[index]['duration']
    min = str(duration//60)
    sec = duration%60-1
    if sec < 10:
      sec = str('0') + str(sec)
    sec = str(sec)
    print('【P' + str(index+1) + '】' + k[index]['part'] + ' - ' + min + ':' + sec)
else:
  #print('单p')
  rec = requests.get(url,headers=headers)
  soup = BeautifulSoup(rec.text, 'html.parser')
  videotitle = soup.find(name='title')
  videoimage = soup.find(itemprop='image')
  videodesc = soup.find(itemprop='description')
  print(str(videoimage['content']))

  print('【P1】' + str(videotitle.text[:-26]))
  
  print(str(videodesc['content']))




