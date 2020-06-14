# cine for kodi 0.2.0
## :black_nib: 简介
- cine插件是一个电影网站聚合插件，它是vid插件的改进版，为适配电影网站而生

---
## :book: 目录
 * [:beginner: 开始使用](#beginner-开始使用)
   * [下载依赖](#下载依赖)
 * [:moyai: 开发文档](#moyai-开发文档)
   * [get_categories()函数中注册](#get_categories函数中注册)
   * [创建所需函数](#创建所需函数)
   * [get_xxx_categories()函数](#get_xxx_categories函数)
   * [get_xxx_videos(url,page)函数](#get_xxx_videosurlpage-函数)
   * [get_xxx_source(url)函数](#get_xxx_sourceurl-函数)
   * [get_xxx_mp4(url)函数](#get_xxx_mp4url-函数)
 * [:rocket: 快速适配支持maccms采集的网站 `即将上线`](#rocket-快速适配支持maccms采集的网站-即将上线)
 * [:gear: 内置函数](#gear-内置函数)
   * [get_html()](#get_html)
   * [post_html()](#post_html)
   * [unix_to_data()](#unix_to_data)

---

## :beginner: 开始使用

### 下载依赖

先安装script.module.pyjsparser.zip等待安装成功

接着安装 script.module.js2py.zip，等待安装成功

最后安装script.module.cfscrape.zip，等待安装成功

下载地址：https://pan.lanzou.com/u/zheng2014

---

## :moyai: 开发文档 

本插件和bangumi插件的开发文档通用

假设你想为本插件编写一个 hellobangumi网站的番剧插件，供所有使用该插件的人可以轻松浏览，搜索该网站的番剧

你需要在👇

### get_categories()函数中“注册”

```python
def get_categories():
    return [{'id':1,'name':'哔咪哔咪(bimibimi.tv)','link':'bimibimi','author':'zhengfan2014','upload':'2020-5-6','videos':24,'search':24,'plot':'更新速度比樱花稍慢，但是总体画质比樱花高'}]
```
在最后一行加上 你的 浏览helloworld网站插件

```python
{'id':2,'name':'我的helloworld','link':'helloworld','author':'zhengfan2014','upload':'2020-5-6'}
```
必填参数：
必填参数  |	格式
:----: | :----
id |	整数(int)，值必须且为非0的正值，大小不限，甚至可以重复，第一次列表排序根据此值从小到大来排序
name |	字符串(str)，值必须但不限制，用来在首页显示你编写的网站的名字
link |	字符串(str)，值必须且唯一，不得与get_categories函数中其他link的值重复，是你网站在bangumi插件中的唯一标识符
author | 字符串(str)，插件作者
upload | 字符串(str)，y-m-d格式，用来表示插件最后更新时间

可选参数：

可选参数  |	格式
:----: | :----
videos | 整数(int)，可选参数，用来表示网页视频列表每页显示的最大视频数，插件根据这个判断是否显示下一页的按钮，如果对应的网站没有下一页（比如八重樱动漫），可不设置
search | 整数(int)，用来表示搜索的视频列表每页显示的最大视频数，插件根据这个判断是否显示下一页的按钮，如果对应的网站没有下一页（比如八重樱动漫），可不设置
plot | 字符串(str)，对插件的说明，你可以简单介绍下这个网站的优缺点，方便用户选择

### 创建所需函数

xxx 由 你注册时link的值决定

必须函数：

必须函数  |	格式
:---- | :----
get_xxx_categories() | 显示对应网站分类的函数
get_xxx_videos(url,page) | 输出视频列表的函数
get_xxx_source(url) | 输出视频多条播放线路列表和选集列表的函数
get_xxx_mp4(url) | 输出视频地址的函数

可选函数

可选函数  |	格式
:---- | :----
get_xxx_search(keyword,page) | 输出搜索视频列表的函数
get_xxx_mp4info(url) | 输出刮削的视频信息的函数

### get_xxx_categories() 函数
 > 输出一个列表套娃字典的内容。当用户选择了一个分类后，字典内的对应分类的link值将传递给下一个函数get_xxx_videos(url,page)中的 url

### get_xxx_videos(url,page) 函数
 > 输出一个列表套娃字典的内容。当用户选择了一个视频后，字典内的对应视频的href值将传递给下一个函数get_xxx_source(url)中的 url

必须参数

字典参数 |	格式
:---- | :----
name | 视频名字
thumb | 视频图片地址
href | 视频url地址，传递给下一个函数get_xxx_source(url)中的 url

可选参数
字典参数 |	格式
:---- | :----
info | 字典，比如{'plot':'123'}具体参数参见kodi 的setinfo

 输出示例：
 ```python
[{'name':'视频1','thumb':'http://123.com/1.jpg','href':'http://123.com/videos1/'},{'name':'视频2','thumb':'http://123.com/2.jpg','href':'http://123.com/videos2/'}]
 ```

  > 注意：  
 > 1.输出的内容编码建议为utf-8，使用ascll可能会出问题
---

### get_xxx_source(url) 函数
 > 输出一个列表套娃字典套娃字符串化字典的内容。当用户选择了一个视频后，字典内的对应视频的href值将传递给下一个函数get_xxx_mp4(url)中的 url

输出树：
 - [
   - {
     - name : 线路名字
     - href : 字符串化的字典,字典内容为 {'第x集':'第x集对应的url地址' }
   - }
 - ]

 > 注意：  
 > 1.href的内容必须为str处理过的字典！  
 > 2.输出的内容编码建议为utf-8，使用ascll可能会出问题

 输出示例：
 ```python
[{'name':'播放线路1','href':"{'第一集':'http://baidu.com/videos/1/1','第二集':'http://baidu.com/videos/1/2'}"},
{'name':'播放线路2','href':"{'第一集':'http://baidu.com/videos/2/1','第二集':'http://baidu.com/videos/2/2'}"}]
 ```
---
### get_xxx_mp4(url) 函数
 > 输出视频的地址

 输出示例：
```python
http://gss3.baidu.com/shaufbwdusaf.mp4
```
---
## 	:rocket: 快速适配支持maccms采集的网站 `即将上线`

### get_maccms_xxx(api,url,keyword,page,banid,debug)

> 对接支持maccms采集站的接口  
> json接口请使用get_maccms_json函数，xml接口请使用get_maccms_xml函数

#### 必须参数
参数 |	格式
:---- | :----
api | 采集站接口的地址

#### 可选参数 - url,keyword,page

get_maccms_xxx函数通过传入的可选参数类型来决定输出的内容


参数                     |	url | keyword | page
:----                    | :----: | :----: | :----:
输出get_xxx_categories()内容     | 
输出get_xxx_videos(url,page)内容 | :heavy_check_mark: | | :heavy_check_mark: 
输出get_xxx_source(url)内容      | :heavy_check_mark: | | 
输出get_xxx_search(url)内容      |  | :heavy_check_mark:| :heavy_check_mark: 

get_xxx_mp4info(url) : url,keyword,page共有2³=8的组合结果，除以上的四种组合之外，其他的四种传入类型均输出符合get_xxx_mp4info(url) 的内容

#### 可选参数 - banid

此参数用于屏蔽一些空内容或者少内容的视频分类

仅在get_maccms_xxx函数输出符合get_xxx_categories()的内容时此可选参数生效

格式：字符串，数字为视频分类id，可用chrome浏览器查看接口源代码获得，或者通过get_maccms_xxx函数的debug模式获得

示例 - 屏蔽单个分类，id为1的电影分类
```python
banid='1'
```
示例 - 屏蔽多个分类，id为1的电影，id为2的电视剧和id为3的动漫
```python
banid='1,2,3'
```
#### 可选参数 - debug

此参数用于开启get_maccms_xxx函数的debug模式

仅在get_maccms_xxx函数输出符合get_xxx_categories()的内容时此可选参数生效

格式：设置一个非'no'的值

示例
```python
debug='yes'
```
```python
debug='123'
```
```python
debug='y'
```
以上示例均能启用debug模式

debug模式功能：

 - 检测每一个分类列表，是否为空

 - 检测资源站输出视频列表的pagesize值，用于设置get_categories()函数中“注册”的video的值

 - 检测搜索不同关键词是否输出相似度极高的结果

### 快速适配采集站示例

我们以适配卧龙资源为例子

先走一套常规流程

在get_categories()函数中“注册”

```python
{'id':2,'name':'卧龙资源','link':'wolongzy','author':'zhengfan2014','upload':'2020-6-12'}
```
创建对应函数，注意，get_wolongzy的wolongzy是由上一步的link的值决定的
```python
#显示对应网站分类的函数
get_wolongzy_categories():
    return 
#输出视频列表的函数
get_wolongzy_videos(url,page):
    return 
#输出视频多条播放线路列表和选集列表的函数
get_wolongzy_source(url):
    return 
#输出视频真实播放地址函数
get_wolongzy_mp4(url):
    return 
#输出视频简介信息等函数
get_wolongzy_mp4info(url):
    return 
#输出搜索结果函数
get_wolongzy_search(url):
    return 
```
然后，你只需要拿到卧龙资源的接口地址，注意是要直接输出m3u8视频地址的接口，
```
https://cj.wlzy.tv/inc/s_api_mac_m3u8.php
```
接着，看清楚你的接口输出的是xml还是json，用chrome查看源代码判断。含有一堆<>的就是xml ，有大量的{}就是json接口

这里以xml接口举例，知道接口类型了，接下来就是调用get_maccms函数对接了

以下四个，传入什么函数，就照抄进get_maccms_xml函数里
```python
#显示对应网站分类的函数
get_wolongzy_categories():
    return get_maccms_xml('https://cj.wlzy.tv/inc/s_api_mac_m3u8.php')
#输出视频列表的函数
get_wolongzy_videos(url,page):
    return get_maccms_xml('https://cj.wlzy.tv/inc/s_api_mac_m3u8.php',url=url,page=page)
#输出视频多条播放线路列表和选集列表的函数
get_wolongzy_source(url):
    return get_maccms_xml('https://cj.wlzy.tv/inc/s_api_mac_m3u8.php',url=url)
#输出搜索结果函数
get_wolongzy_search(keyword,page):
    return get_maccms_xml('https://cj.wlzy.tv/inc/s_api_mac_m3u8.php',keyword=keyword,page=page)
```

get_xxx_mp4也是照抄，不过不用调用get_maccms_xml函数，因为get_wolongzy_source输出的就是真实视频地址了，
```python
#输出视频真实播放地址函数
get_wolongzy_mp4(url):
    return url
```
至于get_xxx_mp4info函数它比较特殊，因为单url的类型已经被get_xxx_source抢了，所以只能用那些上面没用到的类型，比如url和keyword同时传入，就是上面没有的，这时就会输出mp4info(url)的内容

 > 实际上get_maccms_xml函数输出mp4info的内容并不需要调用url参数和keyword的值，所以这两个值可以随便乱填，不影响内容生成

```python
#输出视频简介信息等函数
get_wolongzy_mp4info(url):
    return get_maccms_xml('https://cj.wlzy.tv/inc/s_api_mac_m3u8.php',url='url',keyword='123')
```
这样，一个资源站就适配好了，你可以尽情用kodi享受在线电影 电视剧 ~~无处不在的赌场广告~~ 了


---
## :gear: 内置函数

### get_html()

#### 描述：
get_html() 函数和requests.get函数相同，但是get_html() 函数返回url的网页源代码同时会缓存一份在本地，两分钟内的相同请求直接调用缓存的结果，减少向服务器请求的次数，降低被网站站长察觉的几率

#### 语法：
get_html(url)
####  参数：
参数 | 说明
---- | ----
url | 字符串(str)，必填参数，为要访问的url `cine beta 0.1.0+支持`
ua | 字符串(str)，可选参数，不填默认为pc的ua。 `cine beta 0.1.0+支持`
cf | 整数(int)，可选参数，cf=1时启用绕过cloudflare 5秒盾功能。不填默认不启用 `cine beta 0.1.0+支持`
mode | 字符串(str)，可选参数，默认为mode='html'输出网页源代码，当mode='url'时，返回的不是网页源代码而是request请求后的url。适合对付那些需要302跳转才能获取真实视频地址的 `cine beta 0.1.0+支持`
encode | 字符串(str)，可选参数，用来指定网页编码，默认为utf-8，当输出为乱码时可尝试指定encode='gbk'  `cine beta 0.2.0+支持`

ua可传入的值：

ua值 | 说明
---- | ----
pc | 电脑的ua `默认`
mobile | 安卓手机的ua
iphone | 苹果手机的ua
ipad | ipad的ua
mac | 苹果电脑的ua

mode可传入的值：

ua值 | 说明
---- | ----
html | 输出网页源代码 `默认`
url | 输出request请求后跳转到的url

encode可传入的值：

ua值 | 说明
---- | ----
utf-8 | 使用utf-8来解码html源代码 `默认`
gbk | 使用gbk来解码html源代码

#### 返回值：
函数返回url的网页源代码
#### 实例：

以下展示了使用 get_html() 方法的实例：
```python
print(get_html('http://google.cn'))
```
以上实例运行后输出结果为：
```html
<!DOCTYPE html>
<html lang="zh">
  <meta charset="utf-8">
  <title>Google</title>
  <style>
    html { background: #fff; margin: 0 1em; }
    body { font: .8125em/1.5 arial, sans-serif; text-align: center; }
    h1 { font-size: 1.5em; font-weight: normal; margin: 1em 0 0; }
    p#footer { color: #767676; font-size: .77em; }
    p#footer a { background: url(//www.google.cn/intl/zh-CN_cn/images/cn_icp.gif) top right no-repeat; padding: 5px 20px 5px 0; }
    ul { margin: 2em; padding: 0; }
    li { display: inline; padding: 0 2em; }
    div { -moz-border-radius: 20px; -webkit-border-radius: 20px; border: 1px solid #ccc; border-radius: 20px; margin: 2em auto 1em; max-width: 650px; min-width: 544px; }
    div:hover, div:hover * { cursor: pointer; }
    div:hover { border-color: #999; }
    div p { margin: .5em 0 1.5em; }
    img { border: 0; }
  </style>
  <div>
    <a href="http://www.google.com.hk/webhp?hl=zh-CN&amp;sourceid=cnhp">
      <img src="//www.google.cn/landing/cnexp/google-search.png" alt="Google" width="586" height="257">
    </a>
    <h1><a href="http://www.google.com.hk/webhp?hl=zh-CN&amp;sourceid=cnhp"><strong id="target">google.com.hk</strong></a></h1>
    <p>请收藏我们的网址
  </div>
  <ul>
    <li><a href="http://translate.google.cn/?sourceid=cnhp">翻译</a>
  </ul>
  <p id="footer">&copy;2011 - <a href="http://www.miibeian.gov.cn/">ICP证合字B2-20070004号</a>
  <script nonce="seq4yqrbKQbF7TNEBaEOtg">
    var gcn=gcn||{};gcn.IS_IMAGES=(/images\.google\.cn/.exec(window.location)||window.location.hash=='#images'||window.location.hash=='images');gcn.HOMEPAGE_DEST='http://www.google.com.hk/webhp?hl=zh-CN&sourceid=cnhp';gcn.IMAGES_DEST='http://images.google.com.hk/imghp?'+'hl=zh-CN&sourceid=cnhp';gcn.DEST_URL=gcn.IS_IMAGES?gcn.IMAGES_DEST:gcn.HOMEPAGE_DEST;gcn.READABLE_HOMEPAGE_URL='google.com.hk';gcn.READABLE_IMAGES_URL='images.google.com.hk';gcn.redirectIfLocationHasQueryParams=function(){if(window.location.search&&/google\.cn/.exec(window.location)&&!/webhp/.exec(window.location)){window.location=String(window.location).replace('google.cn','google.com.hk')}}();gcn.replaceHrefsWithImagesUrl=function(){if(gcn.IS_IMAGES){var a=document.getElementsByTagName('a');for(var i=0,len=a.length;i<len;i++){if(a[i].href==gcn.HOMEPAGE_DEST){a[i].href=gcn.IMAGES_DEST}}}}();gcn.listen=function(a,e,b){if(a.addEventListener){a.addEventListener(e,b,false)}else if(a.attachEvent){var r=a.attachEvent('on'+e,b);return r}};gcn.stopDefaultAndProp=function(e){if(e&&e.preventDefault){e.preventDefault()}else if(window.event&&window.event.returnValue){window.eventReturnValue=false;return false}if(e&&e.stopPropagation){e.stopPropagation()}else if(window.event&&window.event.cancelBubble){window.event.cancelBubble=true;return false}};gcn.resetChildElements=function(a){var b=a.childNodes;for(var i=0,len=b.length;i<len;i++){gcn.listen(b[i],'click',gcn.stopDefaultAndProp)}};gcn.redirect=function(){window.location=gcn.DEST_URL};gcn.setInnerHtmlInEl=function(a){if(gcn.IS_IMAGES){var b=document.getElementById(a);if(b){b.innerHTML=b.innerHTML.replace(gcn.READABLE_HOMEPAGE_URL,gcn.READABLE_IMAGES_URL)}}};
    gcn.listen(document, 'click', gcn.redirect);
    gcn.setInnerHtmlInEl('target');
  </script>
```
### post_html()

#### 描述：
post_html() 函数和requests.post函数相同，但是post_html() 函数返回url的网页源代码同时会缓存一份在本地，两分钟内的相同请求直接调用缓存的结果，减少向服务器请求的次数，降低被网站站长察觉的几率

#### 语法：
post_html(url,data)
####  参数：
参数 | 说明
---- | ----
url | 字符串(str)，必填参数，为要访问的url
data | 字符串化的字典(str(dict))，必填参数，为要post的值组成的字典
ua | 字符串(str)，可选参数，不填默认为pc的ua。

ua可传入的值：

ua值 | 说明
---- | ----
pc | 电脑的ua
mobile | 安卓手机的ua
iphone | 苹果手机的ua
ipad | ipad的ua
mac | 苹果电脑的ua

#### 返回值：
函数返回url的网页源代码
#### 实例：

以下展示了使用 post_html() 方法的实例：
```python
payload = str({'key1': 'value1', 'key2': 'value2'})

print(post_html('https://httpbin.org/post',payload))
```
以上实例运行后输出结果为：
```json
"form": {
    "key2": "value2",
    "key1": "value1"
  },
```

### unix_to_data()

#### 描述：
unix_to_data()返回人类能正常理解的unix时间

#### 语法：
unix_to_data(uptime,format)
####  参数：
参数 | 说明
---- | ----
uptime | 整数(int)，必填参数，为要转换的unix时间（10位或者13位）
format | 字符串(str)，可选参数，不填默认输出 2020-10-10格式的时间。

format可传入的值：

format值 | 说明
---- | ----
data | 输出 2020-10-10格式的时间
zhdata | 输出 2020年10月10日 格式的时间
datatime | 输出 2020-10-10 10:10:10 格式的时间
zhdatatime | 输出 2020年10月10日 10时10分10秒 格式的时间
time | 输出 10:10:10 格式的时间
zhtime | 输出 10时10分10秒 格式的时间

#### 返回值：
函数返回人类能正常理解的unix时间
#### 实例：

以下展示了使用 unix_to_data() 方法的实例：
```python
print(unix_to_data(1588590928))
```
以上实例运行后输出结果为：
```python 
2020-5-4
```