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
cookies = dict(SUB='_2AkMpN-raf8NxqwJRmfoXxGniZIl_ygvEieKfaxsBJRMxHRl-yj92qhFTtRB6ArfENQBVM_xipNLvZYca4pNo4lw7p9Xi')


def get_categories():
    return [{'name':'美食','link':'https://weibo.com/tv?type=channel&first_level_channel_id=4379553934581913'},
            {'name':'游戏','link':'https://weibo.com/tv?type=channel&first_level_channel_id=4379553431261151'},
            {'name':'音乐','link':'https://weibo.com/tv?type=channel&first_level_channel_id=4379158936012261'},
            {'name':'影视','link':'https://weibo.com/tv?type=channel&first_level_channel_id=4379156922732905'},
            {'name':'娱乐综艺','link':'https://weibo.com/tv?type=channel&first_level_channel_id=4379155794457909'},
            {'name':'时尚美妆','link':'https://weibo.com/tv?type=channel&first_level_channel_id=4379553112491541'},
            {'name':'VLOG','link':'https://weibo.com/tv?type=channel&first_level_channel_id=4379162597598697'},
            {'name':'搞笑幽默','link':'https://weibo.com/tv?type=channel&first_level_channel_id=4379552642725861'},
            {'name':'纪录片','link':'https://weibo.com/tv?type=channel&first_level_channel_id=4445109857792664'},
            {'name':'评测','link':'https://weibo.com/tv?type=channel&first_level_channel_id=4453781547450385'},
            {'name':'故事','link':'story'},
            {'name':'热榜','link':'rank'}]

def get_videos(url):
#爬视频列表的
    if url == 'rank' or url == 'story':
        if url == 'rank':
            #日榜
            rec = requests.get('https://weibo.com/tv?type=dayrank',headers=headers,cookies=cookies)
            rec.encoding = 'utf-8'
            rectext = rec.text
            #print(rectext)
            soup = BeautifulSoup(rectext, 'html.parser')
            list = soup.find_all('div',class_='V_list_a')
            videos = []
            for index in range(len(list)):
                videosource = list[index]['video-sources']
                videosource = unescape(videosource)
                videosource = unescape(videosource)
                videosource = videosource[8:]
                mp4 = videosource.split('http:')
                img = list[index].find('img')
                img = img['src']
                if img[0:4] == 'http':
                    img = 'http' + img[5:]
                else:
                    img = 'http:' + img
                title = list[index].find('h3')
                title = title.text
                title = title.replace(' ', '').replace('\n','')
                if len(title) > 40:
                    title = title[:40] + '...'
                title = '['+str(index+1)+']' + title
                videoitem = {}
                videoitem['name'] = title
                videoitem['thumb'] = img
                videoitem['href'] = 'http:' + mp4[len(mp4)-1]
                videos.append(videoitem)
        else:
            #故事
            q = '11'
            rec = requests.get('https://weibo.com/tv?type=story',headers=headers,cookies=cookies)
            rec.encoding = 'utf-8'
            rectext = rec.text
            #print(rectext)
            soup = BeautifulSoup(rectext, 'html.parser')
            list = soup.find_all('div',class_='V_list_b')
            videos = []
            for index in range(len(list)):
                if list[index]['action-data'][:9] != 'type=live':


                    videosource = list[index]['video-sources']
                    videosource = unescape(videosource)
                    videosource = unescape(videosource)
                    videosource = videosource[8:]
                    mp4 = videosource.split('http:')
                    img = list[index].find('img')
                    img = img['src']
                    if img[0:4] == 'http':
                        img = 'http' + img[5:]
                    else:
                        img = 'http:' + img
                    username = list[index].find('div',class_='V_box_col V_autocut')
                    username = username.text
                    like = list[index].find('div',class_='like')
                    like = like.text
                    likenum = re.findall(r'\d+',like)
                    videoitem = {}
                    videoitem['name'] = username.encode('utf-8') + ' 分享的短视频 [赞' + str(likenum[0])+ ']'
                    videoitem['thumb'] = img
                    videoitem['href'] = 'http:' + mp4[len(mp4)-1]
                    videos.append(videoitem)

    
                else:
                    index = index +1










    else:
        #普通列表
        rec = requests.get(url,headers=headers,cookies=cookies)
        rec.encoding = 'utf-8'
        rectext = rec.text
        #print(rectext)
        soup = BeautifulSoup(rectext, 'html.parser')
        list = soup.find_all('div',class_='V_list_a')
        videos = []
        for index in range(len(list)):
            videosource = list[index]['video-sources']
            videosource = unescape(videosource)
            videosource = unescape(videosource)
            videosource = videosource[8:]
            mp4 = videosource.split('http:')
            img = list[index].find('img')
            img = img['src']
            if img[0:4] == 'http':
                img = 'http' + img[5:]
            else:
                img = 'http:' + img
            title = list[index].find('h3')
            videoitem = {}
            videoitem['name'] = title.text
            videoitem['thumb'] = img
            videoitem['href'] = 'http:' + mp4[len(mp4)-1]
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
        'path': video['href'],
	'thumbnail': video['thumb'],
	'icon': video['thumb'],
        'is_playable': True,
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
