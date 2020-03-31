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
    return [{'name':'首映厅','link':'shouying'},
            {'name':'纪录片','link':'jilu'}]

@plugin.cached(TTL=60)
def get_shouying():
    videos = []
    url = 'https://www.huanxi.com/player.shtml'
    rec = requests.get(url,headers=headers)
    rec.encoding = 'utf-8'
    cag=1
    #print(rec.text)
    soup = BeautifulSoup(rec.text, 'html.parser')
    rectext = rec.text



    filmitem = soup.find_all('div',class_='content')
    for index in range(len(filmitem)):
        img = filmitem[index].find('img')
        title = filmitem[index].find('p')
        a = filmitem[index].find('a')
        name = filmitem[index].find('p',class_='label')
        dj = filmitem[index].find('p',class_='dj')
        dbh = filmitem[index].find('p',class_='dbh')
        if dj == None:
            tag = '['+ dbh.text +']'
        else:
            tag = '[独播]['+ dbh.text.encode('utf-8') +']'
        videoitem = {}
        videoitem['name'] =   title.text + ' - ' +name.text
        videoitem['href'] = 'https://www.huanxi.com/'+a['href']
        videoitem['thumb'] = img['src']
        videos.append(videoitem)  
    return videos

@plugin.cached(TTL=60)
def get_jilu():
    videos = []
    url = 'https://www.huanxi.com/documentary.shtml'
    rec = requests.get(url,headers=headers)
    rec.encoding = 'utf-8'

    #print(rec.text)
    soup = BeautifulSoup(rec.text, 'html.parser')
    rectext = rec.text
    biaoti = soup.find_all('div',class_='titles')
    btlist = []
    for i in range(len(biaoti)):
        text = biaoti[i].find('span')
        btlist.append(text.text)
        btlist.append(text.text)

    jl = soup.find_all('div',class_='bottom')
    for i in range(len(jl)):
        #取出偶数的项目
        if (i % 2) != 0:

            a = jl[i].find_all('a')
            tag = btlist[i]
            for i in range(len(a)):
                title = a[i].find('div',class_='down')
                title = title.text
                title = title.strip()
                title = title.replace('[<div class="down">\n<div>','')
                title = title.replace('</div>\n</div>]','')
                #title = title.encode('utf-8')
                title = title.split('</div>\n<div>')
                #dialog = xbmcgui.Dialog()
                #ok = dialog.ok('错误提示', str(title))
                videoitem = {}
                videoitem['name'] = '['+tag+']'+title[0]
                videoitem['href'] = 'https://www.huanxi.com/'+a[i]['href']
                videoitem['thumb'] = a[i].img['src']
                videos.append(videoitem)  
    return videos

@plugin.cached(TTL=60)
def get_mp4(url):
    mp4list = {}
    rec = requests.get(url,headers=headers)
    #print(rec.text)
    rectext = rec.text
    j = json.loads(rectext)
    qxd = ['4k','1080p','720p','480p']
    if j['result']['tips'] != '':
        for index in range(len(j['result']['bitrate'])):
            p = j['result']['bitrate'][len(j['result']['bitrate'])-index-1]
            mp4list[qxd[index]] = j['result']['cdn_url'] + '?bitrate=' + str(p) + '&https=1'
    else:

        for index in range(len(j['result']['bitrate'])):
            p = j['result']['bitrate'][len(j['result']['bitrate'])-index-1]
            mp4list[qxd[index]] = j['result']['cdn_url'] + '?bitrate=' + str(p) + '&https=1'
    return mp4list

