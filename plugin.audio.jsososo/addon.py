#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from xbmcswift2 import Plugin, xbmcgui, xbmc, xbmcaddon, xbmcplugin
#from xbmcswift2 import Actions
import requests
from bs4 import BeautifulSoup
import xbmcgui
import base64
import json
import urllib2
import sys
import HTMLParser
import re
import time

def unix_to_data(uptime,format='data'):
    if len(str(uptime)) > 10:
        uptime = str(uptime)[:-(len(str(uptime))-10)]
    uptime = float(uptime)
    time_local = time.localtime(uptime)
    if format == 'data' or format == 'zhdata' or format == 'datatime' or format == 'zhdatatime' or format == 'time' or format == 'zhtime':
        if format == 'data':
            uptime = time.strftime('%Y-%m-%d',time_local)
        if format == 'zhdata':
            uptime = time.strftime('%Y年%m月%d日',time_local)
        if format == 'datatime':
            uptime = time.strftime('%Y-%m-%d %H:%M:%S',time_local)
        if format == 'zhdatatime':
            uptime = time.strftime('%Y年%m月%d日 %H时%M分%S秒',time_local)
        if format == 'time':
            uptime = time.strftime('%H:%M:%S',time_local)
        if format == 'zhtime':
            uptime = time.strftime('%H时%M分%S秒',time_local)
    else:
        uptime = time.strftime(format,time_local)
    return uptime

#超过10000换算
def zh(num):
    if int(num) >= 100000000:
        p = round(float(num)/float(100000000), 1)
        p = str(p) + '亿'
    else:
        if int(num) >= 10000:
            p = round(float(num)/float(10000), 1)
            p = str(p) + '万'
        else:
            p = str(num)
    return p

def get_real_url(url):
    rs = requests.get(url,headers=headers,timeout=2)
    return rs.url

def unescape(string):
    string = urllib2.unquote(string).decode('utf8')
    quoted = HTMLParser.HTMLParser().unescape(string).encode('utf-8')
    #转成中文
    return re.sub(r'%u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})', lambda m: unichr(int(m.group(1), 16)), quoted)


plugin = Plugin()


headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36'}
cache = plugin.get_storage('cache')
his = plugin.get_storage('his')

#初始化api
# if 'myqq' not in cache:
#     cache['myqq'] = ''
# if 'my163' not in cache:
#     cache['my163'] = ''
# if 'my163num' not in cache:
#     cache['my163num'] = ''
# if 'myqqnum' not in cache:
#     cache['myqqnum'] = ''
# xbmcplugin.setContent(int(sys.argv[1]), 'musicvideos')

netease_api = xbmcplugin.getSetting(int(sys.argv[1]), 'neteasemusicapiurl')
qqmusic_api = xbmcplugin.getSetting(int(sys.argv[1]), 'qqmusicapiurl')
migu_api = xbmcplugin.getSetting(int(sys.argv[1]), 'miguapiurl')


@plugin.cached(TTL=1)
def get_html(url,cookie=''):
    if cookie != '':
        h = headers
        h['cookie'] = cookie
        r = requests.get(url,headers=h)
    else:
        r = requests.get(url,headers=headers)
    return r.text

########################################### 为你推荐歌单api ###########################################
def one63weinituijian():
    gedans = []
    r = get_html(netease_api + '/recommend/resource','MUSIC_U=' + xbmcplugin.getSetting(int(sys.argv[1]), 'neteasemusicu'))
    j = json.loads(r)
    if j['code'] == 200:
        glist = j['recommend']
        for index in range(len(glist)):
            desc = ''
            if glist[index]['copywriter']:
                desc += glist[index]['copywriter'].encode('utf-8')
            gd ={}
            gd['name'] = glist[index]['name']
            gd['thumb'] = glist[index]['picUrl']
            gd['url'] = 'https://music.163.com/#/playlist?id=' + str(glist[index]['id'])
            gd['info'] = {'plot':zh(glist[index]['playcount']) + ' 播放 · ' + zh(glist[index]['trackCount']) + ' 首歌\n\n' + desc}
            gd['info']['cast'] = [(glist[index]['creator']['nickname'],unix_to_data(glist[index]['createTime']) + u'创建')]
            gedans.append(gd)
        return gedans
    else:
        if j['code'] == 301:
            dialog = xbmcgui.Dialog()
            dialog.notification('请求失败','请尝试更换MUSIC_U', xbmcgui.NOTIFICATION_INFO, 5000)

def qqweinituijian():
    gedans = []
    r = get_html(qqmusic_api + '/recommend/playlist/u')
    j = json.loads(r)
    glist = j['data']['list']
    for index in range(len(glist)):
        gd ={}
        gd['name'] = glist[index]['title']
        gd['thumb'] = glist[index]['cover']
        gd['url'] = 'https://y.qq.com/n/yqq/playlist/' + str(glist[index]['content_id']) + '.html'
        gd['info'] = {'plot':zh(glist[index]['listen_num']) + ' 播放量'}
        gd['info']['cast']= [glist[index]['username']]
        gedans.append(gd)
    return gedans
########################################### 日推api ###########################################
def one63ritui():
    gedans = []
    r = get_html(netease_api + '/recommend/songs','MUSIC_U='+xbmcplugin.getSetting(int(sys.argv[1]), 'neteasemusicu'))
    j = json.loads(r)
    if j['code'] == 200:
        gedans = []
        glist = j['recommend']
        # songs = ''
        # for index in range(len(glist)):
        #     if index == 0:
        #         songs += str(glist[index]['id'])
        #     else:
        #         songs += ',' + str(glist[index]['id'])
        # #mp3 url
        # r2 = get_html(netease_api + '/song/url?id=' + songs)
        # j2 = json.loads(r2)
        # mp3urls = j2['data']
        for index in range(len(glist)):
            gd ={}
            gd['name'] = glist[index]['name']
            gd['thumb'] = glist[index]['album']['picUrl']
            # gdurl = ''
            # for i in range(len(mp3urls)):
            #     if int(mp3urls[i]['id']) == int(glist[index]['id']):
            #         gdurl = mp3urls[i]['url']
            # if gdurl == '':
            #     gd['name'] += ' - [无版权]'
            if xbmcplugin.getSetting(int(sys.argv[1]), 'httpswitch') == 'true':
                gdurl =  'http'
            else:
                gdurl = 'https'
            gdurl += '://music.163.com/song/media/outer/url?id='+str(glist[index]['id'])+'.mp3'
            gd['url'] = gdurl
            gd['info'] = {'title':glist[index]['name'],'album':glist[index]['album']['name'],'artist':glist[index]['artists'][0]['name'],'mediatype':'song'}
            #gd['url'] = j2['data'][0]['url']
            gedans.append(gd)
        return gedans
    else:
        if j['code'] == 301:
            dialog = xbmcgui.Dialog()
            dialog.notification('请求失败','请尝试更换网易云音乐的 MUSIC_U', xbmcgui.NOTIFICATION_INFO, 5000)

