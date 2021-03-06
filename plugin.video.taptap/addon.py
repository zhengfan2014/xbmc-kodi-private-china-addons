#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from xbmcswift2 import Plugin
import requests
from bs4 import BeautifulSoup
import xbmcgui
import base64
import json
import urllib2
import sys
import HTMLParser
import re
import time

from requests.adapters import HTTPAdapter

def get_real_url(url):
    rs = requests.get(url,headers=headers,timeout=2)
    return rs.url

def unescape(string):
    string = urllib2.unquote(string).decode('utf8')
    quoted = HTMLParser.HTMLParser().unescape(string).encode('utf-8')
    #转成中文
    return re.sub(r'%u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})', lambda m: unichr(int(m.group(1), 16)), quoted)


plugin = Plugin()

#taptap
tail = '&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC'
##############################################################################################################
macheaders = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4 Supplemental Update) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15'}
ipadheaders = {'user-agent': 'Mozilla/5.0 (iPad; CPU OS 10_15_4 Supplemental Update like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Mobile/15E148 Safari/605.1.15'}
iphoneheaders = {'user-agent': 'Mozilla/5.0 (iPhone; CPU OS 10_15_4 Supplemental Update like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Mobile/14E304 Safari/605.1.15'}
mheaders = {'user-agent':'Mozilla/5.0 (Linux; Android 10; Z832 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Mobile Safari/537.36'}
headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
@plugin.cached(TTL=30)
def get_html_longtimecache(url,ua='pc',cookie='',mode='html',encode='utf-8'):
    output = get_html(url,ua,cookie,mode,encode)
    return output

@plugin.cached(TTL=2)
def get_html(url,ua='pc',cookie='',mode='html',encode='utf-8'):
    if cookie != '':
        cookie = eval(cookie)
    else:
        cookie = {}
    #UA相关
    if ua == 'pc':
        head = headers
    if ua == 'mobile':
        head = mheaders
    if ua == 'iphone':
        head = iphoneheaders
    if ua == 'ipad':
        head = ipadheaders
    if ua == 'mac':
        head = macheaders

    
    
    #超时重试3次
    # s0 = requests.Session()
    with requests.Session() as s0:
        s0.mount('http://', HTTPAdapter(max_retries=3))
        s0.mount('https://', HTTPAdapter(max_retries=3))

        #获取网页源代码
        if mode == 'html':
            r = s0.get(url,headers=head,cookies=cookie)
            
            #编码相关
            if encode == 'utf-8':
                r.encoding = 'utf-8'
            if encode == 'gbk':
                r.encoding = 'gbk'
            html = r.text
    
        #用于获取302跳转网页的真实url
        if mode == 'url':
            head['Connection'] = 'close'
            r = s0.get(url,headers=head,timeout=5,stream=True,cookies=cookie)
            html = r.url
    
        return html

@plugin.cached(TTL=2)
def post_html(url,data='',ua='pc',cookie='',mode='html',encode='utf-8',jsons=''):
    if data != '':
        data =eval(data)
    if jsons != '':
        jsons =eval(jsons)

    #UA相关
    if ua == 'pc':
        head = headers
    if ua == 'mobile':
        head = mheaders
    if ua == 'iphone':
        head = iphoneheaders
    if ua == 'ipad':
        head = ipadheaders
    if ua == 'mac':
        head = macheaders

    #超时重试3次
    with requests.Session() as s0:
        s0.mount('http://', HTTPAdapter(max_retries=3))
        s0.mount('https://', HTTPAdapter(max_retries=3))

    
        if data != '' or jsons != '':
            #获取网页源代码
            if mode == 'html':
                if data != '':
                    r = s0.post(url,headers=head,data=data)
                if jsons != '':
                    r = s0.post(url,headers=head,json=jsons)
                
                if encode == 'utf-8':
                    r.encoding = 'utf-8'
                if encode == 'gbk':
                    r.encoding = 'gbk'
                html = r.text

        
            if mode == 'url' or mode == 'cookie':
                head['Connection'] = 'close'
                if data != '':
                    r = s0.post(url,headers=head,data=data,timeout=5,stream=True)
                if jsons != '':
                    r = s0.post(url,headers=head,json=jsons,timeout=5,stream=True)
                
            
                #用于获取302跳转网页的真实url
                if mode == 'url':
                    html = r.url
                #用于获取cookie
                if mode == 'cookie':
                    cookiedict = {}
                    for k,y in r.cookies.items():
                        cookiedict[k] = y
                    html = cookiedict
        
        
            return html

