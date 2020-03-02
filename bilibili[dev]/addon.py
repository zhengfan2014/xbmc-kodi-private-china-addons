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


headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}


def get_categories():
    return [{'name':'首页','link':'https://www.bilibili.com/ranking/all/0/0/1'},
            {'name':'新番','link':'https://www.bilibili.com/ranking/bangumi/13/0/3'},
            {'name':'动画','link':'https://www.bilibili.com/ranking/all/1/0/1'},
            {'name':'国创','link':'https://www.bilibili.com/ranking/all/168/0/1'},
            {'name':'音乐','link':'https://www.bilibili.com/ranking/all/3/0/1'},
            {'name':'舞蹈','link':'https://www.bilibili.com/ranking/all/129/0/1'},
            {'name':'游戏','link':'https://www.bilibili.com/ranking/all/4/0/1'},
            {'name':'科技','link':'https://www.bilibili.com/ranking/all/36/0/1'},
            {'name':'数码','link':'https://www.bilibili.com/ranking/all/188/0/1'},
            {'name':'生活','link':'https://www.bilibili.com/ranking/all/160/0/1'},
            {'name':'鬼畜','link':'https://www.bilibili.com/ranking/all/119/0/1'},
            {'name':'时尚','link':'https://www.bilibili.com/ranking/all/155/0/1'},
            {'name':'娱乐','link':'https://www.bilibili.com/ranking/all/5/0/1'},
            {'name':'新人','link':'https://www.bilibili.com/ranking/rookie/0/0/3'}]

def get_videos(category):
#爬视频列表的
    # if int(page) == 1:
    #     pageurl = category
    # else:
    #     pageurl = category + 'index_'+page+'.html'
    pageurl = category

    r = requests.get(pageurl, headers=headers)
    r.encoding = 'UTF-8'
    soup = BeautifulSoup(r.text, "html.parser")
    videos = []
    #videoelements = soup.find('ul', id='list1').find_all('li')
    #videoelements = contenter.find_all("a", attrs={"data-original": True})
    videoelements = soup.find_all('li',class_='rank-item')

    if videoelements is None:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('错误提示', '没有播放源')
    else:
        #dialog = xbmcgui.Dialog()
        #sss = str(len(videoelements))
        #ok = dialog.ok('video数量', sss)

        for videoelement in videoelements:
            
            videoitem = {}
            videoitem['name'] = videoelement.find('img')['alt']
            videoitem['href'] = videoelement.find('a')['href']
            #videoitem['thumb'] = 'aaaa'
            videoitem['genre'] = '豆瓣电影'
            videos.append(videoitem)
        return videos

def get_sources(videolink):
    r = requests.get(videolink, headers=headers)
    r.encoding = 'UTF-8'
    soup = BeautifulSoup(r.text)
    sources = []
    categoryname = soup.find('span',class_='info_category info_ico').find('a').get_text()
    sourcetitle = soup.find('div', class_='context').find('h3', text='播放地址（无需安装插件）')
    thumbimg = soup.find('div', class_='context').find('img')['src']
    if sourcetitle is not None:
        sourcecontenter = sourcetitle.parent
        sourceitems = sourcecontenter.find_all('a')
        for sourceitem in sourceitems:
            videosource = {}
            videosource['name'] = sourceitem['title']
            videosource['thumb'] = thumbimg
            videosource['category'] = categoryname
            videosource['href'] = sourceitem['href']
            sources.append(videosource)
        return sources
    else:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('错误提示', '没有播放源')


@plugin.route('/sources/<url>/')
def sources(url):
    sources = get_sources(url)
    items = [{
        'label': source['name'],
        'path': plugin.url_for('play', url=source['href']),
        'thumbnail': source['thumb'],
        'icon': source['thumb'],
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
        #'path': plugin.url_for('sources', url=video['href']),
	#'thumbnail': video['thumb'],
	#'icon': video['thumb'],
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
