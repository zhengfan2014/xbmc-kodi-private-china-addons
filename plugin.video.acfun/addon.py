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



def unescape(string):
    string = urllib2.unquote(string).decode('utf8')
    quoted = HTMLParser.HTMLParser().unescape(string).encode('utf-8')
    #转成中文
    return re.sub(r'%u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})', lambda m: unichr(int(m.group(1), 16)), quoted)


plugin = Plugin()


headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}


def get_categories():
    return [{'name':'综合','link':'https://www.acfun.cn/rest/pc-direct/rank/channel?channelId=&subChannelId=&rankLimit=100&rankPeriod=WEEK'},
            {'name':'番剧','link':'https://www.acfun.cn/rest/pc-direct/rank/channel?channelId=155&subChannelId=&rankLimit=30&rankPeriod=WEEK'},
            {'name':'动画','link':'https://www.acfun.cn/rest/pc-direct/rank/channel?channelId=1&subChannelId=&rankLimit=100&rankPeriod=WEEK'},
            {'name':'娱乐','link':'https://www.acfun.cn/rest/pc-direct/rank/channel?channelId=60&subChannelId=&rankLimit=100&rankPeriod=WEEK'},
            {'name':'生活','link':'https://www.acfun.cn/rest/pc-direct/rank/channel?channelId=201&subChannelId=&rankLimit=100&rankPeriod=WEEK'},
            {'name':'音乐','link':'https://www.acfun.cn/rest/pc-direct/rank/channel?channelId=58&subChannelId=&rankLimit=100&rankPeriod=WEEK'},
            {'name':'舞蹈·偶像','link':'https://www.acfun.cn/rest/pc-direct/rank/channel?channelId=123&subChannelId=&rankLimit=100&rankPeriod=WEEK'},
            {'name':'游戏','link':'https://www.acfun.cn/rest/pc-direct/rank/channel?channelId=59&subChannelId=&rankLimit=100&rankPeriod=WEEK'},
            {'name':'科技','link':'https://www.acfun.cn/rest/pc-direct/rank/channel?channelId=70&subChannelId=&rankLimit=100&rankPeriod=WEEK'},
            {'name':'影视','link':'https://www.acfun.cn/rest/pc-direct/rank/channel?channelId=68&subChannelId=&rankLimit=100&rankPeriod=WEEK'},
            {'name':'体育','link':'https://www.acfun.cn/rest/pc-direct/rank/channel?channelId=69&subChannelId=&rankLimit=100&rankPeriod=WEEK'},
            {'name':'鱼塘','link':'https://www.acfun.cn/rest/pc-direct/rank/channel?channelId=125&subChannelId=&rankLimit=100&rankPeriod=WEEK'}]

def get_search(keyword, page):
    # if int(page) == 1:
    #     pageurl = category
    # else:
    #     pageurl = category + 'index_'+page+'.html'
    serachUrl = 'https://www.acfun.cn/rest/pc-direct/search/video?keyword=' + keyword + '&pCursor=' + str(page)

    r = requests.get(serachUrl, headers=headers)
    r.encoding = 'UTF-8'
    rtext = r.text
    j = json.loads(rtext)
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', str(j['videoList']))
    videos = []
    #videoelements = soup.find('ul', id='list1').find_all('li')
    #videoelements = contenter.find_all("a", attrs={"data-original": True})
    #videoelements = soup.find('ul', id='list1').find_all('a', {'data-origin', True})
    #videoelements = soup.find_all('li', class_='activeclearfix')
    for index in range(len(j['videoList'])):
        videoitem = {}
        videoitem['name'] = j['videoList'][index]['title']
        videoitem['href'] = 'https://m.acfun.cn/v?ac='+ str(j['videoList'][index]['id'])
        videoitem['thumb'] = j['videoList'][index]['coverUrl']
        videoitem['genre'] = '喜剧片'
        videos.append(videoitem)
    return videos






def get_videos(category):
#爬视频列表的
    pageurl = category

    r = requests.get(pageurl, headers=headers)
    r.encoding = 'UTF-8'
    rtext= r.text
    j = json.loads(rtext.encode('utf-8'))
    #j是字典

    k = j['rankList']
    
    videos = []
    #videoelements = soup.find('ul', id='list1').find_all('li')
    #videoelements = contenter.find_all("a", attrs={"data-original": True})
    

    #if videoelements is None:
       # dialog = xbmcgui.Dialog()
       # ok = dialog.ok('错误提示', '没有播放源')
    #else:
        #dialog = xbmcgui.Dialog()
        #sss = str(len(videoelements))
        #ok = dialog.ok('video数量', sss)

    for index in range(len(k)):
            item = k[index]
            videoitem = {}
            videoitem['name'] = item['contentTitle']
            videoitem['href'] = item['shareUrl']
            videoitem['thumb'] = item['coverUrl']
            videos.append(videoitem)
    return videos