@plugin.cached(TTL=60)
def get_videolist(url):
    #视频片花和幕后列表
    videos = []
    devid = '0828875861381020000'
    apiurl = 'https://www.huanxi.com/apis/hxtv/play/authen?vid='
    rec = requests.get(url,headers=headers)
    rec.encoding = 'utf-8'
    rectext = rec.text

    str1 = rectext.find('tagid:')
    str2 = rectext.find('SourceID:')
    str3 = rectext.find('videoType:')
    str4 = rectext.find('GroupID:')
    str5 = rectext.find('GroupName:')
    str6 = rectext.find('title:')
    str7 = rectext.find('vtype_sub:')
    str8 = rectext.find('singImg:')
    str10 = rectext.find('<link rel="stylesheet" href="css/base.css?v=5.1.2">')
    cutjson = rectext[str1:str10]
    #print(cutjson)

    vid = rectext[str2+10:str3].strip()
    gid = rectext[str4+10:str5].strip()
    gname = rectext[str5+10:str6].strip()
    vtype = rectext[str3+10:str3+12].strip()
    img = rectext[str8:str10].strip()
    img = img.replace('}','')
    img = img.replace('</script>','').strip()
    title = rectext[str6:str7].strip()

    title = title[7:-2]
    img = img[9:-1]
    vid = vid[:-1]
    gid = gid[:-2]
    gname = gname[1:-2]


    multip = rectext.find('dramas_no_num:')
    if multip != -1:
        #多p
        str11 = rectext.find('dramas_vip_num:')
        duop = rectext[multip:str11].strip()
        duop = duop[15:-2]
        k = json.loads(duop)
        for index in range(len(k['ep_list'])):
            tag = '[VIP]'
            qqq=k['ep_list'][index]['ep_part_ispay']
            if qqq == '0':
                tag = '[baipiao]'
            videoitem = {}
            videoitem['name'] = tag+k['ep_list'][index]['ep_part_title']
            videoitem['href'] = apiurl+vid+'&vtype='+vtype+'&version=5.0&deviceId='+devid+'&platform=1&xt=1&epid='+str(k['ep_list'][index]['ep_part_id'])
            videoitem['thumb'] = k['ep_list'][index]['ep_part_pic']
            videos.append(videoitem)  
    else:
        #单p
        videoitem = {}
        videoitem['name'] = '[shikan]'+title
        videoitem['href'] = 'https://www.huanxi.com/apis/hxtv/play/authen?vid=' + vid + '&vtype=' + vtype + '&version=5.0&deviceId=' + devid + '&platform=1&xt=1'
        videoitem['thumb'] = img
        videos.append(videoitem)

    #print(vtype)
    rec = requests.get('https://www.huanxi.com/apis/hxtv/clips/getListOfGroup?tul=154&vtype=1&vid='+vid+'&group_id='+gid+'&group_name='+gname+'&platform=1&xt=0&version=5.1&deviceId=0828875861381020000',headers=headers)
    j = json.loads(rec.text)
    for index in range(len(j['result'][0]['list'])):
        videoitem = {}
        videoitem['name'] = j['result'][0]['group_name']+': '+j['result'][0]['list'][index]['title']
        videoitem['href'] = apiurl+str(j['result'][0]['list'][index]['vid'])+'&vtype=2&version=5.0&deviceId='+devid+'&platform=1&xt=1'
        videoitem['thumb'] = j['result'][0]['list'][index]['pic']
        videos.append(videoitem)  
    if len(j['result']) == 2:
        for index in range(len(j['result'][1]['list'])):
            videoitem = {}
            videoitem['name'] = j['result'][1]['group_name']+': '+j['result'][1]['list'][index]['title']
            videoitem['href'] = apiurl+str(j['result'][1]['list'][index]['vid'])+'&vtype=2&version=5.0&deviceId='+devid+'&platform=1&xt=1'
            videoitem['thumb'] = j['result'][1]['list'][index]['pic']
            videos.append(videoitem) 
    return videos


@plugin.route('/duop/<url>/')
def duop(url):
    videos = get_videolist(url)
    items = [{
        'label': video['name'],
        'path': plugin.url_for('play', name=video['name'].encode('utf-8'), url=video['href']),
	'thumbnail': video['thumb'],
        'icon': video['thumb'],
    } for video in videos]
    return items

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
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', url)
    if url == 'shouying':
        #shou
        videos = get_shouying()
    else:
        #jilu
        videos = get_jilu()
    items = [{
        'label': video['name'],
        'path': plugin.url_for('duop', url=video['href']),
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
