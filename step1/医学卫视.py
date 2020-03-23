#视频列表
import json 
import requests
from bs4 import BeautifulSoup

url = 'https://www.mvyxws.com/'
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
rec = requests.get(url,headers=headers)
cag=1
#print(rec.text)
soup = BeautifulSoup(rec.text, 'html.parser')
filmitem = soup.find_all('div',class_='category')
#print(filmitem[cag])
filmitem = filmitem[cag].find_all('a')
print(len(filmitem))
for index in range(len(filmitem)):
  print(filmitem[index]['title'])
  print('https://www.mvyxws.com'+filmitem[index]['href'])

  


  #多p
import json 
import requests
from bs4 import BeautifulSoup

url = 'https://www.mvyxws.com/vod/disease?cid=718'
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
rec = requests.get(url,headers=headers)
cag=1
#print(rec.text)
soup = BeautifulSoup(rec.text, 'html.parser')
filmitem = soup.find('ul',class_='jb-list')
#print(filmitem[cag])
filmitem = filmitem.find_all('li')
print(len(filmitem))
for index in range(len(filmitem)):
  print(filmitem[index].a['title'])
  print('https://www.mvyxws.com'+filmitem[index].a['href'])

  

  #取出mp4
import re
import json 
import requests
from bs4 import BeautifulSoup

url = 'https://www.mvyxws.com/vod/play/id/12279'
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
rec = requests.get(url,headers=headers)
#print(rec.text)
rect = rec.text
str1 = rect.find('fileID:')
str2 = rect.find('appID:')
str3 = rect.find('player.currentTime(0);')
fileid = re.search(r'\d+',rect[str1:str2]).group()
appid = re.search(r'\d+',rect[str2:str3]).group()
rec = requests.get('https://playvideo.qcloud.com/getplayinfo/v2/' + appid + '/' + fileid,headers=headers)
j = json.loads(rec.text)
print()
for index in range(len(j['videoInfo']['transcodeList']) - 1):
  num = len(j['videoInfo']['transcodeList'])
  print(j['videoInfo']['transcodeList'][num - index - 1]['height'])
  print(j['videoInfo']['transcodeList'][num - index - 1]['url'])