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
    return [{'name':'编辑推荐','link':'bianji'},
            {'name':'为你推荐','link':'foryou'},
            {'name':'热门榜','link':'https://www.taptap.com/top/download'},
            {'name':'新品榜','link':'https://www.taptap.com/top/new'},
            {'name':'预约榜','link':'https://www.taptap.com/top/reserve'},
            {'name':'热卖榜','link':'https://www.taptap.com/top/sell'},
            {'name':'热玩榜','link':'https://www.taptap.com/top/played'},
            {'name':'往期推荐','link':'https://www.taptap.com/category/recommend'},
            {'name':'TapTap独家','link':'https://www.taptap.com/tag/TapTap%E7%8B%AC%E5%AE%B6'},
            {'name':'单机','link':'https://www.taptap.com/tag/%E5%8D%95%E6%9C%BA'},
            {'name':'角色扮演','link':'https://www.taptap.com/tag/%E8%A7%92%E8%89%B2%E6%89%AE%E6%BC%94'},
            {'name':'动作','link':'https://www.taptap.com/tag/%E5%8A%A8%E4%BD%9C'},
            {'name':'MOBA','link':'https://www.taptap.com/tag/moba'},
            {'name':'策略','link':'https://www.taptap.com/tag/%E7%AD%96%E7%95%A5'},
            {'name':'卡牌','link':'https://www.taptap.com/tag/%E5%8D%A1%E7%89%8C'},
            {'name':'生存','link':'https://www.taptap.com/tag/%E7%94%9F%E5%AD%98'},
            {'name':'模拟','link':'https://www.taptap.com/tag/%E6%A8%A1%E6%8B%9F'},
            {'name':'竞速','link':'https://www.taptap.com/tag/%E7%AB%9E%E9%80%9F'},
            {'name':'益智','link':'https://www.taptap.com/tag/%E7%9B%8A%E6%99%BA'},
            {'name':'二次元','link':'https://www.taptap.com/tag/%E4%BA%8C%E6%AC%A1%E5%85%83'}]

