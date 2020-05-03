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

useragent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}


def get_categories():
    return [{'name':'新番放送','link':'http://www.bimibimi.me/type/riman/'},
            {'name':'国产动漫','link':'http://www.bimibimi.me/type/guoman/'},
            {'name':'番组计划','link':'http://www.bimibimi.me/type/fanzu/'},
            {'name':'剧场动画','link':'http://www.bimibimi.me/type/juchang/'},
            {'name':'影视','link':'http://www.bimibimi.me/type/move/'}]

@plugin.cached(TTL=60)
def get_videos(url):
    #爬视频列表的
    videos = []
    r = requests.get(url,headers=headers)
    r.encoding = 'utf-8'
    #print(r.text)
    soup = BeautifulSoup(r.text, 'html.parser')
    linelist = soup.find('ul',class_='drama-module clearfix tab-cont')
    #print(len(linelist))
    alist = linelist.find_all('a',class_='img')
    plist = linelist.find_all('span',class_='fl')
    for i in range(len(alist)):
        videoitem = {}
        videoitem['name'] =  alist[i]['title'] + '[' + plist[i].text + ']' 
        videoitem['href'] =  'http://www.bimibimi.me' + alist[i]['href']
        videoitem['thumb'] = alist[i].img['data-original']
        videos.append(videoitem)
    return videos

@plugin.cached(TTL=60)
def get_source(url):
    #爬视频列表的
    videos = []
    r = requests.get(url,headers=headers)
    #print(r.text)
    soup = BeautifulSoup(r.text, 'html.parser')
    linelist = soup.find_all('div',class_='play_box')
    #print(len(linelist))

    sourcelist = []
    for index in range(len(linelist)):
        alist = linelist[index].find_all('a')
        duopdict = {}
        for i in range(len(alist)):
            duopdict[alist[i].text] = alist[i]['href']
        #print('------------'*30)
        sourcelist.append(duopdict)

    for index in range(len(sourcelist)):
        videoitem = {}
        videoitem['name'] = '播放线路' + str(index+1)
        videoitem['href'] = str(sourcelist[index])
        videos.append(videoitem)
    return videos

@plugin.cached(TTL=60)
def get_mp4(url):
    r = requests.get(url,headers=headers)
    rtext = r.text
    soup = BeautifulSoup(rtext, 'html.parser')
    title = soup.find('title')
    str1 = rtext.find('var player_data=')
    str2 = rtext.find('</script><script type="text/javascript"')
    cutjson = rtext[str1+16:str2]
    #print(cutjson)
    j = json.loads(cutjson)
    #向接口发送请求
    if j['from']:
        if j['from'] == 'niux':
            apiurl = 'http://182.254.167.161/danmu/niux.php?id=' + j['url']
        else:
            apiurl = 'http://182.254.167.161/danmu/play.php?url=' + j['url']
        r = requests.get(apiurl,headers=headers)
        rtext = r.text
        #print(rtext)
        soup = BeautifulSoup(r.text, 'html.parser')
        source = soup.find('source',type='video/mp4')
        mp4 = source['src']
        rt = []
        rt.append(title.text)
        rt.append(mp4)
    return rt

@plugin.route('/play/<url>/')
def play(url):
        
        items = []
        #print(rec.text)
        mp4 = get_mp4(url)
        #dialog = xbmcgui.Dialog()
        #ok = dialog.ok('错误提示',str(mp4))
        #print(mp4['src'])
        item = {'label': mp4[0],'path':mp4[1],'is_playable': True,'info':('video')}
        items.append(item)
        return items

@plugin.route('/duop/<list>/')
def duop(list):
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', list)
    list = eval(list)
    
    #j = json.loads(list)
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', str(len(list)))
    items = []
    for k,i in list.items():
        item = {'label':k.encode('utf-8'),'path':plugin.url_for('play',url='http://www.bimibimi.me' + i)}
        items.append(item)
    return items

@plugin.route('/source/<url>/')
def source(url):
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', url)

    sources = get_source(url)
    items = [{
        'label': s['name'],
        'path': plugin.url_for('duop', list=s['href']),
    } for s in sources]

    sorted_items = items
    #sorted_items = sorted(items, key=lambda item: item['label'])
    return sorted_items

@plugin.route('/category/<name>/<url>/')
def category(name,url):
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', url)

    videos = get_videos(url)
    items = [{
        'label': video['name'],
        'path': plugin.url_for('source', url=video['href']),
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
        'path': plugin.url_for('category', name=category['name'] , url=category['link']),
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