def unix_to_data(uptime,format='data'):
    if len(str(uptime)) > 10:
        uptime = str(uptime)[:-(len(str(uptime))-10)]
    uptime = float(uptime)
    time_local = time.localtime(uptime)
    if format == 'data' or format == 'zhdata' or format == 'datatime' or format == 'zhdatatime' or format == 'time' or format == 'zhtime' or format == 'ymdh':
        if format == 'data':
            uptime = time.strftime('%Y-%m-%d',time_local)
        if format == 'zhdata':
            uptime = time.strftime('%Y年%m月%d日',time_local)
        if format == 'datatime':
            uptime = time.strftime('%Y-%m-%d %H:%M:%S',time_local)
        if format == 'zhdatatime':
            uptime = time.strftime('%Y年%m月%d日 %H时%M分%S秒',time_local)
        if format == 'time':
            uptime = time.strftime('%H:%M:%S',time_local)
        if format == 'zhtime':
            uptime = time.strftime('%H时%M分%S秒',time_local)
        if format == 'ymdh':
            time_now = int(time.time())
            chazhi = int(int(time.time()) - int(uptime))
            if chazhi < 60:
                uptime = str(int(chazhi)) + '秒前'
            if chazhi >= 60 and chazhi < 3600:
                uptime = str(int(chazhi/60)) + '分钟前'
            if chazhi >= 3600 and chazhi < 86400:
                uptime = str(int(chazhi/3600)) + '小时前'
            if chazhi >= 86400 and chazhi < 2592000:
                uptime = str(int(chazhi/86400)) + '天前'
            if chazhi >= 2592000 and chazhi < 31104000:
                uptime = str(int(chazhi/2592000)) + '月前'
            if chazhi >= 31104000:
                uptime = str(int(chazhi/31104000)) + '年前'
    else:
        uptime = time.strftime(format,time_local)
    return uptime

def data_to_unix(dt,format='datatime'):
    if format == 'data' or format == 'zhdata' or format == 'datatime' or format == 'zhdatatime' or format == 'time' or format == 'zhtime' or format == 'ymdh':
        if format == 'data':
            timeArray = time.strptime(dt,'%Y-%m-%d')
        if format == 'zhdata':
            timeArray = time.strptime(dt,'%Y年%m月%d日')
        if format == 'datatime':
            timeArray = time.strptime(dt,'%Y-%m-%d %H:%M:%S')
        if format == 'zhdatatime':
            timeArray = time.strptime(dt,'%Y年%m月%d日 %H时%M分%S秒')
        if format == 'time':
            timeArray = time.strptime(dt,'%H:%M:%S')
        if format == 'zhtime':
            timeArray = time.strptime(dt,'%H时%M分%S秒')
    else:
        timeArray = time.strptime(dt,format)
    #转换成时间戳
    timestamp = time.mktime(timeArray)
    return timestamp

#超过10000换算
def zh(num):
    if num != '':
        if int(num) >= 100000000:
            p = round(float(num)/float(100000000), 1)
            p = str(p) + '亿'
        else:
            if int(num) >= 10000:
                p = round(float(num)/float(10000), 1)
                p = str(p) + '万'
            else:
                p = str(num)
    else:
        p = '0'
    return p

