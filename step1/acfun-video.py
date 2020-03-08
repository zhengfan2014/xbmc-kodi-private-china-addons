import requests
import json
#多p：https://www.acfun.cn/v/ac3202810_4
#单p：https://www.acfun.cn/v/ac12607834
url = 'https://www.acfun.cn/v/ac3202810_4'
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
rec = requests.get(url,headers=headers)
#print(rec.text)

cutjson = rec.text
str1 = cutjson.find('window.pageInfo = window.videoInfo = ')
str2 = cutjson.find('window.qualityConfig =')
videoinfo = cutjson[str1+37:str2-10]
j = json.loads(videoinfo)

print(j['title'])
print(j['description'])

if len(j['videoList']) == 1:
  #单p
  #print(j['currentVideoInfo']['ksPlayJson'])

  j2 = json.loads(j['currentVideoInfo']['ksPlayJson'])
  for index in range(len(j2)):
    print(j2['adaptationSet']['representation'][index]['qualityType'])
    print(j2['adaptationSet']['representation'][index]['url'])
    print('**********'*30)
else:
  #duop
  for index in range(len(j['videoList'])):
    print(j['videoList'][index]['title'])
  print(j['currentVideoInfo']['ksPlayJson'])