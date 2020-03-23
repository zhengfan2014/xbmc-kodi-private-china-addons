#视频列表
import json 
import requests
from bs4 import BeautifulSoup

url = 'http://open.nlc.cn/onlineedu/course/explore/search.htm?filter=subject&subjectId=1001&orderBy=latest'
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
rec = requests.get(url,headers=headers)
#print(rec.text)
soup = BeautifulSoup(rec.text, 'html.parser')
courseitem = soup.find_all('div',class_='course-item')
for index in range(len(courseitem)):
  img = courseitem[index].find('img',class_='img-responsive')
  title = courseitem[index].find('a',class_='link-dark')
  titletext = title.text
  titletext = titletext.strip()
  titletext = titletext.replace('\n', '').replace('\r', '')
  print(titletext)
  print('http://open.nlc.cn' + img['src'])
  print('http://open.nlc.cn' + title['href'])
  print('------'*30)





#多p
import json 
import requests
from bs4 import BeautifulSoup

url = 'http://open.nlc.cn/onlineedu/course/detail/lesson/list.htm?courseid=4916'
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
rec = requests.get(url,headers=headers)
#print(rec.text)
soup = BeautifulSoup(rec.text, 'html.parser')
courseitem = soup.find_all('li',class_='period lesson-item')
for index in range(len(courseitem)):
  link = courseitem[index].find('a')
  title = courseitem[index].find('span',class_='title')
  print(title.text)
  print('http://open.nlc.cn' + link['href'])
  





#video url
import json 
import requests
from bs4 import BeautifulSoup

url = 'http://open.nlc.cn/onlineedu/course/play.htm?id=10497'
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
rec = requests.get(url,headers=headers)
#print(rec.text)
soup = BeautifulSoup(rec.text, 'html.parser')
videolist = soup.find('div',class_='lesson-dashboard lesson-dashboard-open')
print()
print()
api = 'http://open.nlc.cn/onlineedu/course/plugin/lesson/play.htm?lessonId=' + str(videolist['data-lesson-id']) + '&fileId=' + str(videolist['data-file-id'])
rec = requests.get(api,headers=headers)
j = json.loads(rec.text)
videourl = j['coursefile']['clarity4']
vidnum = videourl[-6:-5]
print(vidnum)
if vidnum != 2:
  vidnum = int(vidnum) - 1
  qxd = ['标清540p','高清720p','超清1080p']
  for index in range(vidnum):
    print(qxd[index])
    print(videourl[:-6] + str(index+1) + '.mp4')
  print('ok')





