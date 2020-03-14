#爬视频列表
import json 
import requests
from bs4 import BeautifulSoup

url = 'https://www.thepaper.cn/load_video_chosen.jsp?channellID=26916&nodeid=26913&pageidx=1'
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
rec = requests.get(url,headers=headers)
#print(rec.text)

soup = BeautifulSoup(rec.text, 'html.parser')

imgsrc = soup.find_all('img')
ahref = soup.find_all('a',class_='play has_pic')
title = soup.find_all('div',class_='video_title')
for index in range(len(imgsrc)):
  titletext = title[index].text
  titletext = titletext.replace('	', '')
  imgsrcurl = imgsrc[index]['src']
  print('http' + imgsrcurl[5:])
  print('https://thepaper.cn/' + ahref[index]['href'])
  print(titletext)
  print('-----------'*30)






#爬视频地址
import requests
from bs4 import BeautifulSoup

url = 'https://www.thepaper.cn/newsDetail_forward_6437339'
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
rec = requests.get(url,headers=headers)

soup = BeautifulSoup(rec.text, 'html.parser')
#print(rec.text)
mp4 = soup.find('source',type='video/mp4')
print(mp4['src'])