def get_categories():
    return [{'name':'编辑推荐','link':'bianji'},
            {'name':'为你推荐','link':'foryou'},
            {'name':'热门榜','link':'https://www.taptap.com/top/download'},
            {'name':'新品榜','link':'https://www.taptap.com/top/new'},
            {'name':'预约榜','link':'https://www.taptap.com/top/reserve'},
            {'name':'热卖榜','link':'https://www.taptap.com/top/sell'},
            {'name':'热玩榜','link':'https://www.taptap.com/top/played'},
            {'name':'往期推荐','link':'https://www.taptap.com/category/recommend'},
            {'name':'TapTap独家','link':'https://www.taptap.com/tag/TapTap%E7%8B%AC%E5%AE%B6'},
            {'name':'单机','link':'https://www.taptap.com/tag/%E5%8D%95%E6%9C%BA'},
            {'name':'角色扮演','link':'https://www.taptap.com/tag/%E8%A7%92%E8%89%B2%E6%89%AE%E6%BC%94'},
            {'name':'动作','link':'https://www.taptap.com/tag/%E5%8A%A8%E4%BD%9C'},
            {'name':'MOBA','link':'https://www.taptap.com/tag/moba'},
            {'name':'策略','link':'https://www.taptap.com/tag/%E7%AD%96%E7%95%A5'},
            {'name':'卡牌','link':'https://www.taptap.com/tag/%E5%8D%A1%E7%89%8C'},
            {'name':'生存','link':'https://www.taptap.com/tag/%E7%94%9F%E5%AD%98'},
            {'name':'模拟','link':'https://www.taptap.com/tag/%E6%A8%A1%E6%8B%9F'},
            {'name':'竞速','link':'https://www.taptap.com/tag/%E7%AB%9E%E9%80%9F'},
            {'name':'益智','link':'https://www.taptap.com/tag/%E7%9B%8A%E6%99%BA'},
            {'name':'二次元','link':'https://www.taptap.com/tag/%E4%BA%8C%E6%AC%A1%E5%85%83'},
            {'name':'游戏合辑','link':'https://www.taptap.com/simple-events/android'}]

