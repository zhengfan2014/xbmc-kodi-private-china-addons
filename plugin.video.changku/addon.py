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

plugin = Plugin()


headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}

@plugin.cached(TTL=60)
def get_mp4(url):
    r = requests.get(url,headers=headers)
    url = r.url
    #url = 'https://www.xinpianchang.com/a10696100'
    rec = requests.get(url,headers=headers)
    rec.encoding = 'utf-8'
    #print(rec.text)
    rectext = rec.text
    str1 = rectext.find('vid: "')
    str2 = rectext[str1:str1+30].find('",')
    vid = rectext[str1+6:str1+str2]
    api = 'https://openapi-vtom.vmovier.com/v3/video/' + vid + '?expand=resource&usage=xpc_web'
    rec = requests.get(api,headers=headers)
    rec.encoding = 'utf-8'
    j = json.loads(rec.text)
    mp4list = {}
    for index in range(len(j['data']['resource']['progressive'])):
        mp4list[j['data']['resource']['progressive'][index]['profile']] = 'http' + j['data']['resource']['progressive'][index]['url'][5:]
        
    return mp4list

def unescape(string):
    string = urllib2.unquote(string).decode('utf8')
    quoted = HTMLParser.HTMLParser().unescape(string).encode('utf-8')
    #转成中文
    return re.sub(r'%u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})', lambda m: unichr(int(m.group(1), 16)), quoted)



def get_categories():
    return [{'name':'首页推荐','link':'shouye'},
            {'name':'最新推荐','link':'listnew'},
            {'name':'热门排行','link':'listhot#rotate-nav'},
            {'name':'星级精选','link':'liststars#rotate-nav'},
            {'name':'#创意#','link':'https://www.vmovier.com/channel/idea'},
            {'name':'#励志#','link':'https://www.vmovier.com/channel/inspiration'},
            {'name':'#搞笑#','link':'https://www.vmovier.com/channel/fun'},
            {'name':'#广告#','link':'https://www.vmovier.com/channel/ad'},
            {'name':'#汽车#','link':'https://www.vmovier.com/channel/qiche'},
            {'name':'#旅行#','link':'https://www.vmovier.com/channel/travel'},
            {'name':'#爱情#','link':'https://www.vmovier.com/channel/love'},
            {'name':'#剧情#','link':'https://www.vmovier.com/channel/story'},
            {'name':'#运动#','link':'https://www.vmovier.com/channel/sports'},
            {'name':'#动画#','link':'https://www.vmovier.com/channel/animation'},
            {'name':'#音乐#','link':'https://www.vmovier.com/channel/mv'},
            {'name':'#科幻#','link':'https://www.vmovier.com/channel/fiction'},
            {'name':'#预告#','link':'https://www.vmovier.com/channel/trailer'},
            {'name':'#纪录#','link':'https://www.vmovier.com/channel/record'},
            {'name':'#混剪#','link':'https://www.vmovier.com/channel/cut'},
            {'name':'#游戏#','link':'https://www.vmovier.com/channel/game'},
            {'name':'#时尚#','link':'https://www.vmovier.com/channel/shishang'},
            {'name':'#实验#','link':'https://www.vmovier.com/channel/experimental'},
            {'name':'#生活#','link':'https://www.vmovier.com/channel/lifeness'}]

@plugin.cached(TTL=60)
def get_shouye():
    videos = []
    url = 'https://www.vmovier.com/'
    rec = requests.get(url,headers=headers)
    #print(rec.text)
    soup = BeautifulSoup(rec.text, 'html.parser')
    filmitem = soup.find('ul',class_='rotate')
    filmitem = filmitem.find_all('li')
    for index in range(len(filmitem)):
        try:
            if filmitem[index].img['alt'] != '':
                videoitem = {}
                videoitem['name'] = filmitem[index].img['alt']
                videoitem['href'] = filmitem[index].a['href']
                videoitem['thumb'] = filmitem[index].img['src']
                videos.append(videoitem)  
        except TypeError:
            print('no')
    return videos

@plugin.cached(TTL=60)
def get_list(link):
    tag = link[4:]

    videos = []
    url = 'https://www.vmovier.com/' + tag
    rec = requests.get(url,headers=headers)
    #print(rec.text)
    soup = BeautifulSoup(rec.text, 'html.parser')
    filmitem = soup.find('ul',class_='index-list clearfix')
    filmitem = filmitem.find_all('li')
    for index in range(len(filmitem)):
         videoitem = {}
         videoitem['name'] = filmitem[index].img['alt']
         videoitem['href'] = 'https://www.vmovier.com' + filmitem[index].a['href']
         videoitem['thumb'] = filmitem[index].img['src']
         videos.append(videoitem)  
    return videos

@plugin.cached(TTL=60)
def get_videos(url):
    #爬视频列表的
    videos = []

    rec = requests.get(url,headers=headers)
    #print(rec.text)
    soup = BeautifulSoup(rec.text, 'html.parser')
    filmitem = soup.find('ul',class_='search-works-list clearfix')
    filmitem = filmitem.find_all('li')
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', j['itemList'][0]['data']['itemList'][0]['data']['content']['data']['playUrl'])

    for index in range(len(filmitem)):
        videoitem = {}
        videoitem['name'] = filmitem[index].img['alt']
        videoitem['href'] = 'https://www.vmovier.com' + filmitem[index].a['href']
        videoitem['thumb'] = filmitem[index].img['src']
        videos.append(videoitem)  
    return videos



@plugin.route('/play/<name>/<url>/')
def play(name,url):
        mp4list = get_mp4(url)
        items = []
        for k,i in mp4list.items():

            item = {'label':'[' + k.encode('utf-8') + ']' + name,'path':i.encode('utf-8'),'is_playable': True}
            items.append(item)
        return items

@plugin.route('/category/<name>/<url>/')
def category(name,url):
    if url == 'shouye' or url[:4] == 'list':
        if url == 'shouye':
            #首页
            videos = get_shouye()
        else:
            #list
            videos = get_list(url)

    else:
        videos = get_videos(url)

    items = [{
        'label': video['name'],
        'path': plugin.url_for('play', name=video['name'].encode('utf-8') , url=video['href']),
        'thumbnail': video['thumb'],
        'icon': video['thumb'],
    } for video in videos]

    #sorted_items = items
    #sorted_items = sorted(items, key=lambda item: item['label'])
    return items




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
