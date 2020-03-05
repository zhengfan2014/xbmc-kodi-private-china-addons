#bangumi-list和video-list的整合
#!/usr/bin/python
# -*- coding: UTF-8 -*- 
from bs4 import BeautifulSoup
import re
import requests
import json

headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
mheaders = {'user-agent' : 'Mozilla/5.0 (Linux; Android 10; Z832 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36'}
url = 'https://www.bilibili.com/bangumi/play/ss29366/'

#多p：https://www.bilibili.com/video/av84351845
#单p：https://www.bilibili.com/video/av91222524/


if re.match('https://',url) == None:
  if re.match('http://',url) != None:
    url = 'https://'+url[7:]
  else:
    print('无法解析')

ifbangumiurl = re.match('https://www.bilibili.com/bangumi/play/ss',url)
ifvideourl = re.match('https://www.bilibili.com/video/av',url)
if ifbangumiurl or ifvideourl != None:
  if ifbangumiurl != None:
    
    rec = requests.get('http://m'+url[11:],headers=mheaders)
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




  else:
    print('视频')
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





else:
  print('不支持的B站链接')