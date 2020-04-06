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
import cfscrape



def unescape(string):
    string = urllib2.unquote(string).decode('utf8')
    quoted = HTMLParser.HTMLParser().unescape(string).encode('utf-8')
    #转成中文
    return re.sub(r'%u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})', lambda m: unichr(int(m.group(1), 16)), quoted)


plugin = Plugin()

useragent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}

def jserror(html):
    dialog = xbmcgui.Dialog()
    ok = dialog.ok('错误提示',str(html))
    dialog = xbmcgui.Dialog()
    ok = dialog.ok('错误提示', '出现了奇怪的错误呢，可能是你的ip进该网站黑名单了呢，24小时后再试吧（或者换个ip？）\n如果换ip也不能访问可能网站页面改了解析失败了呢，耐心等作者修复')
    return 1


def get_categories():
    return [{'name':'编辑推荐','link':'https://api.clicli.us/posts?status=public&sort=&tag=%E6%8E%A8%E8%8D%90&uid=&page=1&pageSize=10'},
            {'name':'新番表','link':'https://api.clicli.us/posts?status=nowait&sort=%E6%96%B0%E7%95%AA&tag=&uid=&page=1&pageSize=100'},
            {'name':'排行','link':'https://api.clicli.us/rank'},
            {'name':'最近更新','link':'https://api.clicli.us/posts?status=public&sort=bgm&tag=&uid=&page=1&pageSize=30'}]

@plugin.cached(TTL=60)
def get_videos(url):
    #爬视频列表的
    videos = []
    scraper = cfscrape.create_scraper()
    html = scraper.get(url).content
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', str(html))
    try:
        j = json.loads(html)
        for index in range(len(j['posts'])):
            con = j['posts'][index]['content']
            img = re.search('!\\[[^\\]]+\\]\\([^\\)]+\\)', con)
            videoitem = {}
            videoitem['name'] = '[' + j['posts'][index]['sort'].encode('utf-8') + ']' + j['posts'][index]['title'].encode('utf-8') + ' (' + j['posts'][index]['time'].encode('utf-8') + '更新)'
            videoitem['href'] = j['posts'][index]['id']
            videoitem['thumb'] = img.group()[7:-1]
            videos.append(videoitem)  
    except ValueError:
        jserror(html)
    return videos

@plugin.cached(TTL=60)
def get_duop(id):
    #爬视频列表的
    videos = []
    scraper = cfscrape.create_scraper()
    html = scraper.get('https://api.clicli.us/videos?pid=' + str(id) +'&page=1&pageSize=150').content
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', str(html))
    try:
        j = json.loads(html)
        pnum = 1
        for index in range(len(j['videos'])):
            pp = str(pnum)
            pp = pp.encode('utf-8')
            videoitem = {}
            videoitem['name'] = '[' + pp + ']' + j['videos'][index]['title'].encode('utf-8')
            videoitem['href'] = j['videos'][index]['content']
            videos.append(videoitem)
            pnum += 1  
    except ValueError:
        jserror(html)
    except TypeError:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('错误提示', '这个不是视频哦')
    return videos

@plugin.cached(TTL=60)
def get_mp4(url):
    url = 'https://jx.clicli.us/jx?url=' + url
    scraper = cfscrape.create_scraper()
    html = scraper.get(url).content
    try:
        j = json.loads(html)
        mp4 = j['url'] 
    except ValueError:
        jserror(html)
    return mp4

@plugin.route('/play/<name>/<url>/')
def play(name,url):
        
        items = []
        #print(rec.text)
        mp4 = get_mp4(url)
        #print(mp4['src'])
        item = {'label': name,'path':mp4,'is_playable': True}
        items.append(item)
        return items

@plugin.route('/duop/<id>/')
def duop(id):
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', url)

    videos = get_duop(id)
    items = [{
        'label': video['name'],
        'path': plugin.url_for('play', name=video['name'] , url=video['href']),
    } for video in videos]

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
        'path': plugin.url_for('duop', id=video['href']),
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
