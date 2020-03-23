#视频列表
import json 
import requests
from bs4 import BeautifulSoup

url = 'https://www.xinpianchang.com/channel/index/id-81/sort-pick/type-/duration_type-0/resolution_type-?from=articleListPage'
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
rec = requests.get(url,headers=headers)
#print(rec.text)
soup = BeautifulSoup(rec.text, 'html.parser')
filmitem = soup.find_all('li',class_='enter-filmplay')
for index in range(len(filmitem)):
  img = filmitem[index].find('img',class_='lazy-img')
  title = filmitem[index].find('p',class_='fs_14 fw_600 c_b_3 line-hide-1')
  print(img['_src'])
  print(title.text)
  print(filmitem[index]['data-articleid'])





#获取视频mp4
import json 
import requests
import re
from bs4 import BeautifulSoup

url = 'https://www.xinpianchang.com/a10696100'
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
rec = requests.get(url,headers=headers)
#print(rec.text)
rectext = rec.text
str1 = rectext.find('vid: "')
str2 = rectext[str1:str1+30].find('",')
vid = rectext[str1+6:str1+str2]
api = 'https://openapi-vtom.vmovier.com/v3/video/' + vid + '?expand=resource&usage=xpc_web'
rec = requests.get(api,headers=headers)
j = json.loads(rec.text)
for index in range(len(j['data']['resource']['progressive'])):
  print(j['data']['resource']['progressive'][index]['profile'])
  print('http' + j['data']['resource']['progressive'][index]['url'][5:])





#场库分类
import json 
import requests
from bs4 import BeautifulSoup

url = 'https://www.vmovier.com/channel/idea'
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
rec = requests.get(url,headers=headers)
#print(rec.text)
soup = BeautifulSoup(rec.text, 'html.parser')
filmitem = soup.find('ul',class_='search-works-list clearfix')
filmitem = filmitem.find_all('li')
print(len(filmitem))
for index in range(len(filmitem)):
  print(filmitem[index].img['alt'])
  print(filmitem[index].img['src'])
  print('https://www.vmovier.com' + filmitem[index].a['href'])






  #场库首页和排行榜
import json 
import requests
from bs4 import BeautifulSoup

url = 'https://www.vmovier.com/stars#rotate-nav'
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
rec = requests.get(url,headers=headers)
#print(rec.text)
soup = BeautifulSoup(rec.text, 'html.parser')
filmitem = soup.find('ul',class_='index-list clearfix')
filmitem = filmitem.find_all('li')
print(len(filmitem))
for index in range(len(filmitem)):
  print(filmitem[index].img['alt'])
  print(filmitem[index].img['src'])
  print('https://www.vmovier.com' + filmitem[index].a['href'])







  #场库每日推荐(有报错)
import json 
import requests
from bs4 import BeautifulSoup

url = 'https://www.vmovier.com/'
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
rec = requests.get(url,headers=headers)
#print(rec.text)
soup = BeautifulSoup(rec.text, 'html.parser')
filmitem = soup.find('ul',class_='rotate')
filmitem = filmitem.find_all('li')
print(len(filmitem))
for index in range(len(filmitem)):
  if filmitem[index].img['alt'] != '':

    print(filmitem[index].img['alt'])
    print(filmitem[index].img['src'])
    print(filmitem[index].a['href'])
  