def qqritui():
    gedans = []
    r = get_html(qqmusic_api + '/recommend/daily',xbmcplugin.getSetting(int(sys.argv[1]), 'qqmusiccookie'))
    j = json.loads(r)
    if j['result'] == 100:
        glist = j['data']['songlist']
        songs= ''
        for index in range(len(glist)):
            if index == 0:
                songs += glist[index]['songmid']
            else:
                songs += ',' + glist[index]['songmid']
        r1 = get_html(qqmusic_api + '/song/urls?id=' + songs)
        j1 = json.loads(r1)
        mp3urls = j1['data']
        for index in range(len(glist)):
            if glist[index]['songmid'] in mp3urls:
                gd ={}
                gd['name'] = glist[index]['songname']
                gd['thumb'] = 'http://y.gtimg.cn/music/photo_new/T002R300x300M000' + glist[index]['albummid'] + '.jpg'
                gd['url'] = mp3urls[glist[index]['songmid']]
                gd['info'] = {'title':glist[index]['songname'],'album':glist[index]['albumname'],'artist':glist[index]['singer'][0]['name'],'mediatype':'song'}
                gedans.append(gd)
        return gedans
    else:
        if j['result'] == 301:
            dialog = xbmcgui.Dialog()
            dialog.notification('请求失败','请尝试更换QQ音乐的 cookie', xbmcgui.NOTIFICATION_INFO, 5000)    

########################################### 我的歌单api ###########################################
def one63gedan():
    gedans = []
    r = get_html(netease_api + '/user/playlist?uid=' + str(xbmcplugin.getSetting(int(sys.argv[1]), 'neteasemusicuid')))
    j = json.loads(r)
    glist = j['playlist']
    for index in range(len(glist)):
        desc = ''
        if glist[index]['description']:
            desc += glist[index]['description'].encode('utf-8')
        gd ={}
        gd['name'] = glist[index]['name']
        gd['thumb'] = glist[index]['coverImgUrl']
        gd['url'] = 'https://music.163.com/#/playlist?id=' + str(glist[index]['id'])
        gd['info'] = {'plot':zh(glist[index]['playCount']) + ' 播放 · ' + zh(glist[index]['trackCount']) + ' 首歌\n\n' + desc}
        gd['info']['cast'] = [(glist[index]['creator']['nickname'],unix_to_data(glist[index]['createTime']) + u'创建')]
        gedans.append(gd)
    return gedans

def qqgedan():
    gedans = []
    r = get_html(qqmusic_api + '/user/songlist?id=' + str(xbmcplugin.getSetting(int(sys.argv[1]), 'qqmusicid')))
    j = json.loads(r)
    glist = j['data']['list']
    for index in range(len(glist)):
        if int(glist[index]['tid']) > 0:
            gd ={}
            gd['name'] = glist[index]['diss_name']
            gd['thumb'] = glist[index]['diss_cover']
            gd['url'] = 'https://y.qq.com/n/yqq/playlist/' + str(glist[index]['tid']) + '.html'
            gd['info'] = {'plot':zh(glist[index]['listen_num']) + ' 播放 · ' + zh(glist[index]['song_cnt']) + ' 首歌'}
            gd['info']['cast'] = [j['data']['creator']['hostname']]
            gedans.append(gd)
    return gedans
########################################### 推荐歌单api ###########################################

def one63tuijiangedan():
    gedans = []
    r = get_html(netease_api + '/personalized')
    j = json.loads(r)
    glist = j['result']
    for index in range(len(glist)):
        gd ={}
        gd['name'] = glist[index]['name']
        gd['thumb'] = glist[index]['picUrl']
        gd['url'] = 'https://music.163.com/#/playlist?id=' + str(glist[index]['id'])
        gd['info'] = {'plot':zh(glist[index]['playCount']) + ' 播放 · ' + zh(glist[index]['trackCount']) + ' 首歌\n\n' + glist[index]['copywriter'].encode('utf-8')}
        gd['info']['cast'] = ['不知道是谁']
        gedans.append(gd)
    return gedans

def qqtuijiangedan():
    gedans = []
    r = get_html(qqmusic_api + '/recommend/playlist/')
    j = json.loads(r)
    glist = j['data']['list']
    for index in range(len(glist)):
        gd ={}
        gd['name'] = glist[index]['title']
        gd['thumb'] = glist[index]['cover_url_big']
        gd['url'] = 'https://y.qq.com/n/yqq/playlist/' + str(glist[index]['tid']) + '.html'
        gd['info'] = {'plot':zh(glist[index]['access_num']) + ' 播放量'}
        gd['info']['cast']= [glist[index]['creator_info']['nick']]
        gedans.append(gd)
    return gedans

########################################### 歌单详细信息api ###########################################
def one63playlist(id):
    gedans = []
    r = get_html(netease_api + '/playlist/detail?id=' + str(id))
    j = json.loads(r)
    glist = j['playlist']['trackIds']
    songs = ''
    for index in range(len(glist)):
        if index == 0:
            songs += str(glist[index]['id'])
        else:
            songs += ',' + str(glist[index]['id'])
    #mp3详情
    r1 = get_html(netease_api + '/song/detail?ids=' + songs)
    j1 = json.loads(r1)
    mp3detail = j1['songs']
    # #mp3 url
    # r2 = get_html(netease_api + '/song/url?id=' + songs)
    # j2 = json.loads(r2)
    # mp3urls = j2['data']
    # pDialog = xbmcgui.DialogProgress()
    # pDialog.create('网易云音乐', '努力从母猪厂的土豆服务器偷mp3中...(0%)')
    for index in range(len(mp3detail)):
        # pDialog.update(int(100*(float(index)/float(len(mp3detail)))), '努力从母猪厂的土豆服务器偷mp3中...('+str(int(100*(float(index)/float(len(mp3detail)))))+'%)')
        # #r2 = get_html(netease_api + '/song/url?id=' + str(mp3detail[index]['id']))
        # #j2 = json.loads(r2)
        gd ={}
        gd['name'] = mp3detail[index]['name']
        gd['thumb'] = mp3detail[index]['al']['picUrl']
        # gdurl = ''
        # for i in range(len(mp3urls)):
        #     if int(mp3urls[i]['id']) == int(mp3detail[index]['id']):
        #         gdurl = mp3urls[i]['url']
        # if gdurl == '':
        #     gd['name'] += ' - [无版权]'
        # gd['url'] = gdurl
        if xbmcplugin.getSetting(int(sys.argv[1]), 'httpswitch') == 'true':
            gd['url'] = 'http'
        else:
            gd['url'] = 'https'
        gd['url'] += '://music.163.com/song/media/outer/url?id=' + str(mp3detail[index]['id']) + '.mp3'
        gd['info'] = {'title':mp3detail[index]['name'],'album':mp3detail[index]['al']['name'],'artist':mp3detail[index]['ar'][0]['name'],'mediatype':'song'}
        #gd['url'] = j2['data'][0]['url']
        gedans.append(gd)
    return gedans

def qqplaylist(id):
    gedans = []
    r = get_html(qqmusic_api + '/songlist?id=' + str(id))
    j = json.loads(r)
    glist = j['data']['songlist']
    songs= ''
    for index in range(len(glist)):
        if index == 0:
            songs += glist[index]['songmid']
        else:
            songs += ',' + glist[index]['songmid']
    r1 = get_html(qqmusic_api + '/song/urls?id=' + songs)
    j1 = json.loads(r1)
    mp3urls = j1['data']
    
    for index in range(len(glist)):
        
        if glist[index]['songmid'] in mp3urls:
            gd ={}
            gd['name'] = glist[index]['songname']
            gd['thumb'] = 'http://y.gtimg.cn/music/photo_new/T002R300x300M000' + glist[index]['albummid'] + '.jpg'
            gd['url'] = mp3urls[glist[index]['songmid']]
            gd['info'] = {'title':glist[index]['songname'],'album':glist[index]['albumname'],'artist':glist[index]['singer'][0]['name'],'mediatype':'song'}
            gedans.append(gd)
    return gedans

