import json
import requests
import re
import random
from bs4 import BeautifulSoup
hash = '45de7ffc02c0fdeb49263721999a5dbf'
apilist1=['https://happyukgo.com/','https://helloacm.com/','https://steakovercooked.com/','https://anothervps.com/','https://isvbscriptdead.com/','https://zhihua-lai.com/','https://weibomiaopai.com/','https://steemyy.com/']

url = 'https://m.bilibili.com/video/av84351845'
apiurl = apilist1[random.randint(0,8)]+'api/video/?cached&lang=ch&page=bilibili&hash='+hash+'&video='+url

#print(apiurl)

headers = {'user-agent' : 'Mozilla/5.0 (Linux; Android 10; Z832 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36'}
rec = requests.get(apiurl,headers=headers)
result = eval(repr(rec.text).replace('\\', ''))
#print(result)
j = json.loads(result)
print('【1080P】 FLV - 由' + j['server']+'的api解析')

print(j['url'])

#api2
payload = {'urlav': url}

r = requests.post("https://www.xbeibeix.com/api/bilibili.php",data=payload,headers=headers)
#print(r.text)
soup = BeautifulSoup(r.text, 'html.parser')
videodown = soup.find(download='视频.mp4')

cuthtml1 =str(r.text)
str1 = cuthtml1.find('清晰度：')
str2 = cuthtml1.find('P</p></li>')
apiqingxidu = cuthtml1[str1+7:str2]
print('【'+apiqingxidu+'P】 MP4 - 由xbeibeix.com的api解析')

cuthtml2 =str(r.text)
str1 = cuthtml2.find('封面：')
str2 = cuthtml2.find('ng</p></li>')
apiimage = cuthtml2[str1+3:str2] + 'ng'
print(apiimage)

print('--'*100)
print(videodown['href'])