def get_videos(url,page):
    videos = []
    if url == 'bianji':
        #编辑推荐
        url = 'https://www.taptap.com/webapiv2/video/v1/refresh?type=editors_choice&from=1&limit=10' + tail
        r = get_html(url)
        j = json.loads(r)
        for index in range(len(j['data']['list'])):
            imgurl = j['data']['list'][index]['image']['url']
            id = j['data']['list'][index]['id']
            videoitem = {}
            videoitem['name'] = j['data']['list'][index]['title']
            videoitem['href'] = 'https://taptap.com/video/' + str(id)
            videoitem['thumb'] = 'http' + imgurl[5:]
            videoitem['info'] = {'plot':''}
            videoitem['info']['plot'] += zh(j['data']['list'][index]['stat']['play_total']) + ' 播放 · ' + str(unix_to_data(j['data']['list'][index]['created_time'],format='ymdh')) + '\n'
            videoitem['info']['plot'] += zh(j['data']['list'][index]['ups']) + ' 赞 · ' + zh(j['data']['list'][index]['comments']) + ' 回复' + '\n\n'
            if 'app' in j['data']['list'][index]:
                videoitem['info']['plot'] += '[COLOR blue]关联游戏：[/COLOR]' + '\n' + j['data']['list'][index]['app']['title'].encode('utf-8') + '\n'
                videoitem['info']['plot'] += j['data']['list'][index]['app']['category'].encode('utf-8') + ' - [COLOR yellow]' + j['data']['list'][index]['app']['stat']['rating']['score'].encode('utf-8') + '[/COLOR]分'
            videos.append(videoitem)  
        return videos
    elif url == 'foryou':
        #为你推荐
        url = 'https://www.taptap.com/webapiv2/video/v1/refresh?type=recommend&from=0&limit=30' + tail
        r = get_html(url)
        j = json.loads(r)
        for index in range(len(j['data']['list'])):
            imgurl = j['data']['list'][index]['data']['image']['url']
            id = j['data']['list'][index]['data']['id']
            videoitem = {}
            videoitem['name'] = j['data']['list'][index]['data']['title']
            videoitem['href'] = 'https://taptap.com/video/' + str(id)
            videoitem['thumb'] = 'http' + imgurl[5:]
            videoitem['info'] = {'plot':''}
            videoitem['info']['plot'] += 'UP主：' + j['data']['list'][index]['data']['author']['name'].encode('utf-8') + '\n'
            videoitem['info']['plot'] += zh(j['data']['list'][index]['data']['stat']['play_total']) + ' 播放 · ' + zh(j['data']['list'][index]['data']['ups']) + ' 赞 · ' + zh(j['data']['list'][index]['data']['comments']) + ' 评论'
            videos.append(videoitem)  
        return videos
    elif re.search('taptap.com/top/',url):
        if int(page) == 1:
            r = get_html(url)
        else:
            #https://www.taptap.com/top/download
            #https://www.taptap.com/ajax/top/download?page=2&total=30
            key = re.search('(?<=top/)[a-z]+',url).group()
            apiurl = 'https://www.taptap.com/ajax/top/' + key + '?page=' + str(int(page)) + '&total=' + str((int(page)-1)*30)
            r = json.loads(get_html(apiurl))['data']['html']
            # dialog = xbmcgui.Dialog()
            # dialog.textviewer('guanfan',apiurl)
        soup = BeautifulSoup(r, 'html.parser')
        rankitem = soup.find_all('div',class_='taptap-top-card')
        for index in range(len(rankitem)):
            data = rankitem[index].find('a',class_='card-left-image')
            img = data.find('img')

            #游戏名
            gamename = ''
            if int(page) == 1:
                if index < 3:
                    gamename += '[COLOR yellow]' +  str(index+1) + '[/COLOR]'
                else:
                    gamename += '[COLOR blue]' +  str(index+1) + '[/COLOR]'
            else:
                gamename += '[COLOR blue]' +  str((int(page)-1)*30+index+1) + '[/COLOR]'
            gamename += ' - ' + img['alt']

            author = rankitem[index].find('p',class_='card-middle-author')
            star = rankitem[index].find('div',class_='card-middle-score')
            star1 = rankitem[index].find('div',class_='middle-footer-rating')
            desc = rankitem[index].find('p',class_='card-middle-description')
            videoitem = {}
            videoitem['name'] = gamename
            videoitem['href'] = data['href']
            videoitem['thumb'] = 'http'+img['src'][5:]
            videoitem['info'] = {'plot':author.text + ''}
            try:
                videoitem['info']['plot'] += u'评分:[COLOR blue]' + star.p.span.text + '[/COLOR]'
                stars = float(star.p.span.text)
            except AttributeError:
                if star1:
                    videoitem['info']['plot'] += u'评分:[COLOR blue]' + star1.text + '[/COLOR]'
                    stars = float(star1.text)
                else:
                    videoitem['info']['plot'] += u'评分过少'
            videoitem['info']['plot'] += '\n' + desc.text.strip()

            tag = rankitem[index].find('div',class_='card-tags')
            tags = tag.find_all('a')
            genre = []
            for i in range(len(tags)):
                genre.append(tags[i].text)
                
            videoitem['info']['title'] = img['alt']
            videoitem['info']['genre'] = genre
            videoitem['info']['castandrole'] = [(author.text.split(u':')[1],u'厂商')]
            if stars:
                videoitem['info']['rating'] = stars
            videos.append(videoitem)  
        return videos
    elif re.search('taptap.com/app/',url):
        #app抓视频列表
        videos = []
        if int(page) == 1:
            r = get_html(url)
        elif re.search('topic\?type\=official',url):
            #官方
            apiurl = url + '&sort=created&page=' + str(page)
            r = get_html(apiurl)
        elif re.search('topic\?type\=video',url):
            #video
            apiurl = url + '&sort=default&page=' + str(page)
            r = get_html(apiurl)
                    
        soup = BeautifulSoup(r, 'html.parser')
        if re.search('topic\?type\=official',url):
            #官方
            videos = []
            videoitem = soup.find_all('div',class_='common-v2-list')
            # dialog = xbmcgui.Dialog()
            # dialog.textviewer('guanfan',str(len(videoitem)))
            for index in range(len(videoitem)):
                videoitems = {}
                vide = videoitem[index].find('div',class_='video-content')
                dynamic = videoitem[index].find('div',class_='item-content')
                if vide:
                    videoitems['name'] = u'[视频]'
                    if dynamic.find('div',class_='content-text'):
                        #显示标题
                        videoitems['name'] += dynamic.find('div',class_='content-text').text.strip()
                    elif dynamic.find('p',class_='content-text'):
                        #没有标题，显示文字内容前30
                        videoitems['name'] += dynamic.find('p',class_='content-text').text[:30].strip()
                    # try:
                    #     videoitems['name'] = u'[视频]' + videoitem[index].find('div',class_='content-text').text.strip()
                    # except AttributeError:
                    #     videoitems['name'] = u'[视频]' + videoitem[index].find('div',class_='item-content').text.strip()
                    videoitems['href'] = 'https://www.taptap.com/video/' + vide.div.video['data-video-id']
                    videoitems['thumb'] = vide.div.video['poster'].split('?')[0]

                    onekeythree = videoitem[index].find('ul',class_='item-text-footer')
                    onekeythrees = onekeythree.find_all('li')

                    videoitems['info'] = {'plot':''}
                    videoitems['info']['plot'] += unix_to_data(data_to_unix(videoitem[index].find('span',class_='item-publish-time').text),format='ymdh').decode('utf-8')
                    videoitems['info']['plot'] += u' · ' + onekeythrees[1].a.span.text.strip() + u' 评论 · ' + onekeythrees[2].button.span.text.strip() + u' 赞'
                    if dynamic.find('p',class_='content-text'):
                        videoitems['info']['plot'] += '\n\n' + dynamic.find('p',class_='content-text').text.replace('\n','').replace('              ','')
                    
                    # try:
                    #     videoitems['info'] = {'plot':videoitem[index].find('p',class_='content-text').text}
                    # except AttributeError:
                    #     videoitems['info'] = {'plot':'123'}
                    # videoitems['info']['plot'] += 'https://www.taptap.com/video/' + vide.div.video['data-video-id']
                else:
                    videoitems['name'] = u'[动态]'
                    if dynamic.find('div',class_='content-text'):
                        #显示标题
                        videoitems['name'] += dynamic.find('div',class_='content-text').text.strip()
                    elif dynamic.find('p',class_='content-text'):
                        #没有标题，显示文字内容前30
                        videoitems['name'] += dynamic.find('p',class_='content-text').text[:30].strip()
                            
                    videoitems['href'] = videoitem[index]['href']
                    if dynamic.find('div',class_='moment-img-list__wrap-1'):
                        videoitems['thumb'] = dynamic.find('div',class_='moment-img-list__wrap-1').a['href']
                    else:
                        videoitems['thumb'] = ''
                    onekeythree = videoitem[index].find('ul',class_='item-text-footer')
                    onekeythrees = onekeythree.find_all('li')

                    videoitems['info'] = {'plot':''}
                    videoitems['info']['plot'] += unix_to_data(data_to_unix(videoitem[index].find('span',class_='item-publish-time').text),format='ymdh').decode('utf-8')
                    videoitems['info']['plot'] += u' · ' + onekeythrees[1].a.span.text.strip() + u' 评论 · ' + onekeythrees[2].button.span.text.strip() + u' 赞'
                    if dynamic.find('p',class_='content-text'):
                        videoitems['info']['plot'] += '\n\n' + dynamic.find('p',class_='content-text').text.replace('\n','').replace('              ','')
                        
                videos.append(videoitems)
            return videos
                
        if re.search('topic\?type\=video',url):
            #视频列表
            videoitem = soup.find_all('div',class_='common-v2-list')
            for index in range(len(videoitem)):
                videoitems = {}
                vide = videoitem[index].find('div',class_='video-content')
                dynamic = videoitem[index].find('div',class_='item-content')
                author = videoitem[index].find('div',class_='author-wrap')

                videoitems['name'] = u'[视频]'
                if dynamic.find('div',class_='item-title'):
                    #显示标题
                    videoitems['name'] += dynamic.find('div',class_='item-title').a.text.strip()
                else:
                    videoitems['name'] += u'无 标 题'   
                videoitems['href'] = 'https://www.taptap.com/video/' + vide.div.video['data-video-id']
                videoitems['thumb'] = vide.div.video['poster'].split('?')[0]

                onekeythree = videoitem[index].find('ul',class_='item-text-footer')
                onekeythrees = onekeythree.find_all('li')

                videoitems['info'] = {'plot':''}
                        
                videoitems['info']['plot'] += unix_to_data(data_to_unix(videoitem[index].find('span',class_='item-publish-time').text),format='ymdh').decode('utf-8')
                videoitems['info']['plot'] += u' · ' + zh(onekeythrees[1].a.span.text.strip()) + u' 评论 · ' + zh(onekeythrees[2].button.span.text.strip()) + u' 赞'

                videos.append(videoitems)
            return videos
    elif re.search('taptap.com/tag/',url):
        #tag页
        #dialog = xbmcgui.Dialog()
        #ok = dialog.ok('类',url)
        if int(page) == 1:
            r = get_html(url)
            
        else:
            keyword = re.search('(?<=tag/).*',url).group()
            r = get_html('https://www.taptap.com/ajax/search/tags?&kw=' + keyword + '&sort=hits&page=' + str(page))
            j = json.loads(r)
            r = j['data']['html']

        soup = BeautifulSoup(r, 'html.parser')
        appitem = soup.find_all('div',class_='taptap-app-card')
        for index in range(len(appitem)):
            data = appitem[index].find('div',class_='app-card-right app-tag-right')
            ahref = appitem[index].find('a',class_='app-card-left')
            img = ahref.find('img')

            videoitems = {}
            name = data.find('a').h4.contents
            videoitems['name'] = name[0]
            if len(name) == 2:
                videoitems['name'] += u' [COLOR blue][' + name[1].contents[0] + '][/COLOR] '
            
            videoitems['thumb'] ='http'+img['src'][5:]
            videoitems['href'] = ahref['href']
            videoitems['info'] = {'plot':''}
            videoitems['info']['plot'] += u'厂商：' + data.find('p',class_='card-right-author').a.text.strip() + u'\n'
            videoitems['info']['plot'] += u'评分：[COLOR blue]' + data.find('div',class_='card-right-rating').span.text.strip() + '[/COLOR] ' + u'\n'
            #installnum = re.search('\d+',data.find('span',class_='card-right-times').text).group()
            
            #videoitems['info']['plot'] += zh(installnum).decode('utf-8') + u' 人安装'
            etag = data.find('p',class_='card-tags').find_all('a')
            etags = []
            # dialog = xbmcgui.Dialog()
            # ok = dialog.ok('类',str(len(etag)))
            for i in range(len(etag)):
                etags.append(etag[i].text)
            videoitems['info']['genre'] = etags
            videos.append(videoitems)  
        return videos
    elif re.search('taptap.com/category/',url):
        #分类
        # dialog = xbmcgui.Dialog()
        # ok = dialog.ok('分类',url)
        if int(page) == 1:
            r = get_html(url)
        else:
            apiurl = url + '?page=' + str(page)
            r = get_html(apiurl)
        soup = BeautifulSoup(r, 'html.parser')
        appitem = soup.find_all('div',class_='taptap-app-item swiper-slide')
        for index in range(len(appitem)):
            data = appitem[index].find('div',class_='app-item-caption')
            img = appitem[index].find('img')
            videoitems = {}
            videoitems['name'] = data.a.h4.text
            if data.find('small',class_='taptap-app-area'):
                videoitems['name'] += u' [COLOR blue][' + data.find('small',class_='taptap-app-area').text + u'][/COLOR] '
            videoitems['thumb'] ='http'+img['data-src'][5:]
            videoitems['href'] = data.a['href']
            pspan = data.find('span','item-caption-label')
            videoitems['info'] = {'plot':u'评分：[COLOR blue]'  + pspan.span.text.strip()+ '[/COLOR]'}
            videoitems['info']['genre'] = [pspan.a.text.strip()]
                        
            videos.append(videoitems) 
        return videos 
    elif re.search('taptap.com/simple-events/android',url):
        #游戏合集页面
        if int(page) == 1:
            r = get_html(url)
        else:
            apiurl = url + '?page=' + str(page)
            r = get_html(apiurl)
        #print(rec.text)
        soup = BeautifulSoup(r, 'html.parser')
        section = soup.find('section',class_='event-simple-list')
        hlist = section.find('ul',class_='list-unstyled').find_all('li')
        for index in range(len(hlist)):
            videoitems = {}
            videoitems['name'] = hlist[index].button.text.strip()
            videoitems['thumb'] = ''
            videoitems['href'] = hlist[index].a['href']
            videos.append(videoitems) 
        return videos

    
 
    