########################################### 专辑详细信息api ###########################################
def one63album(id):
    gedans = []
    r = get_html(netease_api + '/playlist/detail?id=' + str(id))
    j = json.loads(r)
    glist = j['playlist']['trackIds']
    songs = ''
    for index in range(len(glist)):
        if index == 0:
            songs += str(glist[index]['id'])
        else:
            songs += ',' + str(glist[index]['id'])
    #mp3详情
    r1 = get_html(netease_api + '/song/detail?ids=' + songs)
    j1 = json.loads(r1)
    mp3detail = j1['songs']
    # #mp3 url
    # r2 = get_html(netease_api + '/song/url?id=' + songs)
    # j2 = json.loads(r2)
    # mp3url = j2['data']
    for index in range(len(mp3detail)):
        gd ={}
        gd['name'] = mp3detail[index]['name']
        gd['thumb'] = mp3detail[index]['al']['picUrl']
        # gd['url'] = mp3url[index]['url']
        if xbmcplugin.getSetting(int(sys.argv[1]), 'httpswitch') == 'true':
            gd['url'] = 'http'
        else:
            gd['url'] = 'https'
        gd['url'] += '://music.163.com/song/media/outer/url?id=' + str(mp3detail[index]['id']) + '.mp3'
        gedans.append(gd)
    return gedans

def qqalbum(id):
    gedans = []
    r = get_html(qqmusic_api + '/album/songs?albummid=' + str(id))
    j = json.loads(r)
    glist = j['data']['list']
    songs= ''
    for index in range(len(glist)):
        if index == 0:
            songs += glist[index]['mid']
        else:
            songs += ',' + glist[index]['mid']
    r1 = get_html(qqmusic_api + '/song/urls?id=' + songs)
    j1 = json.loads(r1)
    mp3urls = j1['data']
    
    for index in range(len(glist)):
        
        if glist[index]['mid'] in mp3urls:
            gd ={}
            gd['name'] = glist[index]['name']
            gd['thumb'] = 'http://y.gtimg.cn/music/photo_new/T002R300x300M000' + glist[index]['album']['mid'] + '.jpg'
            gd['url'] = mp3urls[glist[index]['mid']]
            gedans.append(gd)
    return gedans

########################################### 歌手热门歌曲api ###########################################
def one63singer(id):
    gedans = []
    r = get_html(netease_api + '/artists?id=' + str(id))
    j = json.loads(r)
    glist = j['hotSongs']
    for index in range(len(glist)):
        gd ={}
        gd['name'] = glist[index]['name']
        gd['thumb'] = glist[index]['al']['picUrl']
        #mp3 url
        r2 = get_html(netease_api + '/song/url?id=' + str(glist[index]['id']))
        j2 = json.loads(r2)
        gd['url'] = j2['data'][0]['url']
        gedans.append(gd)
    return gedans

def qqsinger(id):
    gedans = []
    r = get_html(qqmusic_api + '/singer/songs?num=50&singermid=' + str(id))
    j = json.loads(r)
    glist = j['data']['list']
    songs= ''
    for index in range(len(glist)):
        if index == 0:
            songs += glist[index]['mid']
        else:
            songs += ',' + glist[index]['mid']
    r1 = get_html(qqmusic_api + '/song/urls?id=' + songs)
    j1 = json.loads(r1)
    mp3urls = j1['data']
    
    for index in range(len(glist)):
        
        if glist[index]['mid'] in mp3urls:
            gd ={}
            gd['name'] = glist[index]['name']
            gd['thumb'] = 'http://y.gtimg.cn/music/photo_new/T002R300x300M000' + glist[index]['album']['mid'] + '.jpg'
            gd['url'] = mp3urls[glist[index]['mid']]
            gedans.append(gd)
    return gedans
########################################### 排行 ###########################################
def get_rank():
    items = []
    r1 = get_html(netease_api + '/toplist')
    j1 = json.loads(r1)
    one63list = j1['list']
    for index in range(len(one63list)):
        gd = {}
        gd['name'] = u'网易云音乐 · '+ one63list[index]['name']
        gd['thumb'] = one63list[index]['coverImgUrl']
        gd['url'] = '163|' + str(one63list[index]['id'])
        gd['desc'] = one63list[index]['description']
        items.append(gd)

    r2 = get_html(qqmusic_api + '/top/category')
    j2 = json.loads(r2)
    qqlist = j2['data']
    for index in range(len(qqlist)):
        listlist = qqlist[index]['list']
        for i in range(len(listlist)):
            if listlist[i]['topId'] != 201:
                gd = {}
                gd['name'] = u'QQ音乐 · '+ listlist[i]['label']
                gd['thumb'] = listlist[i]['picUrl']
                gd['url'] = 'qq|' + str(listlist[i]['topId'])
                gd['desc'] = listlist[i]['updateTime'] + u'更新'
                items.append(gd)
    return items
########################################### 排行详细 ###########################################
def one63rank(value):
    gedans = []
    # r = get_html(netease_api + '/top/list?idx=' + value)
    r = get_html(netease_api + '/related/playlist?id=' + value)
    dialog = xbmcgui.Dialog()
    dialog.textviewer('错误提示', str(value))
    j = json.loads(r)
    glist = j['playlist']['tracks']
    # songs = ''
    # for index in range(len(glist)):
    #     if index == 0:
    #         songs += str(glist[index]['id'])
    #     else:
    #         songs += ',' + str(glist[index]['id'])
    # #mp3 url
    # r2 = get_html(netease_api + '/song/url?id=' + songs)
    # j2 = json.loads(r2)
    # mp3url = j2['data']
    for index in range(len(glist)):
        gd ={}
        gd['name'] = glist[index]['name']
        gd['label'] = glist[index]['name']
        if glist[index]['alia'] != []:
            gd['label'] +=  u'(' + glist[index]['alia'][0] + u')'
        gd['thumb'] = glist[index]['al']['picUrl']
        # gd['url'] = mp3url[index]['url']
        if xbmcplugin.getSetting(int(sys.argv[1]), 'httpswitch') == 'true':
            gd['url'] = 'http'
        else:
            gd['url'] = 'https'
        gd['url'] += '://music.163.com/song/media/outer/url?id=' + str(glist[index]['id']) + '.mp3'
        gedans.append(gd)
    return gedans

def qqrank(value):
    gedans = []
    # dialog = xbmcgui.Dialog()
    # dialog.textviewer('错误提示', str(value))
    r = get_html(qqmusic_api + '/top?id=' + str(value))
    j = json.loads(r)
    glist = j['data']['list']
    songs= ''
    for index in range(len(glist)):
        if index == 0:
            songs += glist[index]['mid']
        else:
            songs += ',' + glist[index]['mid']
    r1 = get_html(qqmusic_api + '/song/urls?id=' + songs)
    j1 = json.loads(r1)
    mp3urls = j1['data']
    
    for index in range(len(glist)):
        
        if glist[index]['mid'] in mp3urls:
            gd ={}
            gd['name'] = glist[index]['title']
            gd['label'] = ''
            if int(glist[index]['rankType']) == 1:
                gd['label'] += u'[COLOR red]↑ ' + glist[index]['rankValue'] + u' '*(3-len(str(glist[index]['rankValue']))) +  u'[/COLOR]'
            if int(glist[index]['rankType']) == 2:
                gd['label'] += u'[COLOR green]↓ ' + glist[index]['rankValue'] + u' '*(3-len(str(glist[index]['rankValue']))) + u'[/COLOR]'
            if int(glist[index]['rankType']) == 3:
                gd['label'] += u'= ' + glist[index]['rankValue'] + u' '*(3-len(str(glist[index]['rankValue'])))
            if int(glist[index]['rankType']) == 4:
                gd['label'] += u'[COLOR red]NEW[/COLOR]'
            if int(glist[index]['rankType']) == 6:
                gd['label'] += u'[COLOR red]↑ ' + glist[index]['rankValue'] + u'[/COLOR]' + u' '*(5-len(str(glist[index]['rankValue'])))
            gd['label'] += u' ' +  glist[index]['title']
            gd['thumb'] = 'http://y.gtimg.cn/music/photo_new/T002R300x300M000' + glist[index]['albumMid'] + '.jpg'
            gd['url'] = mp3urls[glist[index]['mid']]
            gedans.append(gd)
    return gedans
