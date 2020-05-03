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

cache = plugin.get_storage('cache',TTL=60)
headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}


def get_categories():
    return [{'name':'妇产科疾病','link':'1'},
            {'name':'儿科疾病','link':'2'},
            {'name':'神经系统疾病','link':'3'},
            {'name':'呼吸系统疾病','link':'4'},
            {'name':'消化系统疾病','link':'5'},
            {'name':'心脑血管系统疾病','link':'6'},
            {'name':'内分泌系统疾病','link':'7'},
            {'name':'泌尿系统疾病','link':'8'},
            {'name':'血液系统疾病','link':'9'},
            {'name':'骨科疾病','link':'10'},
            {'name':'肿瘤疾病','link':'11'},
            {'name':'口腔疾病','link':'12'},
            {'name':'皮肤疾病','link':'13'},
            {'name':'眼科疾病','link':'14'},
            {'name':'耳鼻喉疾病','link':'15'},
            {'name':'生殖系统疾病','link':'16'},
            {'name':'精神心理疾病','link':'17'},
            {'name':'急诊科疾病','link':'18'},
            {'name':'感染科疾病','link':'19'},
            {'name':'肛肠科疾病','link':'20'},
            {'name':'血管外科','link':'21'},
            {'name':'性病','link':'22'},
            {'name':'风湿免疫科疾病','link':'23'},
            {'name':'康复科','link':'24'},
            {'name':'护理常识','link':'25'},
            {'name':'药事药理','link':'26'},
            {'name':'医美整形','link':'27'},
            {'name':'中医中药','link':'28'},
            {'name':'辅助检查及治疗','link':'29'},
            {'name':'罕见病','link':'30'},
            {'name':'其他','link':'31'}]

def get_videos(cag):
    #爬视频列表的
    videos = []
    if 'home' in cache:
        rectext = cache['home']
    else:
        url = 'https://www.mvyxws.com/'
        rec = requests.get(url,headers=headers)
        #print(rec.text)
        rec.encoding = ('utf-8')
        rectext = rec.text
        cache['home'] = rectext
    soup = BeautifulSoup(rectext, 'html.parser')

    cag = int(cag)
    filmitem = soup.find_all('div',class_='category')
    #print(filmitem[cag])
    filmitem = filmitem[cag].find_all('a')
    #print(len(filmitem))
    for index in range(len(filmitem)):
        #print()
        videoitem = {}
        videoitem['name'] = filmitem[index].parent.parent.h2.text[1:] + u':' + filmitem[index]['title']
        videoitem['href'] = 'https://www.mvyxws.com'+filmitem[index]['href']
        videos.append(videoitem)  

    return videos

@plugin.cached(TTL=60)
def get_duop(url):
    videos = []
    rec = requests.get(url,headers=headers)
    cag = 1
    soup = BeautifulSoup(rec.text, 'html.parser')
    filmitem = soup.find('ul',class_='jb-list')
    #print(filmitem[cag])
    thumb = soup.find('div',class_='tx')
    thumb = thumb.img['src']
    filmitem = filmitem.find_all('li')
    #print(len(filmitem))
    for index in range(len(filmitem)):
        videoitem = {}
        videoitem['name'] = filmitem[index].a['title']
        videoitem['href'] = 'https://www.mvyxws.com'+filmitem[index].a['href']
        videoitem['thumb'] = 'https://www.mvyxws.com' + thumb
        videos.append(videoitem)  
    return videos

@plugin.cached(TTL=60)
def get_mp4_request(url):
    rec = requests.get(url,headers=headers)
    rec.encoding = 'utf-8'
    rect = rec.text
    return rect

@plugin.cached(TTL=60)
def get_mp4(rect):
    #rec = requests.get(url,headers=headers)

    #rect = rec.text
    str1 = rect.find('fileID:')
    str2 = rect.find('appID:')
    str3 = rect.find('player.currentTime(0);')
    fileid = re.search(r'\d+',rect[str1:str2]).group()
    appid = re.search(r'\d+',rect[str2:str3]).group()
    rec = requests.get('https://playvideo.qcloud.com/getplayinfo/v2/' + appid + '/' + fileid,headers=headers)
    j = json.loads(rec.text)
    mp4list = []
    for index in range(len(j['videoInfo']['transcodeList']) - 1):
        mp4 = {}
        num = len(j['videoInfo']['transcodeList'])
        mp4['name'] = u'[' +str(j['videoInfo']['transcodeList'][num - index - 1]['height']) + u'p] - ' + j['videoInfo']['basicInfo']['name']
        mp4['thumb'] = j['coverInfo']['coverUrl']
        mp4['url'] = j['videoInfo']['transcodeList'][num - index - 1]['url']
        mp4['duration'] = j['videoInfo']['transcodeList'][num - index - 1]['duration']
        mp4list.append(mp4)
    return mp4list

def get_mp4info(rect):
    soup = BeautifulSoup(rect, 'html.parser')
    mp4info = {}
    title = soup.find('div',class_='video-play fl')
    title = title.h2.text
    mp4info['title'] = title

    year = soup.find('div',class_='sj')
    year = year.text[2:]
    mp4info['year'] = year


    updata = soup.find('div',class_='zj-con')
    up = updata.div.h3.a.text
    upinfo = updata.div.h3.span.text
    mp4info['cast'] = [(up,upinfo)]


    jianjie = soup.find('div',id='zhuanjiajianjie')
    jianjie = jianjie.text
    jianjie = jianjie.replace(u'。',u'。\n\n')
    plot = up + u' - ' + upinfo + u'\n\n'
    plot += jianjie
    mp4info['plot'] = plot



    mp4info['mediatype'] = 'video'
    return mp4info

@plugin.route('/play/<name>/<url>/')
def play(name,url):
    rect = get_mp4_request(url)
    mp4info = get_mp4info(rect)
    videos = get_mp4(rect)
    mp4info['duration'] = videos[0]['duration']
    items = [{
        'label': video['name'].encode('utf-8'),
        'path': video['url'],
        'is_playable': True,
	'thumbnail': video['thumb'],
        'icon': video['thumb'],
        'info':mp4info,
        'info_type':'video',
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
        'path': plugin.url_for('duop' , url=video['href']),
	#'thumbnail': video['thumb'],
        #'icon': video['thumb'],
    } for video in videos]

    sorted_items = items
    #sorted_items = sorted(items, key=lambda item: item['label'])
    return sorted_items

@plugin.route('/duop/<url>/')
def duop(url):
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', url)

    videos = get_duop(url)
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
