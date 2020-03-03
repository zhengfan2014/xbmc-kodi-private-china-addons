
import requests
from bs4 import BeautifulSoup

#首次加载网页
url = 'https://www.pearvideo.com/popular'
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
rec = requests.get(url,headers=headers)
ttmp = rec.text
#从api循环爬出网页，和1合并
urlx = 'https://www.pearvideo.com/popular_loading.jsp'
num = 1
while num < 10:
    startnum = 10
    payload = {'reqType': '1', 'categoryId': '', 'start': startnum*num}
    rec = requests.get(urlx,headers=headers,params=payload)
    ttmp += rec.text
    num += 1


#交给美丽汤循环爬出所有数据
soup = BeautifulSoup(ttmp, 'html.parser')

htmll = soup.find_all('li',class_='popularem clearfix')


print('视频总数：')
print(len(htmll))
#print(htmll)
for index in range(len(htmll)):
    print('视频标题：')
    print(htmll[index].h2.text)
    print('视频地址：')
    print('https://www.pearvideo.com/' + htmll[index].a['href'])
    print('视频图片：')
    imgtmp = htmll[index].find('div',class_='popularem-img')
    print(imgtmp['style'][22:-2])
    print('*-'*30)