########################################### mv ###########################################
def one63mvlist(page):
    items = []
    r = get_html(netease_api + '/mv/all?limit=50&offset=' + str( ( int(page)-1 ) *50 ) )
    j = json.loads(r)
    one63list = j['data']
    for index in range(len(one63list)):
        gd = {}
        gd['name'] = one63list[index]['name']
        gd['thumb'] = one63list[index]['cover']
        gd['url'] = 'https://music.163.com/#/mv?id=' +str(one63list[index]['id'])
        items.append(gd)
    return items

def qqmvlist(page):
    items = []
    r = get_html(qqmusic_api + '/mv/list?pageSize=50&pageNo=' + str(page))
    j = json.loads(r)
    listlist = j['data']['list']
    for i in range(len(listlist)):
        gd = {}
        gd['name'] = listlist[i]['title']
        gd['thumb'] = listlist[i]['picurl']
        gd['url'] = 'https://y.qq.com/n/yqq/mv/v/'+listlist[i]['vid']+'.html'
        items.append(gd)
    return items

def one63playmv(vid):
    r = get_html(netease_api + '/mv/url?id=' + str(vid))
    j = json.loads(r)
    mp4 = j['data']['url']
    return mp4

def qqplaymv(vid):
    r = get_html(qqmusic_api + '/mv/url?id=' + str(vid))
    j = json.loads(r)
    mp4 = j['data'][vid][len( j['data'][vid])-1]
    return mp4

def one63mvinfo(vid):
    vdict = {}
    r = get_html(netease_api + '/mv/detail?mvid=' + str(vid))
    j = json.loads(r)
    i = j['data']
    vdict['title'] = i['name']
    vdict['thumb'] = i['cover']
    vdict['duration'] = int(str(i['duration'])[:-3])
    vdict['plot'] = zh(i['playCount']) + '播放 · ' + zh(i['likeCount']) + '赞 · ' + zh(i['commentCount']) + '评论'
    if i['desc']:
        vdict['plot'] += '\n\n' + i['desc'].encode('utf-8')
    vdict['aired'] = i['publishTime']

    cast = []
    for index in range(len(i['artists'])):
        cast.append(i['artists'][index]['name'])
    vdict['cast'] = cast
    return vdict

def qqmvinfo(vid):
    vdict = {}
    r = get_html(qqmusic_api + '/mv?id=' + str(vid))
    j = json.loads(r)
    i = j['data']['info']
    vdict['title'] = i['name']
    vdict['thumb'] = i['cover_pic']
    vdict['duration'] = i['duration']
    vdict['plot'] = zh(i['playcnt']) + '播放'
    if i['desc']:
        vdict['plot'] = i['desc']
    vdict['aired'] = unix_to_data(i['pubdate'])

    cast = []
    for index in range(len(i['singers'])):
        cast.append(i['singers'][index]['name'])
    vdict['cast'] = cast
    return vdict
########################################### 搜索 ###########################################
def one63search(keyword,type,page):
    gedans = []
    r = get_html(netease_api + '/search?keywords=' + keyword + '&offset='+str((int(page)-1)*30)+'&type='+type)
    j = json.loads(r)
    glist = j['result']
    #单曲
    if type == '1':
        if 'songs' in glist:
            glist = glist['songs']
            songs= ''
            for index in range(len(glist)):
                if index == 0:
                    songs += str(glist[index]['id'])
                else:
                    songs += ',' + str(glist[index]['id'])
            #mp3详情
            r2 = get_html(netease_api + '/song/detail?ids=' + songs)
            j2 = json.loads(r2)
            mp3detail = j2['songs']
    
            for index in range(len(glist)):
                gd ={}
                gd['name'] = mp3detail[index]['name']
                gd['thumb'] = mp3detail[index]['al']['picUrl']
                #mp3url
                r1 = get_html(netease_api + '/song/url?id=' + str(mp3detail[index]['id']))
                j1 = json.loads(r1)
                gdurl = j1['data'][0]['url']
                gd['url'] = gdurl
                #gd['url'] = mp3urls[str(mp3detail[index]['id'])]
                gd['info'] = {'title':mp3detail[index]['name'],'album':mp3detail[index]['al']['name'],'artist':mp3detail[index]['ar'][0]['name']}
                gedans.append(gd)
        else:
            dialog = xbmcgui.Dialog()
            dialog.notification('提示', '搜索结果为空', xbmcgui.NOTIFICATION_INFO, 5000)
    #歌单
    if type == '1000':
        if 'playlists' in glist:
            glist = glist['playlists']
            for index in range(len(glist)):
                gd ={}
                gd['name'] = glist[index]['name']
                gd['thumb'] = glist[index]['coverImgUrl']
                gd['url'] = 'https://music.163.com/#/playlist?id=' + str(glist[index]['id'])
                ginfo =  {'title':glist[index]['name'],'cast':[(glist[index]['creator']['nickname'],u'创建者')],'plot':zh(glist[index]['playCount']).decode('utf-8') + u'播放 · ' + zh(glist[index]['trackCount']).decode('utf-8') + u'首歌 \n\n'}
                if glist[index]['description']:
                    ginfo['plot'] += glist[index]['description']
                gd['info'] = ginfo
                gedans.append(gd)
        else:
            dialog = xbmcgui.Dialog()
            dialog.notification('提示', '搜索结果为空', xbmcgui.NOTIFICATION_INFO, 5000)
    #专辑
    if type == '10':
        if 'albums' in glist:
            glist = glist['albums']
            for index in range(len(glist)):
                gd ={}
                gd['name'] = glist[index]['name']
                gd['thumb'] = glist[index]['blurPicUrl']
                gd['url'] = 'https://music.163.com/#/album?id=' + str(glist[index]['id'])
                gd['info'] = {'title':glist[index]['name'],'album':glist[index]['name'],'artist':glist[index]['artists'][0]['name']}
                gedans.append(gd)
        else:
            dialog = xbmcgui.Dialog()
            dialog.notification('提示', '搜索结果为空', xbmcgui.NOTIFICATION_INFO, 5000)
    #歌手
    if type == '100':
        if 'artists' in glist:
            glist = glist['artists']
            for index in range(len(glist)):
                gd ={}
                gd['name'] = glist[index]['name']
                gd['thumb'] = glist[index]['picUrl']
                gd['url'] = 'https://music.163.com/#/artist?id=' + str(glist[index]['id'])
                gd['info'] = {'title':glist[index]['name'],'artist':glist[index]['name']}
                gedans.append(gd)
        else:
            dialog = xbmcgui.Dialog()
            dialog.notification('提示', '搜索结果为空', xbmcgui.NOTIFICATION_INFO, 5000)
    #MV
    if type == '1004':
        if 'mvs' in glist:
            glist = glist['mvs']
            for index in range(len(glist)):
                gd ={}
                gd['name'] = glist[index]['name']
                gd['thumb'] = glist[index]['cover']
                gd['url'] = 'https://music.163.com/#/mv?id=' + str(glist[index]['id'])
                gd['info'] = {'title':glist[index]['name'],'duration':int(glist[index]['duration'])/1000,'cast':[glist[index]['artistName']]}
                gedans.append(gd)
        else:
            dialog = xbmcgui.Dialog()
            dialog.notification('提示', '搜索结果为空', xbmcgui.NOTIFICATION_INFO, 5000)
    #视频
    if type == '1014':
        if 'videos' in glist:
            glist = glist['videos']
            for index in range(len(glist)):
                gd ={}
                gd['name'] = glist[index]['title']
                gd['thumb'] = glist[index]['coverUrl']
                gd['url'] = 'https://music.163.com/#/video?id=' + str(glist[index]['vid'])
                gd['info'] = {'title':glist[index]['title'],'duration':int(glist[index]['durationms'])/1000,'cast':[glist[index]['creator'][0]['userName']]}
                gedans.append(gd)
        else:
            dialog = xbmcgui.Dialog()
            dialog.notification('提示', '搜索结果为空', xbmcgui.NOTIFICATION_INFO, 5000)
    return gedans

