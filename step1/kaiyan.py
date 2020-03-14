#开眼每日精选
import requests
import json
url = 'http://baobab.kaiyanapp.com/api/v5/index/tab/allRec?page=0'
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
rec = requests.get(url,headers=headers)
#print(rec.text)

j = json.loads(rec.text)
#标题
print(j['itemList'][0]['data']['header']['title'] + ' - ' + j['itemList'][0]['data']['header']['subTitle'])
#视频数：
#print(j['itemList'][0]['data'])
for index in range(len(j['itemList'][0]['data']['itemList'])):
  #标题
  print(j['itemList'][0]['data']['itemList'][index]['data']['content']['data']['title'])
  #图片
  print(j['itemList'][0]['data']['itemList'][index]['data']['content']['data']['cover']['feed'])
  #mp4
  print(j['itemList'][0]['data']['itemList'][index]['data']['content']['data']['playUrl'])


for index in range(len(j['itemList'])):
  if j['itemList'][index]['type'] == 'videoSmallCard' or j['itemList'][index]['type'] == 'FollowCard':
    print(j['itemList'][index]['data']['category']+'] - ' + j['itemList'][index]['data']['title'])
    print(j['itemList'][index]['data']['cover']['feed'])
    print(j['itemList'][index]['data']['playUrl'])






    #开眼排行榜 /周
import requests
import json
listnum = 8
num = 0
while listnum == 8:
  
  url = 'http://baobab.kaiyanapp.com/api/v4/rankList/videos?strategy=weekly&num=8&start=' + str(num*8)
  #monthly 月
  headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
  rec = requests.get(url,headers=headers)
  #print(rec.text)

  j = json.loads(rec.text)
  listnum = len(j['itemList'])
  num += 1
  for index in range(len(j['itemList'])):
    #标题
    print(j['itemList'][index]['data']['category'] + ' - ' + j['itemList'][index]['data']['title'])
    #图片
    print(j['itemList'][index]['data']['cover']['feed'])
    #mp4
    print(j['itemList'][index]['data']['playUrl'])










#专题页面解析（多p）
import requests
import json
id = 488
url = 'https://baobab.kaiyanapp.com/api/v3/lightTopics/webPage/' + str(id)
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
rec = requests.get(url,headers=headers)
#print(rec.text)

j = json.loads(rec.text)
for index in range(len(j['itemList'])):
  print(j['itemList'][index]['data']['title'])
  print(j['itemList'][index]['data']['cover']['feed'])
  print(j['itemList'][index]['data']['playUrl'])











  #专题列表解析
import requests
import json
import urllib
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
url = 'http://baobab.kaiyanapp.com/api/v3/specialTopics?start=0&num=10'
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
rec = requests.get(url,headers=headers)
rec.encoding = 'utf-8'
j = json.loads(rec.text)
for index in range(len(j['itemList'])):
  zhuantiurl = str(j['itemList'][index]['data']['actionUrl'])

  cutjson = zhuantiurl.find('url=')
  zhuantiurl = zhuantiurl[cutjson+4:]
  str1 = zhuantiurl.find('nid%3D')
  str2 = zhuantiurl.find('%26')
  id = zhuantiurl[str1+6:str2]
  print(id)

  
  r = requests.get('https://baobab.kaiyanapp.com/api/v3/lightTopics/webPage/' + str(id),headers=headers)

  jo = json.loads(r.text)
  print(jo['brief'])
  print(j['itemList'][index]['data']['image'])
  print('https://www.eyepetizer.net/videos_article.html?nid='+str(id))
  #print(j['itemList'][index]['data']['playUrl'])