def get_videos(url):
    videos = []
    if url == 'bianji' or url == 'foryou':
        #
        if url == 'bianji':
            #bianji
            url = 'https://www.taptap.com/webapiv2/video/v1/refresh?type=editors_choice&from=1&limit=10&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC'

            rec = requests.get(url,headers=headers)

            j = json.loads(rec.text)


            for index in range(len(j['data']['list'])):
                imgurl = j['data']['list'][index]['image']['url']
                id = j['data']['list'][index]['id']
                videoitem = {}
                videoitem['name'] = j['data']['list'][index]['title']
                videoitem['href'] = 'https://taptap.com/video/' + str(id)
                videoitem['thumb'] = 'http' + imgurl[5:]
                videos.append(videoitem)  
            return videos

        else:
            #fotyou
            url = 'https://www.taptap.com/webapiv2/video/v1/refresh?type=recommend&from=0&limit=30&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC'

            rec = requests.get(url,headers=headers)

            j = json.loads(rec.text)


            for index in range(len(j['data']['list'])):
                imgurl = j['data']['list'][index]['data']['image']['url']
                id = j['data']['list'][index]['data']['id']
                videoitem = {}
                videoitem['name'] = j['data']['list'][index]['data']['title']
                videoitem['href'] = 'https://taptap.com/video/' + str(id)
                videoitem['thumb'] = 'http' + imgurl[5:]
                videos.append(videoitem)  
            return videos
    else:
        #不是排行榜就是分类列表
        if url[:27] == 'https://www.taptap.com/top/':
            rec = requests.get(url,headers=headers)
            #print(rec.text)
            soup = BeautifulSoup(rec.text, 'html.parser')
            rankitem = soup.find_all('div',class_='taptap-top-card')
            for index in range(len(rankitem)):
                data = rankitem[index].find('a',class_='card-left-image')
                img = data.find('img')
                videoitem = {}
                videoitem['name'] = str(index+1)+ ' - ' + img['alt']
                videoitem['href'] = data['href']
                videoitem['thumb'] = 'http'+img['src'][5:]
                videos.append(videoitem)  
            return videos
        else:
            #其他
            if url[:27] == 'https://www.taptap.com/app/':
                #app抓视频列表
                #dialog = xbmcgui.Dialog()
                #ok = dialog.ok('提示',url)
                rec = requests.get(url,headers=headers)
                #print(rec.text)
                soup = BeautifulSoup(rec.text, 'html.parser')
                if soup.find_all('div',class_='no-content'):

                    dialog = xbmcgui.Dialog()
                    ok = dialog.ok('提示','没有视频')
                else:

                    videoitem = soup.find_all('div',class_='video-item')


                    for index in range(len(videoitem)):
                        ss = videoitem[index]

                        img = ss.find('div',class_='video-thumb-box')
                        img = img['style']
                        cutimg = img.split("'")
                        img = cutimg[1]
                        data = ss.find('div',class_='video-content')
                        #dialog = xbmcgui.Dialog()
                        #ok = dialog.ok('提示1',)

                        videoitems = {}
                        videoitems['name'] = data.a.text
                        videoitems['href'] = data.a['href']
                        videoitems['thumb'] = 'http' + img[5:]
                        videos.append(videoitems)  

                    return videos


            else:
                if url[:27] == 'https://www.taptap.com/tag/':
                    #tag页
                    #dialog = xbmcgui.Dialog()
                    #ok = dialog.ok('类',url)
                    rec = requests.get(url,headers=headers)
                    #print(rec.text)
                    soup = BeautifulSoup(rec.text, 'html.parser')
                    appitem = soup.find_all('div',class_='taptap-app-card')
                    for index in range(len(appitem)):
                        data = appitem[index].find('a',class_='app-card-left')
                        img = data.find('img')
                        videoitems = {}
                        videoitems['name'] = img['alt']
                        videoitems['thumb'] ='http'+img['src'][5:]
                        videoitems['href'] = data['href']
                        videos.append(videoitems)  
                    return videos
                else:
                    
                    #分类
                    dialog = xbmcgui.Dialog()
                    ok = dialog.ok('分类',url)
                    rec = requests.get(url,headers=headers)
                    #print(rec.text)
                    soup = BeautifulSoup(rec.text, 'html.parser')
                    appitem = soup.find_all('div',class_='taptap-app-item swiper-slide')
                    for index in range(len(appitem)):
                        data = appitem[index].find('a',class_='app-item-image taptap-link')
                        img = data.find('img')
                        videoitems = {}
                        videoitems['name'] = img['alt']
                        videoitems['thumb'] ='http'+img['data-src'][5:]
                        videoitems['href'] = data['href']
                        videos.append(videoitems)  

                    return videos

    
 
    



@plugin.route('/play/<name>/<url>/')
def play(name,url):

    if url[:25] == 'https://taptap.com/video/' or url[:29] == 'https://www.taptap.com/video/':
        #视频url解析
        #url = 'https://www.taptap.com/video/1319335'
        rec = requests.get(url,headers=headers)
        rectext = rec.text
        
        str1 = re.search(r'{url:b[a-zA-Z]?,url_h265:',rectext).span()
        str2 = re.search(r',url_expires:[a-zA-Z]?',rectext[str1[1]:]).span()
        #print(rectext[str1+17:str2-1])
        mainm3u8 = rectext[str1[1]+1:str1[1]+str2[0]-1]
        #print(type(mainm3u8))
        mainm3u8 = mainm3u8.replace(r'\u002F','/')

        rec = requests.get(mainm3u8,headers=headers)
        rectext = rec.text


        prule = re.compile(r'NAME="\d+[p|k]\d?\d?') 
        pname = prule.findall(rectext)

        urlrule = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')   # 查找数字
        m3u8url = urlrule.findall(rectext)
        cuttext = rectext
        items = []
        for index in range(len(m3u8url)):
            item = {'label': pname[index][6:],'path':m3u8url[index],'is_playable': True}
            items.append(item)
        return items
    else:

        items = []
        item = {'label': '官方视频','path':plugin.url_for('category', url=url+'/video?type=official')}
        items.append(item)
        item = {'label': '玩家视频','path':plugin.url_for('category', url=url+'/video?type=not_official')}
        items.append(item)
        return items


@plugin.route('/category/<url>/')
def category(url):
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', url)

    videos = get_videos(url)
    items = [{
        'label': video['name'],
        'path': plugin.url_for('play', name='123' , url=video['href']),
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