def qqsearch(keyword,type,page):
    gedans = []
    r = get_html(qqmusic_api + '/search?key=' + keyword + '&pageSize=30&pageNo='+str(page)+'&t='+type)
    j = json.loads(r)
    glist = j['data']['list']
    #单曲
    if type == '0':
        songs= ''
        for index in range(len(glist)):
            if index == 0:
                songs += glist[index]['songmid']
            else:
                songs += ',' + glist[index]['songmid']
        r1 = get_html(qqmusic_api + '/song/urls?id=' + songs)
        j1 = json.loads(r1)
        mp3urls = j1['data']
    
        for index in range(len(glist)):
        
            if glist[index]['songmid'] in mp3urls:
                gd ={}
                gd['name'] = glist[index]['songname']
                gd['thumb'] = 'http://y.gtimg.cn/music/photo_new/T002R300x300M000' + glist[index]['albummid'] + '.jpg'
                gd['url'] = mp3urls[glist[index]['songmid']]
                gd['info'] = {'title':glist[index]['songname'],'album':glist[index]['albumname'],'artist':glist[index]['singer'][0]['name']}
                gedans.append(gd)
    #歌单
    if type == '2':
        for index in range(len(glist)):
            gd ={}
            gd['name'] = unescape(glist[index]['dissname'].encode('utf-8')).decode('utf-8')
            gd['thumb'] = glist[index]['imgurl']
            gd['url'] = 'https://y.qq.com/n/yqq/playlist/' + str(glist[index]['dissid']) + '.html'
            gd['info'] = {'title':unescape(glist[index]['dissname'].encode('utf-8')).decode('utf-8'),'cast':[glist[index]['creator']['name'],u'创建者'],'plot':zh(glist[index]['listennum']).decode('utf-8') + u' 播放 \n\n' + unescape(glist[index]['introduction'].encode('utf-8')).decode('utf-8')}
            gedans.append(gd)
    #专辑
    if type == '8':
        for index in range(len(glist)):
            gd ={}
            gd['name'] = glist[index]['albumName']
            gd['thumb'] = glist[index]['albumPic']
            gd['url'] = 'https://y.qq.com/n/yqq/album/' + str(glist[index]['albumMID']) + '.html'
            gd['info'] = {'title':glist[index]['albumName'],'album':glist[index]['albumName'],'artist':glist[index]['singerName']}
            gedans.append(gd)
    #歌手
    if type == '9':
        for index in range(len(glist)):
            gd ={}
            gd['name'] = glist[index]['singerName']
            gd['thumb'] = glist[index]['singerPic']
            gd['url'] = 'https://y.qq.com/n/yqq/singer/' + str(glist[index]['singerMID']) + '.html'
            gd['info'] = {'title':glist[index]['singerName'],'artist':glist[index]['singerName']}
            gedans.append(gd)
    #MV
    if type == '12':
        for index in range(len(glist)):
            gd ={}
            gd['name'] = glist[index]['mv_name']
            gd['thumb'] = glist[index]['mv_pic_url']
            gd['url'] = 'https://y.qq.com/n/yqq/mv/v/' + str(glist[index]['v_id']) + '.html'
            gd['info'] = {'title':glist[index]['mv_name'],'duration':glist[index]['duration']}
            gedans.append(gd)
    return gedans
########################################### 网易云视频 ###########################################
def one63playvideo(vid):
    r = get_html(netease_api + '/video/url?id=' + str(vid))
    j = json.loads(r)
    mp4 = j['urls'][0]['url']
    return mp4

def one63videoinfo(vid):
    vdict = {}
    r = get_html(netease_api + '/video/detail?id=' + str(vid))
    j = json.loads(r)
    i = j['data']
    vdict['title'] = i['title']
    vdict['thumb'] = i['coverUrl']
    vdict['duration'] = int(i['durationms']/1000)
    vdict['plot'] = zh(i['playTime']) + '播放 · ' + zh(i['praisedCount']) + '赞 · ' + zh(i['commentCount']) + '评论'
    if i['description']:
        vdict['plot'] += '\n\n' + i['description'].encode('utf-8')
    vdict['aired'] = unix_to_data(i['publishTime'])
    genre = []
    for index in range(len(i['videoGroup'])):
        genre.append(i['videoGroup'][index]['name'])

    vdict['cast'] = [(i['creator']['nickname'],'视频作者')]
    vdict['genre'] = genre
    vdict['tag'] = genre
    return vdict


@plugin.route('/')
def index():
    items = []
    items.append({
        'label': '推荐',
        'path': plugin.url_for('tuijian'),
    })
    items.append({
        'label': '排行',
        'path': plugin.url_for('rank'),
    })
    items.append({
        'label': 'MV',
        'path': plugin.url_for('mv'),
    })
    items.append({
        'label': '搜索',
        'path': plugin.url_for('so'),
    })
    items.append({
        'label': '歌单',
        'path': plugin.url_for('gedang'),
    })
    items.append({
        'label': '日推',
        'path': plugin.url_for('ritui'),
    })
    # items.append({
    #     'label': '设置',
    #     'path': plugin.url_for('setting'),
    # })
    return items

@plugin.route('/tuijian/')
def tuijian():
    items = []
    items.append({
        'label': '网易云 · 热门推荐歌单',
        'path': plugin.url_for('get_tuijian',mode='163'),
    })
    items.append({
        'label': 'QQ音乐 · 热门推荐歌单',
        'path': plugin.url_for('get_tuijian',mode='qq'),
    })
    return items

@plugin.route('/ritui/')
def ritui():
    if xbmcplugin.getSetting(int(sys.argv[1]), 'neteasemusiccookieswitch') == 'true' or xbmcplugin.getSetting(int(sys.argv[1]), 'qqmusiccookieswitch') == 'true':
        items = []
        if xbmcplugin.getSetting(int(sys.argv[1]), 'neteasemusicu') != '' and xbmcplugin.getSetting(int(sys.argv[1]), 'neteasemusiccookieswitch') == 'true':
            items.append({
                'label': '网易云 · 私人推荐',
                'path': plugin.url_for('get_ritui',mode='163'),
            })
        if xbmcplugin.getSetting(int(sys.argv[1]), 'qqmusiccookie') != '' and xbmcplugin.getSetting(int(sys.argv[1]), 'qqmusiccookieswitch') == 'true':
            items.append({
                'label': 'QQ音乐 · 私人推荐',
                'path': plugin.url_for('get_ritui',mode='qq'),
            })
        
        return items
    else:
        dialog = xbmcgui.Dialog()
        dialog.notification('该功能未解锁','请先启用QQ音乐或者网易云的cookie功能', xbmcgui.NOTIFICATION_INFO, 5000)

