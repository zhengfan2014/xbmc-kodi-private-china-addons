#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from xbmcswift2 import Plugin,xbmcgui,xbmcplugin
import requests
from bs4 import BeautifulSoup
import base64
import json
import urllib2
import sys
import HTMLParser
import re

plugin = Plugin()
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36'}


@plugin.cached(TTL=10)
def get_html_10min(url, head=''):
    if head == '':
        r = requests.get(url, headers=headers)
    else:
        r = requests.get(url, headers=eval(head))
    r.encoding = 'utf-8'
    r = r.text
    return r


@plugin.cached(TTL=1)
def get_html_1min(url, head=''):
    if head == '':
        r = requests.get(url, headers=headers)
    else:
        r = requests.get(url, headers=eval(head))
    r.encoding = 'utf-8'
    r = r.text
    return r


def unescape(string):
    string = urllib2.unquote(string).decode('utf8')
    quoted = HTMLParser.HTMLParser().unescape(string).encode('utf-8')
    # 转成中文
    return re.sub(r'%u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})', lambda m: unichr(int(m.group(1), 16)), quoted)


def get_categories():
    return [{'name': '热门', 'link': 'https://www.xinpianchang.com/channel/index/type-/sort-like/duration_type-0/resolution_type-/'},
            {'name': '广告', 'link': 'https://www.xinpianchang.com/channel/index/id-1/sort-pick/type-/duration_type-0/resolution_type-/'},
            {'name': '剧情短片', 'link': 'https://www.xinpianchang.com/channel/index/id-31/sort-pick/duration_type-0/resolution_type-/type-'},
            {'name': '宣传片', 'link': 'https://www.xinpianchang.com/channel/index/id-16/sort-pick/duration_type-0/resolution_type-/type-/'},
            {'name': '创意', 'link': 'https://www.xinpianchang.com/channel/index/id-76/sort-pick/duration_type-0/resolution_type-/type-'},
            {'name': '特殊摄影', 'link': 'https://www.xinpianchang.com/channel/index/id-61/sort-pick/duration_type-0/resolution_type-/type-'},
            {'name': '旅拍', 'link': 'https://www.xinpianchang.com/channel/index/id-141/sort-pick/duration_type-0/resolution_type-/type-'},
            {'name': '影视', 'link': 'https://www.xinpianchang.com/channel/index/id-81/sort-pick/duration_type-0/resolution_type-/type-'},
            {'name': '混剪', 'link': 'https://www.xinpianchang.com/channel/index/id-142/sort-pick/duration_type-0/resolution_type-/type-'},
            {'name': '器材', 'link': 'https://www.xinpianchang.com/channel/index/id-143/sort-pick/duration_type-0/resolution_type-/type-'},
            {'name': '干货教程', 'link': 'https://www.xinpianchang.com/channel/index/id-144/sort-pick/duration_type-0/resolution_type-/type-'},
            {'name': 'Vlog', 'link': 'https://www.xinpianchang.com/channel/index/id-129/sort-pick/duration_type-0/resolution_type-/type-'},
            {'name': '古风', 'link': 'https://www.xinpianchang.com/channel/index/id-145/sort-pick/duration_type-0/resolution_type-/type-'},
            {'name': '短视频', 'link': 'https://www.xinpianchang.com/channel/index/id-29/sort-pick/duration_type-0/resolution_type-/type-'},
            {'name': '纪录', 'link': 'https://www.xinpianchang.com/channel/index/id-49/sort-pick/duration_type-0/resolution_type-/type-'},
            {'name': '动画', 'link': 'https://www.xinpianchang.com/channel/index/id-69/sort-pick/duration_type-0/resolution_type-/type-'},
            {'name': '音乐', 'link': 'https://www.xinpianchang.com/channel/index/id-27/sort-pick/duration_type-0/resolution_type-/type-'},
            {'name': '极限', 'link': 'https://www.xinpianchang.com/channel/index/id-146/sort-pick/duration_type-0/resolution_type-/type-'}]


