# zhengfan2014的kodi插件仓库
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

- 5dm（dilidili） -  www.5dm.tv
> - 显示所有栏目的视频
> - 显示弹幕

- 吐槽网（c站） - tucao.one
> - 显示所有栏目的视频
> - 显示弹幕

- 网易云音乐
> - 播放音乐
> - 播放mv
> - 显示歌词
> - 自定义导入歌单

- qq音乐
> - 播放音乐
> - 播放mv
> - 显示歌词
> - 自定义导入歌单

- 直播聚合
> - 播放全平台的直播
> - 自定义导入想看直播的列表

## 已经写出解析和取出视频mp4地址的原型python代码

- 医学微视
- 国图公开课
- 抖音
- 快手

## 成品插件
>  注：github已不再上传插件zip包，成品插件统一在爱发电发布：afdian.net/@zhengfan2014
- plugin.video.acfun        0.2.0 - 来自acfun.cn的在线视频
- plugin.video.bilibili     0.5.1 - 来自bilibili.com的在线视频
- plugin.video.changku      0.1.0 - 来自vmovier.com的在线视频
- plugin.video.huanxi       0.1.0 - 来自huanxi.com的在线视频
- plugin.video.kaiyan       0.1.0 - 来自豌豆荚旗下的开眼app的在线视频
- plugin.video.pengpai      0.1.0 - 来自paper.cn的在线视频
- plugin.video.skypixel     0.1.0 - 来自skypixel.com的在线视频
- plugin.video.taptap       0.1.0 - 来自taptap.com的在线视频
- plugin.video.weibotv      0.1.1 - 来自weibo.com/tv的在线视频
- plugin.video.xinpianchang 0.1.0 - 来自xinpianchang.com的在线视频
# 捐赠作者
如果您觉得这些小作品对您有很大帮助的话，不妨给作品点一个小小的star，请作者喝一杯咖啡，您的支持也是作者维护插件库的动力  
爱发电：https://afdian.net/@zhengfan2014  
paypal：http://paypal.me/nxsoft


