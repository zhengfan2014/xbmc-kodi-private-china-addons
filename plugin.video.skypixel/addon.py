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


def unescape(string):
    string = urllib2.unquote(string).decode('utf8')
    quoted = HTMLParser.HTMLParser().unescape(string).encode('utf-8')
    #转成中文
    return re.sub(r'%u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})', lambda m: unichr(int(m.group(1), 16)), quoted)


headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}


def get_categories():
    return [{'name':'探索', 'link':'https://www.skypixel.com/api/v2/works?lang=zh-Hans&platform=web&device=desktop&sort=hot&filter=featured:true&limit=100&offset=0'},
            {'name':'自然', 'link':'https://www.skypixel.com/api/v2/topics/nature/works?lang=zh-Hans&platform=web&device=desktop&sort=hot&filter=featured:true&limit=100&offset=40'},
            {'name':'城市','link':'https://www.skypixel.com/api/v2/topics/city/works?lang=zh-Hans&platform=web&device=desktop&sort=hot&filter=featured:true&limit=100&offset=20'},
            {'name':'运动','link':'https://www.skypixel.com/api/v2/topics/sport/works?lang=zh-Hans&platform=web&device=desktop&sort=hot&filter=featured:true&limit=100&offset=20'},
            {'name':'人物','link':'https://www.skypixel.com/api/v2/topics/people/works?lang=zh-Hans&platform=web&device=desktop&sort=hot&filter=featured:true&limit=100&offset=60'},
            {'name':'签约摄影师','link':'https://www.skypixel.com/api/v2/photographers/contract-works?lang=zh-Hans&platform=web&device=desktop&sort=hot&slug=creator_works&filter=featured:true&limit=100&offset=40'}]

@plugin.cached(TTL=60)
def get_videos(url):
    #爬视频列表的
    videos = []

    rec = requests.get(url,headers=headers)
    #print(rec.text)
    j = json.loads(rec.text)
    for index in range(len(j['data']['items'])):
        if j['data']['items'][index]['type'] == 'video':
            videoitem = {}
            videoitem['name'] = j['data']['items'][index]['title']
            videoitem['href'] = j['data']['items'][index]['cdn_url']['large']
            videoitem['thumb'] = j['data']['items'][index]['image']['large']
            videos.append(videoitem)  

    return videos



@plugin.route('/play/<name>/<url>/')
def play(name,url):
        url = url[:-8]
        items = []
        
        item = {'label':'[' + '1080P'+ ']' + name,'path':url + '1080.mp4','is_playable': True}
        items.append(item)
        item = {'label':'[' + '720P'+ ']' + name,'path':url + '720.mp4','is_playable': True}
        items.append(item)
        item = {'label':'[' + '480P'+ ']' + name,'path':url + 'sd.mp4','is_playable': True}
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
