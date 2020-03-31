# bilibili for kodi 0.4.0
## 主要功能
- 按照排行榜显示全部视频栏目
- 使用官方api和第三方api解析视频
- 支持播放1080p视频
- 搜索功能
- 按bv号访问视频功能
- 缓存功能（减少向服务器请求次数）
## 更新历史
 > -[v0.4.0]----------------------
 > 新增 - b站官方解析 （感谢github bilibili down 开源项目）
 > 修复 - xbeibeix.com api （我求求你不要再改网页布局了，两天一改，这谁顶得住）
 > -[v0.3.2]----------------------
 > 修复 - xbeibeix api 变更post参数导致失败的问题
 > 新增 - 缓存功能，短时间内的重复请求直接调用本地缓存的结果，减少向服务器的请求次数
 > -[v0.3.1]----------------------
 > 修复 - b站官方av改bv导致所有非番剧无法播放的问题
 > 修复 - xbeibeix.com api 解析的显示
 > 移除 - weibomiaopai.com的api
 > -[v0.3.0]----------------------
 > 修复 - 修改版本号到0.3.0，修复因为安装xbmc中文插件库而导致自动更新成0.2.9版本的taxigps的bilibili
 > 修复 - bug（我忘了修了啥）
 > 新增 - 搜索功能
## 使用到的开源项目
- https://github.com/Henryhaohao/Bilibili_video_download
## 使用到的第三方api
- xbeibeix.com
- weibomiaopai.com (0.3.1版本已移除)