def get_mp4(url):
    #url = 'https://www.xinpianchang.com/a10696100'
    r = get_html_10min(url)
    soup = BeautifulSoup(r, 'html.parser')
    # 创作者
    user = soup.find('ul',class_="creator-list").find_all('li')
    users = []
    for i in range(len(user)):
        users.append({"name":user[i].find('span',class_="name").text.encode("utf-8"),"role":user[i].find('span',class_="roles").text.encode("utf-8"),"thumbnail":user[i].find('img')["_src"].encode("utf-8")})
    # mp4
    vid = re.search("(?<=vid = \").*?(?=\")", r).group()
    modeServerAppKey = re.search(
        "(?<=modeServerAppKey = \").*?(?=\")", r).group()
    api = 'https://mod-api.xinpianchang.com/mod/api/v2/media/' + vid + \
        '?appKey=' + modeServerAppKey + '&extend=userInfo,userStatus'
    r = get_html_10min(api)
    j = json.loads(r)
    mp4list = {}
    for index in range(len(j['data']['resource']['progressive'])):
        mp4list[j['data']['resource']['progressive'][index]['profile']
                ] = 'http' + j['data']['resource']['progressive'][index]['url'][5:]
    # 简介
    desc = soup.find('i',class_="play-counts").text.encode('utf-8') + " 播放 · " + soup.find('span',class_="like-counts").text.encode('utf-8') + " 赞 · " + soup.find('span',class_="collect-counts").text.encode('utf-8') +" 收藏\n"
    desc += soup.find('span',class_='update-time').text.encode('utf-8') +"\n"
    desc += "[COLOR red]" + soup.find('span',class_='authorize-con').text.encode('utf-8') + "[/COLOR]\n\n"
    desc += j['data']['description'].encode('utf-8')
    return {"mp4":mp4list,"user":users,"genre":j['data']['categories'],"tag":j['data']['keywords'],'desc':desc,'img':j['data']['cover']}


# 爬视频列表的
def get_videos(url, page):
    videos = []
    if(int(page) != 1):
        url += "/page-" + str(page)
    r = get_html_1min(url)
    soup = BeautifulSoup(r, 'html.parser')
    filmitem = soup.find_all('li', class_='enter-filmplay')

    for index in range(len(filmitem)):
        img = filmitem[index].find('img', class_='lazy-img')
        title = filmitem[index].find(
            'p', class_='fs_14 fw_600 c_b_3 line-hide-1')

        videoinfo = filmitem[index].find('span', class_='fw_300 icon-play-volume').text.encode(
            "utf-8") + "播放 · " + filmitem[index].find('span', class_='fw_300 c_b_9 icon-like').text.encode("utf-8") + "赞"
        userlist = filmitem[index].find('ul', class_="authors-list")
        videousers = []
        if userlist:
            # 多创作者
            userlists = userlist.find_all('li')
            for i in range(len(userlists)):
                videousers.append((userlists[i].a.div.p.text.encode("utf-8"), userlists[i].a.div.div.text.encode("utf-8")))
        user = filmitem[index].find('a', class_="user-link v-center enter-creator-space")
        if user:
            # 单个创作者
            userdesc = user.find('span', class_="role")
            if userdesc:
                videousers.append((user.find('span', class_="name").text.encode("utf-8"),userdesc.text.encode("utf-8")))
            else:
                videousers.append((user.find('span', class_="name").text.strip().encode("utf-8"),u'作者'))
        plot = filmitem[index].find('div', class_='fs_12 fw_300 c_w_f desc line-hide-3').text.encode("utf-8")
        videoitem = {}
        videoitem['name'] = title.text
        videoitem['href'] = 'https://www.xinpianchang.com/a' + \
            filmitem[index]['data-articleid']
        videoitem['thumb'] = img['_src']
        videoitem['info'] = {"plot": videoinfo + "\n\n" + plot, "castandrole": videousers,"mediatype":"video"}
        videos.append(videoitem)
    return videos


@plugin.route('/play/<name>/<url>/')
def play(name, url):
    mp4list = get_mp4(url)
    items = []
    # 创作者
    for k, i in mp4list["mp4"].items():
        item = {'label': '[' + k.encode('utf-8') + '] - ' + name,
                'path': i.encode('utf-8'),
                 'is_playable': True,
                 'thumbnail':mp4list["img"],
                 'icon':mp4list["img"],
                 "info":{"plot":mp4list["desc"],"tag":mp4list["tag"],"genre":mp4list["genre"],"mediatype":"video"}}
        items.append(item)
    return items


@plugin.route('/category/<url>/<page>/')
def category(url, page):
    videos = get_videos(url, page)

    items = [{
        'label': video['name'],
        'path': plugin.url_for('play', name=video['name'].encode('utf-8'), url=video['href']),
        'thumbnail': video['thumb'],
        'icon': video['thumb'],
        'info':video['info'],
    } for video in videos]
    nextpage = {'label': '[COLOR yellow]下一页[/COLOR]',
                'path': plugin.url_for('category', url=url, page=str(int(page)+1))}
    items.append(nextpage)
    return items


@plugin.route('/')
def index():
    categories = get_categories()
    items = [{
        'label': category['name'],
        'path': plugin.url_for('category', url=category['link'], page=1),
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
