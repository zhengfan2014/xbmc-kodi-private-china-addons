import json
import requests

url = 'https://www.acfun.cn/rest/pc-direct/rank/channel?channelId=155&subChannelId=&rankLimit=30&rankPeriod=WEEK'
    
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
rec = requests.get(url,headers=headers)
#print(rec.text)
j = json.loads(rec.text)
#j是字典
k = j['rankList']
#k是列表对象
print('视频总数：')
print(len(k))

for index in range(len(k)):
    item = k[index]
    print('视频标题：')
    print(item['contentTitle'])
    print('视频图片：')
    print(item['coverUrl'])
    print('视频地址：')
    print(item['shareUrl'])
    print('---'*30)
#写完这个，学到了很多python关于list和dict的东西
#zhengfan2014 于2020/3/2 23.56

    