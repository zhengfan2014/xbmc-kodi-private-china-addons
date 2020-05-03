# VID for kodi
## 简介
- vid插件是一个模块化，方便不是很懂kodi的python新手快速开发的插件，python新手无需知道kodi相关知识，只需知道一点python知识和遵循一定规则，即可为本插件增加和维护网站  
## 入门
为vid新增网站非常简单，只需要在get_categories函数中添加相关信息，并创建三个函数，并按规则return出对应结果即可  

我们以环球网为例子，演示为vid插件编写观看环球网网站视频的功能 

![](https://pic.downk.cc/item/5eae4e67c2a9a83be56fd4ef.png)

### 1.修改get_categories()

首先，我们找到get_categories函数

```python
def get_categories():
    return [{'id':1,'name':'虎嗅 huxiu.com','link':'huxiu'},
            {'id':2,'name':'机核 gcores.com','link':'gcore'},
            {'id':3,'name':'穷游 qyer.com','link':'qyer'},
            {'id':4,'name':'ZEALER zealer.com','link':'zeal'},
            {'id':5,'name':'澎湃 thepaper.cn','link':'pengpai'},
            {'id':6,'name':'新京报 bjnews.com.cn','link':'bjnews'},
            {'id':7,'name':'界面 jiemian.com','link':'jiemian'},
            {'id':8,'name':'36kr 36kr.com','link':'36kr'}]
```
我们观察得知，get_categories()返回一个python列表 [...] ,列表内套娃一个python字典 {...}   

我们仿照上面，构造一个python字典，放在get_categories()里

```python
{'id':9,'name':'环球 huanqiu.com','link':'huanqiu'}
```

|  参数   | 格式 |
|  :----:  | :----  |
| id     | 数字(int),值必须且为非0的正值，大小不限，甚至可以重复，第一次列表排序根据此值从小到大来排序 |
| name  | 字符串(str),值必须但不限制，用来在首页显示你编写的网站的名字 |
| link  | 字符串(str),值必须且唯一，不得与get_categories函数中其他link的值重复，是你网站在vid插件中的唯一标识符 |

完成效果：

```python
def get_categories():
    return [{'id':1,'name':'虎嗅 huxiu.com','link':'huxiu'},
            {'id':2,'name':'机核 gcores.com','link':'gcore'},
            {'id':3,'name':'穷游 qyer.com','link':'qyer'},
            {'id':4,'name':'ZEALER zealer.com','link':'zeal'},
            {'id':5,'name':'澎湃 thepaper.cn','link':'pengpai'},
            {'id':6,'name':'新京报 bjnews.com.cn','link':'bjnews'},
            {'id':7,'name':'界面 jiemian.com','link':'jiemian'},
            {'id':8,'name':'36kr 36kr.com','link':'36kr'},
            {'id':9,'name':'环球 huanqiu.com','link':'huanqiu'}]
```

### 2.新增三个函数

完成第一步之后，我们还需要创建对应三个函数，格式为 get_xx_videos ,xx为上一步设定的link

```python
def get_huanqiu_videos(page):
    videos = []
    return videos
```
⬆ get_huanqiu_videos(page)  函数是用于爬取并输出视频列表的函数，它输出一个python列表，里面套娃python字典


```python
def get_huanqiu_mp4info(url):
    mp4info ={}
    mp4info['img'] = ''
    return mp4info
```
⬆ get_huanqiu_mp4info(url) 函数是用于输出视频详细信息的函数，它输出一个python字典，字典除了img是必须的，其他都是可选值，具体的参数和值可以参考kodi的setinfo

|  传出参数   | 格式 |
|  :----:  | :----  |
| img     | 字符串,用于展示视频的图片，值必须存在，但可设为空 |


```python
def get_huanqiu_mp4(url):
    mp4 = ''
    return mp4
```
⬆ get_huanqiu_mp4(url) 函数用于解析并输出视频的真实地址，提供给kodi播放

### 3.抓包环球网，找到接口

首先，在完善get_huanqiu_videos(page)前，我们肯定要知道，环球网网站是怎么输出视频列表的，才能对症下药，写出对应的get_huanqiu_videos(page)代码。

那么第一步，就是用chrome打开环球网视频的网站

v.huanqiu.com

![](https://pic.downk.cc/item/5eae4e67c2a9a83be56fd4ef.png)

然后我们正常浏览网页，观察环球网是如何加载新的视频列表的

我们发现，不断下滑网页，网页会不断增加新的视频列表

这时，我们猜到，网页是动态加载的，我们按下F12,在network中寻找那个请求新的网页的api

![](https://pic.downk.cc/item/5eae5294c2a9a83be572f203.png)

看，我们找到那个视频列表的api了，它返回的是json的数据，我们多下滑几次，让网页多请求新的视频列表，观察请求头的规律

![](https://pic.downk.cc/item/5eae5087c2a9a83be57195f0.jpg)
![](https://pic.downk.cc/item/5eae50bbc2a9a83be571b816.jpg)

看到没，offset就是环球网视频列表接口的关键参数，以20递增,第一页offset是0，第二页offset是20，以此类推

这时，我们有了足够的情报，可以尝试完善get_huanqiu_videos(page) 了


 **接下来的调试，我推荐新手在Google的colab上进行调试，调试ok时，再移植到kodi插件上，有基础可以直接跳下一步**

### 4.在Google colab上调试代码


Google colab地址：https://colab.research.google.com/

打开网页后，新建notebook

![](https://pic.downk.cc/item/5eae63e7c2a9a83be57fb596.png)

然后，在代码区加上
```python
import requests
from bs4 import BeautifulSoup
import json
headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
```

![](https://pic.downk.cc/item/5eae6433c2a9a83be57ff886.png)
这些是比较常用的python模块和变量，加完就可以直接调试了

然后我们新增两个变量page和url  
page变量是页数的意思，当用户访问第一页的环球网视频时，它为1，访问第二页的环球网视频时，它为2  
但是因为环球网构造请求url里表示翻页的参数第一页是0，第二页是20，所以，我们写了这样一条表达式

这样，当page传入1时，url中的offset为0

```python
page = 1
page = 10*(int(page)-1)
url='https://v.huanqiu.com/api/list?node=%22/e3pmh2fmu/e3pmh2g69%22,%22/e3pmh2fmu/e3pn61vrg%22,%22/e3pmh2fmu/e3prkldqd%22,%22/e3pmh2fmu/e3prvucof%22,%22/e3pmh2fmu/e3ptgqp01%22,%22/e3pmh2fmu/e3ptgqp01/e3ptrminr%22&offset='+str(page)+'&limit=20'
```
接下来，我们依次新增这两个函数

```python
r = requests.get(url,headers=headers)
j = json.loads(r.text)
```

 requests.get() 是python的用于处理html的模块下的函数， requests.get()主要处理get请求，传入的url是要访问url的地址，headers是访问网页用到的ua

json.loads() 是python的用于处理json的模块下的函数，json.loads()可以把字符串形式的json内容变成python字典，便于调用

在代码的最后加入一行print(j)，点下我用surface pen 圈起来那个按钮

![](https://pic.downk.cc/item/5eae64bcc2a9a83be58063fc.png)

稍等片刻，就可以print出 j 这个变量的值了

看，它成功返回环球网接口的值了

![](https://pic.downk.cc/item/5eae6596c2a9a83be5811a3e.png)

这表示我们的代码是完全正确的，我们可以接着写下去。


然后，我们观察之前那个接口返回的结果

![](https://pic.downk.cc/item/5eae5294c2a9a83be572f203.png)

所有的数据都在list里面，所以我们要写一个循环，把每个数据循环出来
循环这部分，就需要用到一点抽象思维了
想象一下有一个vlist[]
里面包裹着三个字典  
```python
vlist = [{'name':'name1'},{'name':'name2'},{'name':'name3'}]
```

我们该怎么循环它们出来呢？  
是不是得从第1个取出name1，第二个取出name2... ？  
我们知道python的列表取第一个list是：
```python
vlist = [{'name':'name1'},{'name':'name2'},{'name':'name3'}]
vlist[0]
```
python的字典取name值是：
```python
dict = {'name':'name1'}
dict['name']
```

那么，把它们结合起来，取vlist列表第一个字典里的name值就是：
```python
vlist = [{'name':'name1'},{'name':'name2'},{'name':'name3'}]
vlist[0]['name']
```
由以上我们知道，循环输出所有vlist中name值的关键，在于vlist[0]中的[0],只要我们能让它在每循环一次时变化该值，就可以实现我们的目的。

我们使用python的for函数，range函数和len函数来实现  

```python
for index in range(len(vlist)):
    print(vlist[index]['name'])
```

| 用到的函数 | 函数简介 |
| ---- | ---- |
[ for函数](https://www.runoob.com/python/python-for-loop.html) | Python for循环可以遍历任何序列的项目，如一个列表或者一个字符串。
[ len函数](https://www.runoob.com/python/att-list-len.html)： | len() 方法返回列表元素个数。
[range函数](https://www.runoob.com/python/python-func-range.html) | python range() 函数可创建一个整数列表，一般用在 for 循环中。

以上可能很复杂，也许你看不懂，但是没关系，只要你会用就行了。python和高中数学差不多，你不需要完全理解其中的过程，只需知道遇到这种情况套这条公式就可以，至于代码，写的多了自然能慢慢领悟

接下来，我们把它做一点小小的改动，让它输出环球网的视频标题，图片url和新闻链接

```python
page = 1
page = 10*(int(page)-1)
url='https://v.huanqiu.com/api/list?node=%22/e3pmh2fmu/e3pmh2g69%22,%22/e3pmh2fmu/e3pn61vrg%22,%22/e3pmh2fmu/e3prkldqd%22,%22/e3pmh2fmu/e3prvucof%22,%22/e3pmh2fmu/e3ptgqp01%22,%22/e3pmh2fmu/e3ptgqp01/e3ptrminr%22&offset='+str(page)+'&limit=20'

r = requests.get(url,headers=headers)
j = json.loads(r.text)

vlist = j['list']
for index in range(len(vlist)):
    print(vlist[index]['title'])
    print(vlist[index]['cover'])
    print('https://v.huanqiu.com/article/' + str(vlist[index]['aid']))
```

![](https://pic.downk.cc/item/5eae9257c2a9a83be59f0089.png)

这段代码成功循环输出所有的视频标题，图片url和新闻的url，但是，它却报错这一行代码有keyerror错误   
```python
print(vlist[index]['title'])
```
是这一行代码有问题吗，如果有问题，为什么前面的循环可以正常输出呢？

我们重新看环球网的接口

![](https://pic.downk.cc/item/5eae9372c2a9a83be59fa8f0.png)

第20那里，是空的！也就是说当初循环时len(vlist)是21，可是21，也就是vlist[20]，却是空的，这导致了
```python
print(vlist[index]['title'])
```
不能在空的vlist[20]里找到['title']的值，导致报错  
所以，我们让len(vlist)的值减1

```python
page = 1
page = 10*(int(page)-1)
url='https://v.huanqiu.com/api/list?node=%22/e3pmh2fmu/e3pmh2g69%22,%22/e3pmh2fmu/e3pn61vrg%22,%22/e3pmh2fmu/e3prkldqd%22,%22/e3pmh2fmu/e3prvucof%22,%22/e3pmh2fmu/e3ptgqp01%22,%22/e3pmh2fmu/e3ptgqp01/e3ptrminr%22&offset='+str(page)+'&limit=20'

r = requests.get(url,headers=headers)
j = json.loads(r.text)

vlist = j['list']
for index in range(len(vlist)-1):
    print(vlist[index]['title'])
    print(vlist[index]['cover'])
    print('https://v.huanqiu.com/article/' + str(vlist[index]['aid']))
```

把修改后的代码在colab上运行，看，不会报错了

![](https://pic.downk.cc/item/5eae94d0c2a9a83be5a057f4.png)

到这一步，恭喜你，代码调试ok，可以尝试往vid插件上移植了

### 5.完善get_huanqiu_videos(page) 函数

前言：在完善之前，先讲讲如何在kodi实时调试代码和查看kodi的log排错
以windows为例：

kodi的目录在：
 > C:\Users\你的登录名\AppData\Roaming\Kodi

![](https://pic.downk.cc/item/5eae9bcfc2a9a83be5a3e7c7.png)

你安装的所有插件在addons目录里  
我们想要调试vid插件，我们打开那个plugin.video.vid 文件夹

![](https://pic.downk.cc/item/5eae9bcfc2a9a83be5a3e7ca.png)

寻找那个 .py 后缀的文件，打开它，修改，然后在kodi运行对应插件

![](https://pic.downk.cc/item/5eae9bcfc2a9a83be5a3e7cc.png)

kodi的log在：

![](https://pic.downk.cc/item/5eae9bcfc2a9a83be5a3e7c7.png)

如果你调试中插件报错，你可以在这里找到报错的详细信息

**前言end**

--- 

首先，我们把上一步的代码往get_huanqiu_videos(page) 里复制

```python
def get_huanqiu_videos(page):
    videos = []
page = 1
page = 10*(int(page)-1)
url='https://v.huanqiu.com/api/list?node=%22/e3pmh2fmu/e3pmh2g69%22,%22/e3pmh2fmu/e3pn61vrg%22,%22/e3pmh2fmu/e3prkldqd%22,%22/e3pmh2fmu/e3prvucof%22,%22/e3pmh2fmu/e3ptgqp01%22,%22/e3pmh2fmu/e3ptgqp01/e3ptrminr%22&offset='+str(page)+'&limit=20'

r = requests.get(url,headers=headers)
j = json.loads(r.text)

vlist = j['list']
for index in range(len(vlist)-1):
    print(vlist[index]['title'])
    print(vlist[index]['cover'])
    print('https://v.huanqiu.com/article/' + str(vlist[index]['aid']))

    return videos
```
记得给所有复制来的代码打上四个空格，因为python对空格要求很严格，多一个少一个会报错
```python
def get_huanqiu_videos(page):
    videos = []
    page = 1
    page = 10*(int(page)-1)
    url='https://v.huanqiu.com/api/list?node=%22/e3pmh2fmu/e3pmh2g69%22,%22/e3pmh2fmu/e3pn61vrg%22,%22/e3pmh2fmu/e3prkldqd%22,%22/e3pmh2fmu/e3prvucof%22,%22/e3pmh2fmu/e3ptgqp01%22,%22/e3pmh2fmu/e3ptgqp01/e3ptrminr%22&offset='+str(page)+'&limit=20'

    r = requests.get(url,headers=headers)
    j = json.loads(r.text)

    vlist = j['list']
    for index in range(len(vlist)-1):
        print(vlist[index]['title'])
        print(vlist[index]['cover'])
        print('https://v.huanqiu.com/article/' + str(vlist[index]['aid']))

    return videos
```
把for循环换成这样

```python
    for index in range(len(vlist)-1):
        videoitem = {}
        videoitem['name'] =  vlist[index]['title']
        videoitem['href'] =  'https://v.huanqiu.com/article/' + str(vlist[index]['aid'])
        videoitem['thumb'] = vlist[index]['cover']
        videoitem['info'] = {}
        videos.append(videoitem)
```
值 | 说明
-- | -- 
name | kodi视频列表的标题
href | 值，就是传递给 get_huanqiu_mp4(url) 和 get_huanqiu_mp4info(url)中的url
thumb | 视频图片地址url，用于展示图片
info | kodi的setinfo,具体参考kodi的setinfo，不想设置传递一个空字典{}

保存下代码，试试运行插件看看，是不是可以正常显示视频列表了？

但是，我们还需要对代码小修改。  
把 page = 1 删掉，不然没法 下一页

(可选修改)把
```python
    r = requests.get(url,headers=headers)
    j = json.loads(r.text)
```
换成
```python
    r = get_html(url)
    j = json.loads(r)
```
get_html(url)是我写的函数，功能和requests.get(url,headers=headers)一样，不仅用法比它简单，而且，有缓存功能，短时间（两分钟内）内相同url请求直接调用缓存的数据，减少向服务器的请求次数，降低被网站方察觉的可能


给info加点东西

```
{'plot':vlist[index]['title'] + u'\n\n来自' + vlist[index]['source']['name'] + '\n' +unix_to_data(str(vlist[index]['ctime'])[:-3],'%Y-%m-%d %H:%M:%S')}
```

'\n' 是回车键的意思  

'' 前加u是让字符串变成utf-8的编码，如果你遇到ascll错误，试试在中文字符串前加u  

unix_to_data()是一个神奇的把158xxxxx的10或者13位数字转成日期时间的神奇函数，你只需要传入158xxx的数字和'%Y-%m-%d %H:%M:%S'格式即可  
想输出2018-1-11 11:12:13 格式的日期传入 ：'%Y-%m-%d %H:%M:%S'
只要2018-1-11 的传入 ：'%Y-%m-%d'

```python
def get_huanqiu_videos(page):
    videos = []
    page = 10*(int(page)-1)
    url='https://v.huanqiu.com/api/list?node=%22/e3pmh2fmu/e3pmh2g69%22,%22/e3pmh2fmu/e3pn61vrg%22,%22/e3pmh2fmu/e3prkldqd%22,%22/e3pmh2fmu/e3prvucof%22,%22/e3pmh2fmu/e3ptgqp01%22,%22/e3pmh2fmu/e3ptgqp01/e3ptrminr%22&offset='+str(page)+'&limit=20'

    r = get_html(url)
    j = json.loads(r)
    
    vlist = j['list']
    for index in range(len(vlist)-1):
        videoitem = {}
        videoitem['name'] =  vlist[index]['title']
        videoitem['href'] =  'https://v.huanqiu.com/article/' + str(vlist[index]['aid'])
        videoitem['thumb'] = vlist[index]['cover']
        videoitem['info'] = {'plot':vlist[index]['title'] + u'\n\n来自' + vlist[index]['source']['name'] + '\n' +unix_to_data(str(vlist[index]['ctime'])[:-3],'%Y-%m-%d %H:%M:%S')}
        videos.append(videoitem)

    return videos
```