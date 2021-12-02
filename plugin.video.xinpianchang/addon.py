#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from xbmcswift2 import Plugin
import requests
from bs4 import BeautifulSoup
import xbmcgui
import base64
import json
import urllib
import sys
from html.parser import HTMLParser
import re

plugin = Plugin()

@plugin.cached(TTL=60)
def get_mp4(url):
    #url = 'https://www.xinpianchang.com/a10696100'
    headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
    rec = requests.get(url,headers=headers)
    rec.encoding = 'utf-8'
    rectext = rec.text
    soup = BeautifulSoup(rectext, 'html.parser')
    # 创作者
    user = soup.find('ul',class_="creator-list").find_all('li')
    users = []
    for i in range(len(user)):
        users.append({"name":user[i].find('span',class_="name").text.encode("utf-8"),"role":user[i].find('span',class_="roles").text.encode("utf-8"),"thumbnail":user[i].find('img')["_src"].encode("utf-8")})
    vid = re.search("(?<=vid = \").*?(?=\")", rectext).group()
    modeServerAppKey = re.search(
        "(?<=modeServerAppKey = \").*?(?=\")", rectext).group()
    api = 'https://mod-api.xinpianchang.com/mod/api/v2/media/' + vid + \
        '?appKey=' + modeServerAppKey + '&extend=userInfo,userStatus'
    rec = requests.get(api,headers=headers)
    rec.encoding = 'utf-8'
    j = json.loads(rec.text)
    mp4list = {}
    for index in range(len(j['data']['resource']['progressive'])):
        mp4list[j['data']['resource']['progressive'][index]['profile']
                ] = 'http' + j['data']['resource']['progressive'][index]['url'][5:]
    # 简介
    '''
    desc = soup.find('i',class_="play-counts").text.encode('utf-8') + " 播放 · " + soup.find('span',class_="like-counts").text.encode('utf-8') + " 赞 · " + soup.find('span',class_="collect-counts").text.encode('utf-8') +" 收藏\n"
    desc += soup.find('span',class_='update-time').text.encode('utf-8') +"\n"
    desc += "[COLOR red]" + soup.find('span',class_='authorize-con').text.encode('utf-8') + "[/COLOR]\n\n"
    desc += j['data']['description'].encode('utf-8')
    '''
    return {"mp4":mp4list,"user":users,"genre":j['data']['categories'],"tag":j['data']['keywords'],'desc':'','img':j['data']['cover']}

def unescape(string):
    string = urllib.unquote(string).decode('utf8')
    quoted = HTMLParser.HTMLParser().unescape(string).encode('utf-8')
    #转成中文
    return re.sub(r'%u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})', lambda m: unichr(int(m.group(1), 16)), quoted)


headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}


def get_categories():
    return [{'name':'热门', 'link':'https://www.xinpianchang.com/channel/index/type-/sort-like/duration_type-0/resolution_type-/'},
            {'name':'广告', 'link':'https://www.xinpianchang.com/channel/index/id-1/sort-pick/type-/duration_type-0/resolution_type-/'},
            {'name':'宣传片','link':'https://www.xinpianchang.com/channel/index/id-16/sort-pick/duration_type-0/resolution_type-/type-/'},
            {'name':'MV','link':'https://www.xinpianchang.com/channel/index/id-27/sort-pick/duration_type-0/resolution_type-/type-'},
            {'name':'短视频','link':'https://www.xinpianchang.com/channel/index/id-29/sort-pick/duration_type-0/resolution_type-/type-'},
            {'name':'剧情短片','link':'https://www.xinpianchang.com/channel/index/id-31/sort-pick/duration_type-0/resolution_type-/type-'},
            {'name':'纪录','link':'https://www.xinpianchang.com/channel/index/id-49/sort-pick/duration_type-0/resolution_type-/type-'},
            {'name':'特殊摄影','link':'https://www.xinpianchang.com/channel/index/id-61/sort-pick/duration_type-0/resolution_type-/type-'},
            {'name':'动画','link':'https://www.xinpianchang.com/channel/index/id-69/sort-pick/duration_type-0/resolution_type-/type-'},
            {'name':'创意混剪','link':'https://www.xinpianchang.com/channel/index/id-76/sort-pick/duration_type-0/resolution_type-/type-'},
            {'name':'影视','link':'https://www.xinpianchang.com/channel/index/id-81/sort-pick/duration_type-0/resolution_type-/type-'},
            {'name':'Vlog','link':'https://www.xinpianchang.com/channel/index/id-129/sort-pick/duration_type-0/resolution_type-/type-'}]

@plugin.cached(TTL=60)
def get_videos(url):
    #爬视频列表的
    videos = []

    rec = requests.get(url,headers=headers)
    rec.encoding = 'utf-8'
    #print(rec.text)
    soup = BeautifulSoup(rec.text, 'html.parser')
    filmitem = soup.find_all('li',class_='enter-filmplay')

    for index in range(len(filmitem)):
        img = filmitem[index].find('img',class_='lazy-img')
        title = filmitem[index].find('p',class_='fs_14 fw_600 c_b_3 line-hide-1')
        videoitem = {}
        videoitem['name'] = title.text
        videoitem['href'] = 'https://www.xinpianchang.com/a'+filmitem[index]['data-articleid']
        videoitem['thumb'] = img['_src']
        videos.append(videoitem)  
    return videos



@plugin.route('/play/<name>/<url>/')
def play(name,url):
        mp4list = get_mp4(url)
        items = []
        for k,i in mp4list['mp4'].items():

            item = {'label':'[' + k + ']' + name,'path':i,'is_playable': True}
            items.append(item)
        return items

@plugin.route('/category/<name>/<url>/')
def category(name,url):
    videos = get_videos(url)
   
    items = [{
        'label': video['name'],
        'path': plugin.url_for('play', name= video['name'].encode('utf-8'), url=video['href']),
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