@plugin.route('/play/<name>/<url>/')
def play(name,url):

    if re.search('taptap.com/video/',url):
        #视频url解析
        #url = 'https://www.taptap.com/video/1319335'
        if re.search('(?<=video/)[0-9]+',url):
            vid = re.search('(?<=video/)[0-9]+',url).group()
            api = 'https://www.taptap.com/webapiv2/video/v2/detail?id=' + str(vid)
            api += tail
            #api += '&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D2%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26UID%3D5aef8bdb-c213-4803-8a5e-33b333de04bb'
            r = get_html(api)
            j = json.loads(r)
            items = []

            #再解析一次url，缓存安排上
            r = get_html_longtimecache(j['data']['video']['url'])
            prule = re.compile(r'(?<=NAME=")\d+[p|k]\d?\d?') 
            pname = prule.findall(r)
            #print(pname)
            urlrule = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')   # 查找数字
            m3u8url = urlrule.findall(r)
            # dialog = xbmcgui.Dialog()
            # ok = dialog.ok('错误',str(pname))
            for index in range(len(pname)):
                item = {'is_playable': True}
                #item['label'] = j['data']['video']['video_resource']['info']['best_format_name']  + ' - '
                item['label'] = pname[index]  + ' - '
                item['label'] += j['data']['video']['title']
                item['path'] = m3u8url[index]
                item['thumbnail'] = j['data']['video']['image']['medium_url'].split('?')[0]
                item['icon'] = j['data']['video']['image']['medium_url'].split('?')[0]
                item['info'] = {}
                item['info']['plot'] = zh(j['data']['video']['stat']['play_total']) + ' 播放 · ' + unix_to_data(int(j['data']['video']['created_time']),'ymdh') + ' · '
                item['info']['plot'] += zh(j['data']['video']['ups']) + ' 赞 · ' + zh(j['data']['video']['comments']) + ' 回复'
                if 'intro' in j['data']['video']:
                    item['info']['plot'] += '\n\n' + re.sub('<.*?>','',j['data']['video']['intro']['text'].encode('utf-8'))
                items.append(item)
        else:
            dialog = xbmcgui.Dialog()
            ok = dialog.ok('错误','url格式错误')
        return items
    elif re.search('(?<=topic/)[0-9]+',url):
        #动态url解析
        if re.search('\?textviewer',url):
            url = url.replace('?textviewer','')
            r = get_html(url)
            soup = BeautifulSoup(r, 'html.parser')
            text = soup.find('div',class_='js-translate-content')
            dialog = xbmcgui.Dialog()
            dialog.textviewer('动态详情',text.text)
        else:
            #显示图片和文字
            items = []
            item = {'label': '动态详情','path':plugin.url_for('play', name='123',url=url+'?textviewer')}
            items.append(item)
            r = get_html(url)
            soup = BeautifulSoup(r, 'html.parser')
            text = soup.find('div',class_='js-translate-content')
            imgs = text.find_all('img',class_='bbcode-img')
            for i in range(len(imgs)):
                item = {'is_playable': True}
                item['label'] = '动态图片' + str(i+1)
                item['path'] = imgs[i]['src'].split('?')[0]
                item['thumbnail'] = imgs[i]['src'].split('?')[0]
                item['icon'] = imgs[i]['src'].split('?')[0]
                items.append(item)
            return items
            
    elif re.search('(?<=app/)[0-9]+',url):
        items = []
        #item = {'label': '官方视频','path':plugin.url_for('category', url=url+'/video?type=official')}
        item = {'label': '官方动态','path':plugin.url_for('category', url=url+'/topic?type=official',page=1)}
        
        items.append(item)
        #item = {'label': '玩家视频','path':plugin.url_for('category', url=url+'/video?type=not_official')}
        item = {'label': '视频专区','path':plugin.url_for('category', url=url+'/topic?type=video',page=1)}
        items.append(item)
        return items
    elif re.search('(?<=category/)[0-9a-zA-Z]+',url):
        items = category(url,1)
        return items


@plugin.route('/category/<url>/<page>/')
def category(url,page):
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', url)

    videos = get_videos(url,page)
    items = []
    if videos != []:
        for video in videos:
            
            item = {}
            item['label'] = video['name']
            item['path'] = plugin.url_for('play', name='123' , url=video['href'])
            item['thumbnail'] = video['thumb']
            item['icon'] = video['thumb']
            if 'info' in video:
                info = video['info']
                info['mediatype'] = 'video'
                item['info'] = info
            items.append(item)
        

        if url != 'bianji' and url != 'foryou':
            nextpage = {'label': '[COLOR yellow]下一页[/COLOR]', 'path': plugin.url_for('category', url=url,page=str(int(page)+1))}
            items.append(nextpage)
    return items




@plugin.route('/')
def index():
    categories = get_categories()
    items = [{
        'label': category['name'],
        'path': plugin.url_for('category', url=category['link'],page=1),
    } for category in categories]

    
    return items


@plugin.route('/labels/<label>/')
def show_label(label):
    # 写抓取视频类表的方法
    #
    items = [
        {'label': label},
    ]
    return items

if __name__ == '__main__':
    plugin.run()