@plugin.route('/mv/')
def mv():
    items = []
    items.append({
        'label': '网易云 · MV',
        'path': plugin.url_for('get_mv',mode='163',page=1),
    })
    items.append({
        'label': 'QQ音乐 · MV',
        'path': plugin.url_for('get_mv',mode='qq',page=1),
    })
    return items

@plugin.route('/so/')
def so():
    items = []
    items.append({
        'label': '网易云 · 单曲搜索',
        'path': plugin.url_for('history',name='搜索 网易云 · 单曲',url='search',mode='163',type='1')
    })
    items.append({
        'label': 'QQ音乐 · 单曲搜索',
        'path': plugin.url_for('history',name='搜索 QQ音乐 · 单曲',url='search',mode='qq',type='0')
    })
    items.append({
        'label': '网易云 · 专辑搜索',
        'path': plugin.url_for('history',name='搜索 网易云 · 专辑',url='search',mode='163',type='10')
    })
    items.append({
        'label': 'QQ音乐 · 专辑搜索',
        'path': plugin.url_for('history',name='搜索 QQ音乐 · 专辑',url='search',mode='qq',type='8')
    })
    items.append({
        'label': '网易云 · 歌手搜索',
        'path': plugin.url_for('history',name='搜索 网易云 · 歌手',url='search',mode='163',type='100')
    })
    items.append({
        'label': 'QQ音乐 · 歌手搜索',
        'path': plugin.url_for('history',name='搜索 QQ音乐 · 歌手',url='search',mode='qq',type='9')
    })
    items.append({
        'label': '网易云 · 歌单搜索',
        'path': plugin.url_for('history',name='搜索 网易云 · 歌单',url='search',mode='163',type='1000')
    })
    items.append({
        'label': 'QQ音乐 · 歌单搜索',
        'path': plugin.url_for('history',name='搜索 QQ音乐 · 歌单',url='search',mode='qq',type='2')
    })
    items.append({
        'label': '网易云 · MV搜索',
        'path': plugin.url_for('history',name='搜索 网易云 · MV',url='search',mode='163',type='1004')
    })
    items.append({
        'label': 'QQ音乐 · MV搜索',
        'path': plugin.url_for('history',name='搜索 QQ音乐 · MV',url='search',mode='qq',type='12')
    })
    # items.append({
    #     'label': '网易云 · 电台搜索',
    #     'path':  plugin.url_for('history',name='搜索 网易云 · 电台',url='search',mode='163',type='1009')
    # })
    items.append({
        'label': '网易云 · 视频搜索',
        'path':  plugin.url_for('history',name='搜索 网易云 · 视频',url='search',mode='163',type='1014')
    })
    # items.append({
    #     'label': '复制粘贴歌单url解析歌单(支持网易云和QQ音乐)',
    #     'path': plugin.url_for('get_mv',mode='163',page=1),
    # })
    # items.append({
    #     'label': '复制粘贴MV url解析mv(支持网易云和QQ音乐)',
    #     'path': plugin.url_for('get_mv',mode='163',page=1),
    # })
    return items

@plugin.route('/gedang/')
def gedang():
    if xbmcplugin.getSetting(int(sys.argv[1]), 'neteasemusiccookieswitch') == 'true' or xbmcplugin.getSetting(int(sys.argv[1]), 'qqmusiccookieswitch') == 'true':
        items = []
        if xbmcplugin.getSetting(int(sys.argv[1]), 'neteasemusicuid') != '' and xbmcplugin.getSetting(int(sys.argv[1]), 'neteasemusiccookieswitch') == 'true':
            items.append({
                'label': '网易云 · 我的歌单',
                'path': plugin.url_for('get_gedang',mode='163'),
            })
        if xbmcplugin.getSetting(int(sys.argv[1]), 'qqmusicid') != '' and xbmcplugin.getSetting(int(sys.argv[1]), 'qqmusiccookieswitch') == 'true':
            items.append({
                'label': 'QQ音乐 · 我的歌单',
                'path': plugin.url_for('get_gedang',mode='qq'),
            })
        return items
    else:
        dialog = xbmcgui.Dialog()
        dialog.notification('该功能未解锁','请先启用QQ音乐或者网易云的cookie功能', xbmcgui.NOTIFICATION_INFO, 5000)

@plugin.route('/rank/')
def rank():
    gdlist = get_rank()
    items = [{
        'label': video['name'],
        'path': plugin.url_for('ranklist',value=video['url'].encode('utf-8')),
	'thumbnail': video['thumb'],
        'icon': video['thumb'],
        'info':{'plot':video['desc'],'mediatype':'video'},
        'info_type':'video',
    } for video in gdlist]
    return items

@plugin.route('/ranklist/<value>/')
def ranklist(value):
    # 通过传递 qq|排行榜id 或 163|排行榜id 的value值 来区分不同的排行榜
    value = value.split("|")
    if value[0] == '163':
        gdlist = one63playlist(value[1])
    if value[0] == 'qq':
        gdlist = qqrank(value[1])
    
    items = []
    for video in gdlist:
        try:
            label = video['label']
        except:
            label = video['name']
        items.append({
        'label': label,
        'path': video['url'],
	'thumbnail': video['thumb'],
        'icon': video['thumb'],
        'is_playable': True,
        'info':{'title':video['name'],'mediatype':'music'},
        'info_type':'music',
    } )
    return items

@plugin.route('/get_mv/<mode>/<page>/')
def get_mv(mode,page):
    if mode == '163':
        gdlist = one63mvlist(int(page))
    else:
        gdlist = qqmvlist(int(page))
        
    items = [{
        'label': video['name'],
        'path': plugin.url_for('playmv',url=video['url']),
	'thumbnail': video['thumb'],
        'icon': video['thumb'],
    } for video in gdlist]
    if len(gdlist) == 50:
        items.append({
            'label': '下一页',
            'path': plugin.url_for('get_mv',mode=mode,page=(int(page)+1)),
        })
    return items

@plugin.route('/get_tuijian/<mode>/')
def get_tuijian(mode):
    items = []
    if mode == '163':
        gdlist = one63tuijiangedan()
    else:
        gdlist = qqtuijiangedan()
    for video in gdlist:
        info = video['info']
        info['mediatype'] = 'video'
        items.append({
            'label': video['name'],
            'path': plugin.url_for('playlist',url=video['url']),
	    'thumbnail': video['thumb'],
            'icon': video['thumb'],
            'info':info,
            'info_type':'video',
        })
    return items

