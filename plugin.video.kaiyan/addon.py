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
    return [{'name':'推荐','link':'http://baobab.kaiyanapp.com/api/v5/index/tab/allRec?page=0'},
            {'name':'周排行','link':'http://baobab.kaiyanapp.com/api/v4/rankList/videos?strategy=weekly&num=8&start='},
            {'name':'月排行','link':'http://baobab.kaiyanapp.com/api/v4/rankList/videos?strategy=monthly&num=8&start='},
            {'name':'专题','link':'http://baobab.kaiyanapp.com/api/v3/specialTopics?start=0&num=10'}]

def get_tuijian_videos(url):
    #爬视频列表的
    videos = []

    rec = requests.get(url,headers=headers)
    #print(rec.text)

    j = json.loads(rec.text)
    #标题
    #print(j['itemList'][0]['data']['header']['title'] + ' - ' + j['itemList'][0]['data']['header']['subTitle'])
    #视频数：
    #print(j['itemList'][0]['data'])
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', j['itemList'][0]['data']['itemList'][0]['data']['content']['data']['playUrl'])

    for index in range(len(j['itemList'][0]['data']['itemList'])):
        videoitem = {}
        videoitem['name'] = j['itemList'][0]['data']['itemList'][index]['data']['content']['data']['title']
        videoitem['href'] = j['itemList'][0]['data']['itemList'][index]['data']['content']['data']['playUrl']
        videoitem['thumb'] = j['itemList'][0]['data']['itemList'][index]['data']['content']['data']['cover']['feed']
        videos.append(videoitem)

        #标题
        #print(j['itemList'][0]['data']['itemList'][index]['data']['content']['data']['title'])
        #图片
        #print(j['itemList'][0]['data']['itemList'][index]['data']['content']['data']['cover']['feed'])
        #mp4
        #print(j['itemList'][0]['data']['itemList'][index]['data']['content']['data']['playUrl'])


    for index in range(len(j['itemList'])):
        if j['itemList'][index]['type'] == 'videoSmallCard' or j['itemList'][index]['type'] == 'FollowCard':
	    videoitem = {}
            videoitem['name'] = '['+j['itemList'][index]['data']['category']+'] - ' + j['itemList'][index]['data']['title']
            videoitem['href'] = j['itemList'][index]['data']['playUrl']
            videoitem['thumb'] = j['itemList'][index]['data']['cover']['feed']
            videos.append(videoitem)
            #print(j['itemList'][index]['data']['category']+'] - ' + j['itemList'][index]['data']['title'])
            
            
            #print(j['itemList'][index]['data']['cover']['feed'])
            #print(j['itemList'][index]['data']['playUrl'])
    return videos



def get_paihang_videos(url):
#爬视频列表的
    listnum = 8
    num = 0
    rank=1
    videos = []
    while listnum == 8:
  
        rec = requests.get(url + str(num*8),headers=headers)
        #print(rec.text)

        j = json.loads(rec.text)
        listnum = len(j['itemList'])
        num += 1
        for index in range(len(j['itemList'])):
            videoitem = {}
            videoitem['name'] = '['+str(rank)+ ']' + j['itemList'][index]['data']['category'] + ' - ' + j['itemList'][index]['data']['title']
            videoitem['href'] = j['itemList'][index]['data']['playUrl']
            videoitem['thumb'] = j['itemList'][index]['data']['cover']['feed']
            videoitem['genre'] = '豆瓣电影'
            videos.append(videoitem)
            rank += 1
            #标题
            #print(j['itemList'][index]['data']['category'] + ' - ' + j['itemList'][index]['data']['title'])
            #图片
            #print(j['itemList'][index]['data']['cover']['feed'])
            #mp4
            #print(j['itemList'][index]['data']['playUrl'])
    return videos






    for videoelement in videoelements:
            
        videoitem = {}
        videoitem['name'] = videoelement.find('img')['alt']
        videoitem['href'] = videoelement.find('a')['href']
        #videoitem['thumb'] = 'aaaa'
        videoitem['genre'] = '豆瓣电影'
        videos.append(videoitem)
    return videos




def get_zhuanti_videos(category):
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




@plugin.route('/play/<name>/<url>/')
def play(name,url):

        items = []
        
        item = {'label': name,'path': get_real_url(url),'is_playable': True}
        items.append(item)
        return items

@plugin.route('/category/<name>/<url>/')
def category(name,url):
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', url)
    if name == '推荐':
        #tuijian
        videos = get_tuijian_videos(url)
    else:
        if name == '周排行':
            #2
            videos = get_paihang_videos(url)
        else:
            if name == '月排行':
                #3
                videos = get_paihang_videos(url)
            else:
                #4
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
