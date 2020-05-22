# zhengfan2014的kodi插件仓库
![星星数](https://img.shields.io/github/stars/zhengfan2014/xbmc-kodi-private-china-addons)
![叉子数](https://img.shields.io/github/forks/zhengfan2014/xbmc-kodi-private-china-addons)
![问题数](https://img.shields.io/github/issues/zhengfan2014/xbmc-kodi-private-china-addons?color=%232E8B57)
![kodi18测试通过](https://img.shields.io/badge/%E5%BC%80%E5%8F%91%E7%8E%AF%E5%A2%83-kodi%2018-green)
[![酷安粉丝][coolapk]](http://www.coolapk.com/u/2864549) [![b站粉丝][bilibili]](https://space.bilibili.com/25818910)
[![爱发电本月收入][mon]](https://afdian.net/@zhengfan2014)
[![爱发电发电人数][once]](https://afdian.net/@zhengfan2014)

----

 > PS : 如果你不能看见上面的小牌子或者github的图片无法正常显示，请在hosts中加入如下一行，不出意外，应该可以正常显示 
 ```
192.30.253.112 github.com
 ```
[引用自csdn评论区](https://blog.csdn.net/qq_38232598/article/details/91346392)

----

  > PS2 : 上面的小牌子你也想整一个？ 请戳这里 ☛ [用 Substats 和 Shields.io 为你的个人主页定制动态数据小牌子](https://sspai.com/post/59593) 我也是从这里学来的😂
## 介绍

> 关于[dev]:dev tag是指插件处于开发者预览版，非最终成品，有许多核心功能无法使用，仅供体验。
## 如何使用
### 安装插件
要安装插件，您需要下载对应的插件zip包。接着：  

- 启动XBMC
- 导航到系统| 设置| 附加组件
- 选择从zip文件安装
- 浏览到存储新下载的zip文件的目录。
- 选择确定

为了在xbmc上正确显示中文文本，请执行以下步骤：  

- 启动XBMC
- 导航到 system| setting| interface| skin| fonts
- 将外观字体更改为“Arial based”
- 在 system| setting| interface| regional| language 中
- 将语言更改为 Chinese （Simple）

# kodi插件开发流程

1. 用py写出爬虫代码爬出视频列表
2. 把py爬虫代码移植到kodi插件里
3. 缝合网上的视频解析接口到kodi插件，成品插件出炉

## 处于设想阶段
- 酷安视频 - coolapk.com
> - 显示酷安视频栏目的热门视频，最新视频
> - 视频下面的评论以弹幕形式展示


## 已经写出解析和取出视频mp4地址的原型python代码

- 国图公开课
- 抖音
- 快手

## 成品插件
>  注：github已不再上传插件zip包，成品插件统一在爱发电发布：afdian.net/@zhengfan2014

### 视频插件

插件目录              | 插件名 | 版本 | 最后更新 | 简介
 :------------------ | ---- | ---- | ---- | ----
 plugin.video.bilibili | bilibili | 0.5.3 | 2020-05-10 | bilibili是国内知名的视频弹幕网站，这里有最及时的动漫新番，最棒的ACG氛围，最有创意的Up主。大家可以在这里找到许多欢乐
 plugin.video.acfun | acfun | 0.2.1 | 2020-05-05 | AcFun是一家弹幕视频网站，致力于为每一个人带来欢乐
 plugin.video.changku | 场库 | 0.1.0 | 2020-03-29 | 高品质短片分享平台,汇集优秀视频短片及微电影创作人,实时不断分享全球优秀视频短片,微电影
 plugin.video.huanxi | 欢喜首映 | 0.1.0 | 2020-03-29 | 欢喜首映拥有王家卫、徐峥、陈可辛、宁浩、顾长卫、张一白、贾樟柯、张艺谋等巨匠影人为平台定制的大制作网剧、网络大电影,将视频播放与内容制作合二为一,首映厅首发好电影
 plugin.video.skypixel | 天空之城 | 0.1.0 | 2020-03-29 | 世界各地的航拍摄影师、拍手叫绝的航拍作品与独具价值的航拍攻略。全世界的探索者们互相启发,乐在其中
 plugin.video.taptap | Taptap | 0.1.0 | 2020-03-29 | TapTap是一个推荐高品质手游的手游分享社区，实时同步全球各大应用市场游戏排行榜，与全球玩家共同交流并发掘高品质手游。每一款推荐游戏，都是由专业的测评团队从全球海量的游戏中精选而出，只为你提供好玩的手机游戏。
 plugin.video.xinpianchang | 新片场 | 0.1.0 | 2020-03-29 | 新片场汇聚全球原创优质视频及创作人，提供4K、无广告、无水印视频观看，专业的视频艺术学习教程，正版视觉素材交易等，与数百万创作人一起用作品打动世界
 plugin.video.weibotv | 微博视频 | 0.1.1 | 2020-03-16 | 随时随地发现新鲜事！微博带你欣赏世界上每一个精彩瞬间，了解每一个幕后故事。
 plugin.video.kaiyan | 开眼 | 0.1.0 | 2020-03-10 | 精选视频推荐，每日大开眼界
 
 ----

### 音乐插件

插件目录              | 插件名 | 版本 | 最后更新 | 简介
 :------------------ | ---- | ---- | ---- | ---- 
 plugin.audio.jsososo | jsososo | 0.1.0 | 2020-05-15 |music.jsososo.com的音乐插件，播放你自己的网易云和QQ音乐歌单和日推

----

### 原创插件

#### 番剧聚合

插件目录              | 插件名 | 版本 | 最后更新 | 简介
 :------------------ | ---- | ---- | ---- | ---- 
 plugin.video.bangumi | bangumi | 0.1.0 | 2020-05-07 |模块化的小众番剧网站聚合插件，提供开发文档，让有python基础的用户无需学习kodi插件开发知识，为本插件快速适配番剧网站

 适配网站 | 网址
---- | ---- 
哔咪哔咪 | http://bimibimi.tv/
樱花动漫 | http://yhdm.tv/
Age动漫 | https://agefans.tw/
嘶哩嘶哩 | http://silisili.me/
八重樱动漫 | http://iafuns.com/
番組計劃 | https://anime.srsg.moe/
Qinmei | https://qinmei.video/
柠萌瞬间 | http://ningmoe.com/
吐槽弹幕网 | https://tucao.one/
clicli弹幕网 | https://clicli.me/
五弹幕 | https://5dm.tv/
clicli弹幕网 | https://clicli.co/

----

#### 电影聚合

插件目录              | 插件名 | 版本 | 最后更新 | 简介
 :------------------ | ---- | ---- | ---- | ---- 
 plugin.video.cine | cine | 0.1.0 | 2020-05-09 |模块化的小众电影/电视剧/综艺网站聚合插件，提供开发文档，让有python基础的用户无需学习kodi插件开发知识，为本插件快速适配电影网站

适配网站 | 网址
---- | ---- 
喜欢看影视 | https://138vcd.com/
片库 | https://pianku.tv/
老豆瓣 | https://laodouban.com/

----

#### 新闻/自媒体聚合

插件目录              | 插件名 | 版本 | 最后更新 | 简介
 :------------------ | ---- | ---- | ---- | ---- 
 plugin.video.vid | vid | 0.1.0 | 2020-05-03 |模块化的新闻/自媒体等单一视频网站聚合插件，提供开发文档，让有python基础的用户无需学习kodi插件开发知识，为本插件快速适配新闻/自媒体等网站

适配网站 | 网址
---- | ---- 
虎嗅视频 | https://www.huxiu.com/channel/10.html
机核视频 | https://www.gcores.com/videos
穷游视频 | https://www.qyer.com/video/
ZEALER视频 | https://www.zealer.com/video/list?id=0
澎湃视频 | https://www.thepaper.cn/channel_26916
新京报视频 | http://www.bjnews.com.cn/video/   http://www.bjnews.com.cn/wevideo/
界面视频 | https://www.jiemian.com/video/lists/index_1.html
36KR视频 | https://36kr.com/video
环球网视频频道 | https://v.huanqiu.com/

----

#### 直播聚合

插件目录              | 插件名 | 版本 | 最后更新 | 简介
 :------------------ | ---- | ---- | ---- | ---- 
 plugin.video.reallive | reallive | 0.1.0 | 2020-05-17 |模块化的直播网站聚合插件，让有python基础的用户无需学习kodi插件开发知识，为本插件快速适配各大直播网站

适配网站 | 网址
---- | ---- 
虎牙直播 | https://www.huya.com/
斗鱼直播 | https://www.douyu.com/
触手直播 | https://chushou.tv/
企鹅电竞 | https://egame.qq.com/
龙珠直播 | http://longzhu.com/
bilibili直播 | https://live.bilibili.com/
YY直播 | https://www.yy.com/
快手直播 | https://live.kuaishou.com/

# 捐赠作者
如果您觉得这些小作品对您有很大帮助的话，不妨给作品点一个小小的star，请作者喝一杯咖啡，您的支持也是作者维护插件库的动力  
爱发电：https://afdian.net/@zhengfan2014  
paypal：http://paypal.me/nxsoft


[coolapk]:https://img.shields.io/badge/dynamic/json?labelColor=11ab60&color=282c34&label=%E9%85%B7%E5%AE%89%20紫碧君&suffix=%20粉丝&query=%24.data.totalSubs&url=https%3A%2F%2Fapi.spencerwoo.com%2Fsubstats%2F%3Fsource%3Dcoolapk%26queryKey%3D2864549&logo=data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iaWNvbiIgdmlld0JveD0iMCAwIDEwMjQgMTAyNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB3aWR0aD0iNjQiIGhlaWdodD0iNjQiPjxkZWZzPjxzdHlsZS8+PC9kZWZzPjxwYXRoIGQ9Ik0xMjcuODkzIDQyNi42NjdjMjkuOTItNjYuOTg3IDk0LjUwNy0xMTYuNjk0IDE2Ni40LTEzMC4zNDcgNTUuNzg3LTkuNiAxMTIuOTYgNS4wNjcgMTYxLjkyIDMxLjk0N0M0OTcuNzYgMzQ5LjQ0IDUzNC40IDM3OC44OCA1NjcuOTQ3IDQxMS4wNGMtMTYuMTYgMTguNC0zOS4wOTQgMjguODUzLTU3LjQ5NCA0NC43NDctNDYuMTMzLTM4Ljg4LTk2LjY0LTc3LjcwNy0xNTcuOTczLTg3LjA5NC03OC45MzMtMTMuMTczLTE1OC41NiA0OS4yMjctMTcwLjUwNyAxMjcuMTQ3LTguNjkzIDQ1LjkyIDEwLjEzNCA5NC42NjcgNDUuMTc0IDEyNC45MDcgMzkuNjggMzQuOTg2IDk3LjIyNiA0NC41ODYgMTQ3LjYyNiAzMS4yNTMgNTcuNi0xMy45MiAxMDEuOTc0LTU3LjA2NyAxMzYuODU0LTEwMi43NzMgNTQuMDgtNzIuMTA3IDk5LjItMTUwLjQgMTQ3Ljg0LTIyNi4xMzQgMTMuOTItMTkuMTQ2IDQ3LjQxMy0xNy4yMjYgNTguNzIgMy44NCA2My42MjYgMTA5LjAxNCAxMjYuMDggMjE4LjcyIDE4OS42IDMyNy43ODcgNy41NzMgMTUuMDkzIDQuNDI2IDM1Ljc4Ny05LjYgNDYuMTMzLTEzLjA2NyAxMC42MTQtMzMuMzM0IDEwLjI0LTQ2LjEzNC0uNjkzYTk3MDY2LjU1OCA5NzA2Ni41NTggMCAwMS0yMjYuMTg2LTE2Mi43MmMxOC44OC0xNS4wNCAzOC40LTI5LjMzMyA1Ny45NzMtNDMuNDY3IDIzLjczMyAxMi45MDcgNDMuNzg3IDMzLjE3NCA2OS42IDQxLjY1NC0yMC4zNzMtMzkuNTc0LTQzLjYyNy03Ny43MDctNjYuMzQ3LTExNS45NDctNDIuNjY2IDU5LjE0Ny03Ny4wNjYgMTI0LjIxMy0xMjMuMTQ2IDE4MS4wNjdDNTE2IDY2My40NjcgNDQ4LjggNzE2Ljk2IDM2OC42NCA3MjguNDhjLTM4Ljg4IDMuNDEzLTc5LjMwNyA0LjIxMy0xMTYuMzczLTkuOTczLTUzLjQ5NC0xOS4xNDctMTAwLjMyLTU4LjcyLTEyNC41ODctMTEwLjU2LTI4LjIxMy01Ni4xMDctMjYuNzczLTEyNS4wMTQuMjEzLTE4MS4yOHoiIGZpbGw9IiNmZmYiLz48L3N2Zz4=&longCache=true

[bilibili]:https://img.shields.io/badge/dynamic/json?labelColor=FE7398&label=bilibili%20紫碧君&suffix=%20粉丝&query=%24.data.totalSubs&url=https%3A%2F%2Fapi.spencerwoo.com%2Fsubstats%2F%3Fsource%3Dbilibili%26queryKey%3D25818910&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGAAAABgCAYAAADimHc4AAAD7ElEQVR4nO2dW9WrMBCFK6ESkFAJSKiESqgEHCABCZWAhEpAAhL2ecik5dDc/pXLBDLfWnlqy0xmJ5BMQnq5CIIgCIIgCIIgCIIgCEIBAHQAemYfrgCunD6wAKAHsEKxALgx+bCQD8/S9tmgVqeDr1lLigDgZvDhXso+K9TyTBQRwRJ8AHjntl0Flh5QRAQK/mKxPeayWx2OXpBNBKiHvi34b7T2MC4pAvW6twR/RwkRKPizBN8CgEcuESj4Lwm+BwBjahEk+H8EwJRKhOaCDzW8e1JLfkUUH1NgmR3XmHffHR1l+72BSs8d7w8U+JDAnZERQMcV+CtUi7dNqFqibB4J7vtrq7xKCuAasbTMXCL4T+5aVk6+2xHUrWdhruAR6HIJcOeu2UHI8zyAe2ytWfEdWz9PVvQ8YAmIQ5dDAB9LFsMVAv8oMO2zAGrC5WNIarRiAuKR9jYEd9pY08aa6uUzIHGRdkgKd8pY0yc1WjEBAqypDYoAG0QAZkQAZkQAZkQAZk4vANQenjsSzS3I/wcSbXU5jQBUkRtdf4Rar90v8kSv3+I3ffCCSpk8I/w+lgDkdI/v2rEp2CaiWm1AsDQLlDAD+dlFXLMeAaCSeLZdaSFE5VUQNot38cKuEeBgAsSuG0flVZBmEanbXfNQAsS0fgBYIn2fIu3/BBMHEyBmDXlFfA8IzeHb+Ems4WAChKykrVA9ZfsQTL57jXzRg4A5wC/A8N4ADiZAZwm2XjW75Qh2KOTfA0p4kygPw28OJcCVgn3nDnYo2EwEYRgGH0qAMyICMCMCMCMCMCMCMCMCMCMCfP3qwHDOQ4AAUekTk8FaBRihJnZdYbvtCGC7LvmkM63GjVDINPFrQgCq5ETXfmMzI90FXzPvfqt7x4rEu/ZaEcCUxFvgz2zO+BUn6UkoaEEAsptiMSX5e8FoRYCN7cVgb4Vq7U/H50Pq4JNP7Qiw8UFnJwcK+tXy+Wj6PLEvPgHSHv5UgwA1IQIwwyFAyLJin9RoxYgAzAQIkPwNmf26busC+OIx5TDqo5nDT+F/SS/9CYzwb+No49zNy2evkYv0LywGGAXUvp6eSneycqOic0w20k7CNgKE7jJunSGLACTCxF27ylmQc98T5MQUH49swd+I0HPXslLKnT0N+wnkrTKi9JZL/L9i1SorMmdeQ4TQQ7OFMxIMzGD45w8nUL1im7efENZLJpgPSw0pfz0cdt4U3230Td/Tvx2R6d2FrHhEWLkq5PELOMsRPHCPnAZGv1xJteL7jbJiaW3sB2nDvPC/osSYvjRQz4cJ6n7KO3rYQL7M+L6nVtfDVRAEQRAEQRAEQRAEIZ5/SAXmdfXaoQsAAAAASUVORK5CYII=&color=282c34&longCache=true

[mon]:https://img.shields.io/badge/dynamic/json?label=本月收入&query=%24.data.totalSubs&url=https%3A%2F%2Fapi.spencerwoo.com%2Fsubstats%2F%3Fsource%3DafdianIncome%26queryKey%3Dzhengfan2014&prefix=%EF%BF%A5%20&suffix=%20%E6%AF%8F%E6%9C%88&labelColor=946ce6&color=282c34&longCache=true

[once]:https://img.shields.io/badge/dynamic/json?label=%E7%88%B1%E5%8F%91%E7%94%B5&query=%24.data.totalSubs&url=https%3A%2F%2Fapi.spencerwoo.com%2Fsubstats%2F%3Fsource%3DafdianFans%26queryKey%3Dzhengfan2014&suffix=%20%E5%8F%91%E7%94%B5%E4%BA%BA%E6%AC%A1%20%2F%20%E6%9C%88&labelColor=946ce6&color=282c34&longCache=true