@plugin.route('/get_ritui/<mode>/')
def get_ritui(mode):
    items = []
    if mode == '163':
        items.append({
            'label':'每日推荐',
            'thumbnail':'https://iph.href.lu/200x200?text='+time.strftime("%d", time.localtime()) +'&fg=FFFFFF&bg=FF0000',
            'icon':'https://iph.href.lu/200x200?text='+time.strftime("%d", time.localtime()) +'&fg=FFFFFF&bg=FF0000',
            'path': plugin.url_for('rituilist',mode='163'),
        })
        gdlist = one63weinituijian()
    else:
        items.append({
            'label':'今日私享',
            'thumbnail':'http://y.qq.com/m/resource/calendar/'+time.strftime("%m%d", time.localtime()) +'_300.jpg',
            'icon':'http://y.qq.com/m/resource/calendar/'+time.strftime("%m%d", time.localtime()) +'_300.jpg',
            'path': plugin.url_for('rituilist',mode='qq'),
        })
        gdlist = qqweinituijian()
    for video in gdlist:
        info = video['info']
        info['mediatype'] = 'video'
        items.append({
            'label': video['name'],
            'path': plugin.url_for('playlist',url=video['url']),
	    'thumbnail': video['thumb'],
            'icon': video['thumb'],
            'info':info,
            'info_type':'video',
            'context_menu':[('Theater Showtimes', 'RunScript(special://home/scripts/showtimes/default.py,Iron Man)')]
        })
    return items

@plugin.route('/rituilist/<mode>/')
def rituilist(mode):
    
    items = []
    if mode == '163':
        gdlist = one63ritui()
    else:
        gdlist = qqritui()
    items = [{
        'label': video['name'],
        'path': video['url'],
	'thumbnail': video['thumb'],
        'icon': video['thumb'],
        'is_playable': True,
        'info':video['info'],
        'info_type':'music',
    } for video in gdlist]
    return items

@plugin.route('/get_gedang/<mode>/')
def get_gedang(mode):
    items = []
    if mode == '163':
        gdlist = one63gedan()
    else:
        gdlist = qqgedan()
        
    for video in gdlist:
        info = video['info']
        info['mediatype'] = 'video'
        items.append({
            'label': video['name'],
            'path': plugin.url_for('playlist',url=video['url']),
	    'thumbnail': video['thumb'],
            'icon': video['thumb'],
            'info':info,
            'info_type':'video',
        })
    return items

@plugin.route('/playlist/<url>/')
def playlist(url):
    items = []
    if 'playlist' in url:
        dialog = xbmcgui.Dialog()
        if '163.com' in url:
            #网易云
            if re.search('(?<=playlist\?id=)\d+',url):
                pid = re.search('(?<=playlist\?id=)\d+',url).group()
                gdlist = one63playlist(pid)
                dialog.notification('提取网易云音乐歌单成功','歌单号:'+str(pid), xbmcgui.NOTIFICATION_INFO, 5000)
        else:
            if 'qq.com' in url:
                #qq音乐
                if re.search('(?<=playlist/)\d+',url):
                    pid = re.search('(?<=playlist/)\d+',url).group()
                    gdlist = qqplaylist(pid)
                    dialog.notification('提取QQ音乐歌单成功','歌单号:'+str(pid), xbmcgui.NOTIFICATION_INFO, 5000)
    else:
        #非法url
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('错误提示', '无法识别的歌单url')
    items = [{
        'label': video['name'],
        'path': video['url'],
	'thumbnail': video['thumb'],
        'icon': video['thumb'],
        'is_playable': True,
        'info':video['info'],
        'info_type':'music',
    } for video in gdlist]
    return items

@plugin.route('/playmv/<url>/')
def playmv(url):
    items = []
    # dialog = xbmcgui.Dialog()
    # ok = dialog.ok('错误提示', str(url))
    if 'mv' in url:
        if '163.com' in url:
            #网易云
            if re.search('(?<=mv\?id=)\d+',url):
                vid = re.search('(?<=mv\?id=)\d+',url).group()
                mp4url = one63playmv(vid)
                mp4info = one63mvinfo(vid)
        else:
            if 'qq.com' in url:
                #qq音乐
                if re.search('(?<=mv/v/)[a-zA-Z0-9]+',url):
                    vid = re.search('(?<=mv/v/)[a-zA-Z0-9]+',url).group()
                    mp4url = qqplaymv(vid)
                    mp4info = qqmvinfo(vid)
        #dialog = xbmcgui.Dialog()
        #ok = dialog.ok('错误提示', vid)
        mp4info['mediatype'] = 'video'
        items.append({
            'label': mp4info['title'],
            'path': mp4url,
	    'thumbnail': mp4info['thumb'],
            'icon': mp4info['thumb'],
            'is_playable': True,
            'info':mp4info,
            'info_type':'video',
        })
    else:
        #非法url
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('错误提示', '无法识别的MVurl')
    return items

@plugin.route('/playvideo/<url>/')
def playvideo(url):
    items = []
    # dialog = xbmcgui.Dialog()
    # ok = dialog.ok('错误提示', str(url))
    if 'video' in url and '163.com' in url:
        #网易云
        if re.search('(?<=video\?id=)[a-zA-Z0-9]+',url):
            vid = re.search('(?<=video\?id=)[a-zA-Z0-9]+',url).group()
            mp4url = one63playvideo(vid)
            mp4info = one63videoinfo(vid)
        
        #dialog = xbmcgui.Dialog()
        #ok = dialog.ok('错误提示', vid)
        mp4info['mediatype'] = 'video'
        items.append({
            'label': mp4info['title'],
            'path': mp4url,
	    'thumbnail': mp4info['thumb'],
            'icon': mp4info['thumb'],
            'is_playable': True,
            'info':mp4info,
            'info_type':'video',
        })
    else:
        #非法url
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('错误提示', '无法识别的视频url')
    return items

@plugin.route('/playalbum/<url>/')
def playalbum(url):
    items = []
    if 'album' in url:
        if '163.com' in url:
            #网易云
            if re.search('(?<=album\?id=)\d+',url):
                pid = re.search('(?<=album\?id=)\d+',url).group()
                gdlist = one63album(pid)
        else:
            if 'qq.com' in url:
                #qq音乐
                if re.search('(?<=album/)[a-zA-Z0-9]+',url):
                    pid = re.search('(?<=album/)[a-zA-Z0-9]+',url).group()
                    gdlist = qqalbum(pid)
        # dialog = xbmcgui.Dialog()
        # ok = dialog.ok('错误提示', pid)
    else:
        #非法url
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('错误提示', '无法识别的专辑url')
    items = [{
        'label': video['name'],
        'path': video['url'],
	'thumbnail': video['thumb'],
        'icon': video['thumb'],
        'is_playable': True,
        'info':{'title':video['name'],'mediatype':'album'},
        'info_type':'music',
    } for video in gdlist]
    return items

@plugin.route('/playsinger/<url>/')
def playsinger(url):
    items = []
    if 'artist' in url or 'singer' in url:
        if '163.com' in url:
            #网易云
            if re.search('(?<=artist\?id=)\d+',url):
                pid = re.search('(?<=artist\?id=)\d+',url).group()
                gdlist = one63singer(pid)
        else:
            if 'qq.com' in url:
                #qq音乐
                if re.search('(?<=singer/)[a-zA-Z0-9]+',url):
                    pid = re.search('(?<=singer/)[a-zA-Z0-9]+',url).group()
                    gdlist = qqsinger(pid)
        # dialog = xbmcgui.Dialog()
        # ok = dialog.ok('错误提示', pid)
    else:
        #非法url
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('错误提示', '无法识别的歌手url')
    items = [{
        'label': video['name'],
        'path': video['url'],
	'thumbnail': video['thumb'],
        'icon': video['thumb'],
        'is_playable': True,
        'info':{'title':video['name'],'mediatype':'album'},
        'info_type':'music',
    } for video in gdlist]
    return items

@plugin.route('/labels/<label>/')
def show_label(label):
    # 写抓取视频类表的方法
    #
    items = [
        {'label': label},
    ]
    return items