def get_sources(url):
    ifmurl = re.match('https://m.acfun.cn',url)
    if ifmurl != None:
        url = 'https://www' + url[9:21] + 'ac' + url[25:]
    
    sources = []
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', url)
    rec = requests.get(url,headers=headers)
    rec.encoding = 'utf-8'
    soup = BeautifulSoup(rec.text, "html5lib")
    if404 = soup.find_all('div', class_='img404')
    
        
        #print(rec.text)
    rectext = rec.text

    cutjson = rectext.encode('utf-8')
    str1 = cutjson.find('window.pageInfo = window.videoInfo = ')
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', str(str1))
    if str1 != -1:
        str2 = cutjson.find('window.qualityConfig =')
        videoinfo = cutjson[str1+37:str2-10]
    


        j = json.loads(videoinfo)
        if len(j['videoList']) == 1:
            
            #print(j['title'])
            #print(j['description'])
            videosource = {}
            #print('视频标题：')
            videosource['name'] = j['title']
            #print('视频图片：')
            #videosource['thumb'] = '12'
            #print('视频地址：')
            videosource['href'] = plugin.url_for('play', url=url)
            #videosource['category'] = '番剧'
            sources.append(videosource)
            return sources
        else:
             for index in range(len(j['videoList'])):
                 videosource = {}
                 videosource['name'] = j['videoList'][index]['title']
                 videosource['href'] = plugin.url_for('play', url=url + '_' +str(index+1))
                 sources.append(videosource)
             return sources
    else:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('错误提示', '错误404，咦？世界线变动了，你好像来到了奇怪的地方。看看其他内容吧~')




@plugin.route('/sources/<url>/')
def sources(url):
    sources = get_sources(url)
    items = [{
        'label': source['name'],
        'path': source['href'],
        #'thumbnail': source['thumb'],
        #'icon': source['thumb'],
    } for source in sources]
    sorted_items = sorted(items, key=lambda item: item['label'])
    return sorted_items


@plugin.route('/category/<url>/')
def category(url):
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', url)


    videos = get_videos(url)
    items = [{
        'label': video['name'],
        'path': plugin.url_for('sources', url=video['href']),
	'thumbnail': video['thumb'],
	'icon': video['thumb'],
    } for video in videos]

    sorted_items = items
    #sorted_items = sorted(items, key=lambda item: item['label'])
    return sorted_items


@plugin.route('/')
def index():
    categories = get_categories()
    items = [{
        'label': category['name'],
        'path': plugin.url_for('category', url=category['link']),
    } for category in categories]

    items.append({
        'label': u'[COLOR yellow]搜索[/COLOR]',
        'path': plugin.url_for('search'),
    })
    items.append({
        'label': u'[COLOR yellow]输入ac号[/COLOR]',
        'path': plugin.url_for('ac'),
    })
    return items

@plugin.route('/search')
def search():
    keyboard = xbmc.Keyboard('', '请输入搜索内容')
    xbmc.sleep(1500)
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        keyword = keyboard.getText()
        #url = HOST_URL + '/index.php?m=vod-search&wd=' + keyword
        # https://www.nfmovies.com/search.php?page=1&searchword='+keyword+'&searchtype=

        videos = get_search(keyword, 1)
        items = [{
            'label': video['name'],
            'path': plugin.url_for('sources', url=video['href']),
            'thumbnail': video['thumb'],
            'icon': video['thumb']
        } for video in videos]

        sorted_items = items
        # sorted_items = sorted(items, key=lambda item: item['label'])
        #nextpage = {'label': ' 下一页', 'path': plugin.url_for('searchMore', keyword=keyword, page=2)}
        #sorted_items.append(nextpage)
        return sorted_items




@plugin.route('/ac')
def ac():
    keyboard = xbmc.Keyboard('', '请输入ac号：')
    xbmc.sleep(1500)
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        keyword = keyboard.getText()
        #url = HOST_URL + '/index.php?m=vod-search&wd=' + keyword
        # https://www.nfmovies.com/search.php?page=1&searchword='+keyword+'&searchtype=

        sources = get_sources('https://www.acfun.cn/v/ac'+str(keyword))
        items = [{
            'label': source['name'],
            'path': source['href'],
            #'thumbnail': source['thumb'],
            #'icon': source['thumb'],
        } for source in sources]
        sorted_items = sorted(items, key=lambda item: item['label'])
        return sorted_items


@plugin.route('/play/<url>/')
def play(url):

    rec = requests.get(url,headers=headers)
    #print(rec.text)
    rectext = rec.text
    cutjson = rectext.encode('utf-8')
    str1 = cutjson.find('window.pageInfo = window.videoInfo = ')
    str2 = cutjson.find('window.qualityConfig =')
    videoinfo = cutjson[str1+37:str2-10]
    j = json.loads(videoinfo)


    #print(j['title'])
    #print(j['description'])
    videojson =j ['currentVideoInfo']['ksPlayJson']
    j2 = json.loads(videojson)


    items = []
    if len(j2['adaptationSet']['representation']) == 1 :
        title = j2['adaptationSet']['representation'][0]['qualityType']
        path = j2['adaptationSet']['representation'][0]['url']
        item = {'label': title,'path':path,'is_playable': True}
        
        items.append(item)
        return items
    else:
        for index in range(len(j2['adaptationSet']['representation'])):
            #print(j2['adaptationSet']['representation'][index]['qualityType'])
            #print(j2['adaptationSet']['representation'][index]['url'])
            title = j2['adaptationSet']['representation'][index]['qualityType']
            path = j2['adaptationSet']['representation'][index]['url']
            item = {'label': title,'path':path,'is_playable': True}
        
            items.append(item)
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
