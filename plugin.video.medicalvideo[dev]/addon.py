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

def get_real_url(url):
    rs = requests.get(url,headers=headers,timeout=2)
    return rs.url

def unescape(string):
    string = urllib2.unquote(string).decode('utf8')
    quoted = HTMLParser.HTMLParser().unescape(string).encode('utf-8')
    #转成中文
    return re.sub(r'%u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})', lambda m: unichr(int(m.group(1), 16)), quoted)


plugin = Plugin()


headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}


def get_categories():
    return [{'name':'七环视频','link':'https://www.thepaper.cn/load_video_chosen.jsp?channelID=26916&nodeid=26913&pageidx='},
            {'name':'温度计','link':'https://www.thepaper.cn/load_video_chosen.jsp?channelID=26916&nodeid=26965&pageidx='},
            {'name':'一级现场','link':'https://www.thepaper.cn/load_video_chosen.jsp?channelID=26916&nodeid=26908&pageidx='},
            {'name':'world湃','link':'https://www.thepaper.cn/load_video_chosen.jsp?channelID=26916&nodeid=27260&pageidx='},
            {'name':'湃客科技','link':'https://www.thepaper.cn/load_video_chosen.jsp?channelID=26916&nodeid=26907&pageidx='},
            {'name':'纪录湃','link':'https://www.thepaper.cn/load_video_chosen.jsp?channelID=26916&nodeid=33168&pageidx='},
            {'name':'围观','link':'https://www.thepaper.cn/load_video_chosen.jsp?channelID=26916&nodeid=26911&pageidx='},
            {'name':'@所有人','link':'https://www.thepaper.cn/load_video_chosen.jsp?channelID=26916&nodeid=26918&pageidx='},
            {'name':'大都会','link':'https://www.thepaper.cn/load_video_chosen.jsp?channelID=26916&nodeid=26906&pageidx='},
            {'name':'追光灯','link':'https://www.thepaper.cn/load_video_chosen.jsp?channelID=26916&nodeid=26909&pageidx='},
            {'name':'运动装','link':'https://www.thepaper.cn/load_video_chosen.jsp?channelID=26916&nodeid=26910&pageidx='},
            {'name':'健寻记','link':'https://www.thepaper.cn/load_video_chosen.jsp?channelID=26916&nodeid=26914&pageidx='},
            {'name':'AI播报','link':'https://www.thepaper.cn/load_video_chosen.jsp?channelID=26916&nodeid=82188&pageidx='},
            {'name':'眼界','link':'https://www.thepaper.cn/load_video_chosen.jsp?channelID=26916&nodeid=89035&pageidx='}]

def get_videos(url):
    #爬视频列表的
    videos = []

    rec = requests.get(url,headers=headers)
    #print(rec.text)
    rec.encoding = ('utf-8')

    soup = BeautifulSoup(rec.text, 'html.parser')

    imgsrc = soup.find_all('img')
    ahref = soup.find_all('a',class_='play has_pic')
    title = soup.find_all('div',class_='video_title')
    #标题
    #print(j['itemList'][0]['data']['header']['title'] + ' - ' + j['itemList'][0]['data']['header']['subTitle'])
    #视频数：
    #print(j['itemList'][0]['data'])
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', j['itemList'][0]['data']['itemList'][0]['data']['content']['data']['playUrl'])

    for index in range(len(imgsrc)):
        titletext = title[index].text
        titletext = titletext.replace('	', '')
        imgsrcurl = imgsrc[index]['src']
        videoitem = {}
        videoitem['name'] = titletext
        videoitem['href'] = 'https://thepaper.cn/' + ahref[index]['href']
        videoitem['thumb'] = 'http' + imgsrcurl[5:]
        videos.append(videoitem)  
    return videos



@plugin.route('/play/<name>/<url>/')
def play(name,url):
        rec = requests.get(url,headers=headers)
        items = []
        soup = BeautifulSoup(rec.text, 'html.parser')
        #print(rec.text)
        mp4 = soup.find('source',type='video/mp4')
        #print(mp4['src'])
        item = {'label': name,'path':mp4['src'],'is_playable': True}
        items.append(item)
        return items

@plugin.route('/category/<name>/<url>/')
def category(name,url):
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', url)

    videos = get_videos(url)
    items = [{
        'label': video['name'],
        'path': plugin.url_for('play', name='最高清晰度 - 本地解析' , url=video['href']),
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