# @plugin.route('/setting')
# def setting():
#     items = []
#     items.append({
#         'label': u'设置网易云音乐API (API:'+netease_api +')',
#         'path': plugin.url_for('input',key='one63api',value='请输入网易云音乐API地址：'),
#     })
#     items.append({
#         'label': u'设置QQ音乐API (API:'+qqmusic_api +')',
#         'path': plugin.url_for('input',key='qqapi',value='请输入QQ音乐API地址：'),
#     })
#     # items.append({
#     #     'label': u'设置咪咕音乐API (API:'+cache['miguapi'] +')',
#     #     'path': plugin.url_for('input',key='miguapi',value='请输入咪咕音乐API地址：'),
#     # })
#     if cache['my163num'] == '':
#         items.append({
#             'label': u'设置网易云uid - 解锁基础功能(获取公开歌单，喜欢的歌等)',
#             'path': plugin.url_for('input',key='my163num',value='请输入网易云uid的值：'),
#         })
#     else:
#         items.append({
#             'label': u'设置网易云uid (uid:'+cache['my163num'] +')',
#             'path': plugin.url_for('input',key='my163num',value='请输入网易云uid的值：'),
#         })
#     if cache['myqqnum'] == '':
#         items.append({
#             'label': u'设置QQ号 - 解锁基础功能(获取公开歌单，喜欢的歌等)',
#             'path': plugin.url_for('input',key='myqqnum',value='请输入QQ号：'),
#         })
#     else:
#         items.append({
#             'label': u'设置QQ号 (QQ号：'+ cache['myqqnum'] +')',
#             'path': plugin.url_for('input',key='myqqnum',value='请输入QQ号：'),
#         })
#     if cache['my163'] == '':
#         items.append({
#             'label': u'设置网易云MUSIC_U - 解锁高级功能(专属日推)',
#             'path': plugin.url_for('input',key='my163',value='请输入网易云MUSIC_U的值：'),
#         })
#     else:
#         items.append({
#             'label': u'设置网易云MUSIC_U (MUSIC_U:'+cache['my163'] +')',
#             'path': plugin.url_for('input',key='my163',value='请输入网易云MUSIC_U的值：'),
#         })
#     if cache['myqq'] == '':
#         items.append({
#             'label': u'设置QQ cookie - 解锁高级功能(专属日推)',
#             'path': plugin.url_for('input',key='myqq',value='请输入QQ cookie：'),
#         })
#     else:
#         items.append({
#             'label': u'设置QQ cookie (QQ cookies：'+ cache['myqq'] +')',
#             'path': plugin.url_for('input',key='myqq',value='请输入QQ cookie：'),
#         })
#     return items

@plugin.route('/input/<key>/<value>/')
def input(key,value):
    keyboard = xbmc.Keyboard('', value)
    xbmc.sleep(1500)
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        dialog = xbmcgui.Dialog()
        ret = dialog.yesno('确认该值正确吗？', keyboard.getText())
        if ret:
            cache[key] = keyboard.getText()
            dialog = xbmcgui.Dialog()
            dialog.notification('提示','保存成功', xbmcgui.NOTIFICATION_INFO, 5000,False)


@plugin.route('/search/<value>/<page>/<type>/<mode>/')
def search(value,page,type,mode):
    if value == 'null':
        keyboard = xbmc.Keyboard('', '请输入搜索内容')
        xbmc.sleep(1500)
        keyboard.doModal()
        hi = his['search']
        if (keyboard.isConfirmed()):
            keyword = keyboard.getText()
            if keyword != '':
                hi[keyword] = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    else:
        keyword = value
    if 'keyword' in dir():
        if mode == '163':
            videos = one63search(keyword,type,page)
        else:
            videos = qqsearch(keyword,type,page)
        items = []
    
        for video in videos:
            info = video['info']
            #mv
            if type == '1004' or type == '12':
                info['mediatype'] = 'video'
                info_type = 'video'
                items.append({'label': video['name'],
                'path': plugin.url_for('playmv', url=video['url']),
            'thumbnail': video['thumb'],
                'icon': video['thumb'],
                'info': info,
                'info_type':info_type,
                })
            #歌单
            if type == '2' or type == '1000':
                info['mediatype'] = 'video'
                info_type = 'video'
                items.append({'label': video['name'],
                'path': plugin.url_for('playlist', url=video['url']),
            'thumbnail': video['thumb'],
                'icon': video['thumb'],
                'info': info,
                'info_type':info_type,
                })
            #单曲
            if type == '0' or type == '1':
                info['mediatype'] = 'song'
                info_type = 'music'
                items.append({'label': video['name'],
                'path': video['url'],
            'thumbnail': video['thumb'],
                'icon': video['thumb'],
                'info': info,
                'info_type':info_type,
                'is_playable': True,
                })
            #专辑
            if type == '8' or type == '10':
                info['mediatype'] = 'album'
                info_type = 'music'
                items.append({'label': video['name'],
                'path': plugin.url_for('playalbum', url=video['url']),
            'thumbnail': video['thumb'],
                'icon': video['thumb'],
                'info': info,
                'info_type':info_type,
                })
            #歌手
            if type == '9' or type == '100':
                info['mediatype'] = 'artist'
                info_type = 'music'
                items.append({'label': video['name'],
                'path': plugin.url_for('playsinger', url=video['url']),
            'thumbnail': video['thumb'],
                'icon': video['thumb'],
                'info': info,
                'info_type':info_type,
                })
            #视频
            if type == '1014':
                info['mediatype'] = 'video'
                info_type = 'video'
                items.append({'label': video['name'],
                'path': plugin.url_for('playvideo', url=video['url']),
            'thumbnail': video['thumb'],
                'icon': video['thumb'],
                'info': info,
                'info_type':info_type,
                })
        if len(videos) == 30:
            items.append({
                'label': '下一页',
                'path': plugin.url_for('search',value=value,page=(int(page)+1),mode=mode,type=type),
            })
        
    
        return items

def get_key (dict, value):
  return [k for k, v in dict.items() if v == value]

@plugin.route('/history/<name>/<url>/<type>/<mode>/')
def history(name,url,type,mode):
    items = []
    items.append({
        'label': '[COLOR yellow]'+ name +'[/COLOR]',
        'path': plugin.url_for(url,value='null',page=1,mode=mode,type=type),
    })
    #his[url] ={'aaa':'2019-01-23 10:00:00','bbb':'2019-01-23 09:01:00','ccc':'2019-01-23 09:00:59'}
    if url in his:
        hi = his[url]
        
    else:
        his[url] = {}
        hi = his[url]
        
    #hi = []
    if hi:
        val = list(hi.values())
        val = sorted(val,reverse=True)
        for index in range(len(val)):
            items.append({
                'label': name+ ':' +get_key(hi,val[index])[0] + ' - [查询时间：' + val[index] +']',
                'path': plugin.url_for(url,value=get_key(hi,val[index])[0],page=1,mode=mode,type=type),
            })
        items.append({
            'label': '[COLOR yellow]清除历史记录[/COLOR]',
            'path': plugin.url_for('cleanhis',url=url),
        })
    else:
        items.append({
            'label': '[COLOR yellow]历史记录为空[/COLOR]',
            'path': plugin.url_for(ok,value='历史记录为空'),
        })

    return items

@plugin.route('/ok/<value>/')
def ok(value):
    dialog = xbmcgui.Dialog()
    ok = dialog.ok('提示', value)

@plugin.route('/cleanhis/<url>/')
def cleanhis(url):
    his[url] = {}
    dialog = xbmcgui.Dialog()
    ok = dialog.ok('提示', '清理历史记录成功')

if __name__ == '__main__':
    plugin.run()
