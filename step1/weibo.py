#热门推荐（纪录片，评测，娱乐都没有）
import json 
import requests
import re
from bs4 import BeautifulSoup
import urllib

url = 'https://weibo.com/video/aj/load?ajwvr=6&page=2&type=channel&hot_recommend_containerid=video_tag_15&__rnd=1584096137063'
cookies = dict(SUB='_2AkMpN-raf8NxqwJRmfoXxGniZIl_ygvEieKfaxsBJRMxHRl-yj92qhFTtRB6ArfENQBVM_xipNLvZYca4pNo4lw7p9Xi')
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
rec = requests.get(url,headers=headers,cookies=cookies)
rec.encoding = 'utf-8'
rectext = rec.text
print(rectext)

num = re.sub(r'\\n', "", rectext)
num = re.sub(r'\\', "", num)
print(num)
soup = BeautifulSoup(num, 'html.parser')
list = soup.find_all('div',class_='V_list_a')
print(len(list))
for index in range(len(list)):
  #soup = BeautifulSoup(list[index], 'html.parser')
  videosource = list[index]['video-sources']

  videosource = urllib.parse.unquote(videosource,encoding='utf-8',errors='replace')
  videosource = urllib.parse.unquote(videosource,encoding='utf-8',errors='replace')
  videosource = videosource[8:]
  mp4 = videosource.split('http:')
  #q = videosource
  imgsrc = list[index].find('img')
  imgsrc = imgsrc['src']
  title = list[index]['action-data']

  str1 = title.find('&title=')
  str2 = title.find('&uid=')
  title = title[str1+7:str2]
  title = urllib.parse.unquote(title,encoding='utf-8',errors='replace')
  print(title)
  print('http:' + imgsrc[6:])
  print('http:' + mp4[0])
  print('*******'*30)














  #编辑推荐
import json 
import requests
import re
from bs4 import BeautifulSoup
import urllib

url = 'https://weibo.com/tv?type=channel&first_level_channel_id=4453781547450385&broadcast_id=4476916414218244'
cookies = dict(SUB='_2AkMpN-raf8NxqwJRmfoXxGniZIl_ygvEieKfaxsBJRMxHRl-yj92qhFTtRB6ArfENQBVM_xipNLvZYca4pNo4lw7p9Xi')
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
rec = requests.get(url,headers=headers,cookies=cookies)
rec.encoding = 'utf-8'
rectext = rec.text
#print(rectext)
soup = BeautifulSoup(rectext, 'html.parser')
list = soup.find_all('div',class_='V_list_a')
for index in range(len(list)):
  videosource = list[index]['video-sources']
  videosource = urllib.parse.unquote(videosource,encoding='utf-8',errors='replace')
  videosource = urllib.parse.unquote(videosource,encoding='utf-8',errors='replace')
  videosource = videosource[8:]
  mp4 = videosource.split('http:')
  img = list[index].find('img')
  img = img['src']
  if img[0:4] == 'http':
    img = 'http' + img[5:]
  else:
    img = 'http:' + img
  title = list[index].find('h3')
  print(title.text)
  print(img)
  print('http:' + mp4[len(mp4)-1])





#排行榜
import json 
import requests
import re
from bs4 import BeautifulSoup
import urllib

url = 'https://weibo.com/tv?type=dayrank'
cookies = dict(SUB='_2AkMpN-raf8NxqwJRmfoXxGniZIl_ygvEieKfaxsBJRMxHRl-yj92qhFTtRB6ArfENQBVM_xipNLvZYca4pNo4lw7p9Xi')
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
rec = requests.get(url,headers=headers,cookies=cookies)
rec.encoding = 'utf-8'
rectext = rec.text
#print(rectext)
soup = BeautifulSoup(rectext, 'html.parser')
list = soup.find_all('div',class_='V_list_a')
for index in range(len(list)):
  videosource = list[index]['video-sources']
  videosource = urllib.parse.unquote(videosource,encoding='utf-8',errors='replace')
  videosource = urllib.parse.unquote(videosource,encoding='utf-8',errors='replace')
  videosource = videosource[8:]
  mp4 = videosource.split('http:')
  img = list[index].find('img')
  img = img['src']
  if img[0:4] == 'http':
    img = 'http' + img[5:]
  else:
    img = 'http:' + img
  title = list[index].find('h3')
  title = title.text
  title = title.replace(' ', '').replace('\n','')
  if len(title) > 40:
    title = title[:40] + '...'
  print(title)
  print(img)
  print('http:' + mp4[len(mp4)-1])




#故事
import json 
import requests
import re
from bs4 import BeautifulSoup
import urllib

url = 'https://weibo.com/tv?type=story'
cookies = dict(SUB='_2AkMpN-raf8NxqwJRmfoXxGniZIl_ygvEieKfaxsBJRMxHRl-yj92qhFTtRB6ArfENQBVM_xipNLvZYca4pNo4lw7p9Xi')
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
rec = requests.get(url,headers=headers,cookies=cookies)
rec.encoding = 'utf-8'
rectext = rec.text
#print(rectext)
soup = BeautifulSoup(rectext, 'html.parser')
list = soup.find_all('div',class_='V_list_b')
for index in range(len(list)):

  #print(list[index])

  if list[index]['action-data'][:9] != 'type=live':


    videosource = list[index]['video-sources']
    videosource = urllib.parse.unquote(videosource,encoding='utf-8',errors='replace')
    videosource = urllib.parse.unquote(videosource,encoding='utf-8',errors='replace')
    videosource = videosource[8:]
    mp4 = videosource.split('http:')
    img = list[index].find('img')
    img = img['src']
    if img[0:4] == 'http':
      img = 'http' + img[5:]
    else:
      img = 'http:' + img
    like = list[index].find('div',class_='like')
    like = like.text
    likenum = re.findall(r'\d+',like)
    print(str(likenum[0] + '赞'))
    print(img)
    print('http:' + mp4[len(mp4)-1])

    
  else:
    index = index +1