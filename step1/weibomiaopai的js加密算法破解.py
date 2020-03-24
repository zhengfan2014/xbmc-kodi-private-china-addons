import json 
import requests
import base64
from bs4 import BeautifulSoup

url = 'https://weibomiaopai.com/online-video-download-helper/bilibili'
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
rec = requests.get(url,headers=headers)
rec.encoding = 'utf-8'
rte = rec.text
str1 = rte.find('var freeservice=')
str2 = rte.find('var thepage="bilibili";')
cut = rte[str1+16:str2]
cut = cut.replace('\n','')
cut = cut.replace(';','')
cut = cut.split("' + '")
q = ''
i = 2
while (i < len(cut)):
  q += cut[i]
  i+=3
q =  base64.b64decode(q)
q =str(q, encoding = "utf-8")
print(q)
