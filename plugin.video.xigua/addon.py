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
import time
t = time.time()

debug = xbmc.LOGFATAL

def get_real_url(url):
    rs = requests.get(url,headers=headers,timeout=2)
    return rs.url

def unescape(string):
    string = urllib2.unquote(string).decode('utf8')
    quoted = HTMLParser.HTMLParser().unescape(string).encode('utf-8')
    #转成中文
    return re.sub(r'%u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})', lambda m: unichr(int(m.group(1), 16)), quoted)


plugin = Plugin()

@plugin.cached(TTL=60*24)
def cook():
    r = requests.get('http://www.ixigua.com',headers=headers)
    cookies = {}
    cookies['ttwid'] = r.cookies['ttwid']
    cookies['ttwid.sig'] = r.cookies['ttwid.sig']
    cookies['xiguavideopcwebid'] = r.cookies['xiguavideopcwebid']
    cookies['xiguavideopcwebid.sig'] = r.cookies['xiguavideopcwebid.sig']
    cookies['wafid']='0aa81c31-dde3-4f40-992f-2baddd00a20e'
    return cookies

headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
cookies = cook()
#cook = plugin.get_storage('cook')

@plugin.cached(TTL=60)
def get_mp4(url):
    mp4list = {}
    rec = requests.get(url,headers=headers,cookies=cookies)
    url = rec.url
    rec = requests.get(url,headers=headers,cookies=cookies)
    rec.encoding = 'utf-8'
    rectext = rec.text
    #print(rectext)
    str1 = rectext.find('id="SSR_HYDRATED_DATA">window._SSR_HYDRATED_DATA')
    str2 = rectext.find('<!-- script -->')
    cutjson = rectext[str1+49:str2-9]
    #print(cutjson)
    #cutjson = cutjson.decode('utf-8')
    j = json.loads(cutjson)
    k = j['Projection']['video']
    
    if 'videoResource' in k:
            #projection
            for index in range(len(j['Projection']['video']['videoResource']['normal']['video_list'])):
                qxd = j['Projection']['video']['videoResource']['normal']['video_list']
                murl = j['Projection']['video']['videoResource']['normal']['video_list']['video_'+str(len(qxd)-index)]['main_url']
                #burl = j['Projection']['video']['videoResource']['normal']['video_list']['video_'+str(len(qxd)-index)]['backup_url_1']
                murl = str(base64.b64decode(murl))
                #burl = str(base64.b64decode(burl))
                mp4list[j['Projection']['video']['videoResource']['normal']['video_list']['video_'+str(len(qxd)-index)]['definition']] = murl
    else:
            #print('teleplay')
            #print('官方解析 normal')
            for index in range(len(j['Teleplay']['videoResource']['normal']['video_list'])):
                qxd = j['Teleplay']['videoResource']['normal']['video_list']
                murl = j['Teleplay']['videoResource']['normal']['video_list']['video_'+str(len(qxd)-index)]['main_url']
                #burl = j['Teleplay']['videoResource']['normal']['video_list']['video_'+str(len(qxd)-index)]['backup_url_1']
                murl = str(base64.b64decode(murl))
                #burl = str(base64.b64decode(burl))
                mp4list['norn api '+j['Teleplay']['videoResource']['normal']['video_list']['video_'+str(len(qxd)-index)]['definition']] = murl
                #mp4list[burl] = burl
            
        #print('官方解析 dash')
            #for index in range(len(j['Teleplay']['videoResource']['dash']['dynamic_video']['dynamic_video_list'])):
                #qxd = j['Teleplay']['videoResource']['dash']['dynamic_video']['dynamic_video_list']
                #print(len(qxd))
                #murl = j['Teleplay']['videoResource']['dash']['dynamic_video']['dynamic_video_list'][len(qxd)-index-1]['main_url']
                #burl = j['Teleplay']['videoResource']['dash']['dynamic_video']['dynamic_video_list'][len(qxd)-index-1]['backup_url_1']
                #print()
                #mp4list['dash api' + j['Teleplay']['videoResource']['dash']['dynamic_video']['dynamic_video_list'][len(qxd)-index-1]['definition']] = 'http://'+murl
                #print('http://'+murl)
                #print('http://'+burl)
    
    
        

    #print(str(base64.b64decode(burl),encoding = 'utf-8'))
 

    return mp4list

@plugin.cached(TTL=60)
def get_duop(url):
    videos = []
    rec = requests.get(url,headers=headers,cookies=cookies)
    rectext = rec.text
    #print(rectext)
    str1 = rectext.find('id="SSR_HYDRATED_DATA">window._SSR_HYDRATED_DATA')
    str2 = rectext.find('<!-- script -->')
    cutjson = rectext[str1+49:str2-9]
    #print(cutjson)
    try:
        j = json.loads(cutjson)
    except ValueError:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('错误提示', '空的')
    
    try:
        for index in range(len(j['Teleplay']['playlist'])):
            videoitem = {}
            videoitem['name'] = '['+ str(index+1) + ']' + j['Teleplay']['playlist'][index]['title']
            videoitem['href'] = 'http://www.ixigua.com/i'+str(j['Teleplay']['playlist'][index]['episodeId'])
            videos.append(videoitem)  
    except TypeError:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('错误提示', '空的1')
    return videos

@plugin.cached(TTL=60)
def get_videos(cag):
    url = 'https://www.ixigua.com/cinema/filter/'+cag+'/'
    api11 = '[api1]'
    api11 = api11.decode('utf-8')
    api22 = '[api2]'
    api22 = api22.decode('utf-8')
    videos = []
    rec = requests.get(url,headers=headers,cookies=cookies)

    rectext = rec.text
    str1 = rectext.find('id="SSR_HYDRATED_DATA">window._SSR_HYDRATED_DATA')
    str2 = rectext.find('<!-- script -->')
    cutjson = rectext[str1+49:str2-9]
    #print(cutjson)
    #cutjson = cutjson.encode('utf-8')
    j = json.loads(cutjson)
    videolist = j['AlbumInCategory'][0]['albumList']
    xbmc.log(str(len(videolist)),debug)
    for index in range(len(videolist)):
        jishu = ''
        ji = '集'
        quan = '全'
        gxz = '更新至'
        ji = ji.decode('utf-8')
        quan = quan.decode('utf-8')
        gxz = gxz.decode('utf-8')
        if videolist[index]['latestSeq'] != 1:
            if videolist[index]['latestSeq'] == videolist[index]['totalEpisodes']:
                jishu = '[' + str(videolist[index]['latestSeq'])+ji+quan+ ']'
            else:
                jishu = '['+gxz + str(videolist[index]['latestSeq'])+ji+ ']'
        videoitem = {}
        videoitem['name'] = api11+videolist[index]['title'] +  jishu 
        videoitem['href'] = videolist[index]['shareUrl']
        videoitem['thumb'] = videolist[index]['coverList'][0]['url']
        videos.append(videoitem)
#api2
    url = 'https://www.ixigua.com/channel/'+cag + '/'
    rec = requests.get(url,headers=headers,cookies=cookies)

    rectext = rec.text
    str1 = rectext.find('<script id="SSR_HYDRATED_DATA">window._SSR_HYDRATED_DATA=')
    str2 = rectext.find('<!-- script -->')
    cutjson = rectext[str1+57:str2-9]
    #print(cutjson)
    #xbmc.log('api2'+cutjson,debug)
    j = json.loads(cutjson)
    for index in range(len(j['Channel'][cag]['operationData']['list'])):
        videoitem = {}
        videoitem['name'] = api22+j['Channel'][cag]['operationData']['list'][index]['title']
        videoitem['href'] = j['Channel'][cag]['operationData']['list'][index]['shareUrl']
        videoitem['thumb'] = j['Channel'][cag]['operationData']['list'][index]['coverList'][0]['url']
        videos.append(videoitem)  
    return videos



def get_categories():
    return [{'name':'电视剧','link':'dianshiju'},
            {'name':'电影','link':'dianying'},
            {'name':'综艺','link':'zongyi'},
            {'name':'少儿','link':'shaoer'},
            {'name':'动漫','link':'dongman'},
            {'name':'纪录片','link':'jilupian'}]


@plugin.route('/duop/<url>/')
def duop(url):
    videos = get_duop(url)
    items = [{
        'label': video['name'],
        'path': plugin.url_for('play', name=video['name'].encode('utf-8') , url=video['href']),
    } for video in videos]

    return items

@plugin.route('/play/<name>/<url>/')
def play(name,url):
    mp4list = get_mp4(url)
    items = []
    for k,i in mp4list.items():

        item = {'label':'[' + k.encode('utf-8') + ']' + name,'path':i.encode('utf-8'),'is_playable': True,'info':('video')}
        #item.setInfo('video',{})
        items.append(item)
    return items

@plugin.route('/category/<name>/<url>/')
def category(name,url):
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', url)

    videos = get_videos(url)
    items = [{
        'label': video['name'],
        'path': plugin.url_for('duop', url=video['href']),
	'thumbnail': video['thumb'],
        'icon': video['thumb'],
    } for video in videos]

    return items




@plugin.route('/')
def index():
    categories = get_categories()
    items = [{
        'label': category['name'],
        'path': plugin.url_for('category', name=category['name'] , url=category['link']),
    } for category in categories]
    items.append({
        'label': u'[COLOR yellow]i号[/COLOR]',
        'path': plugin.url_for('ilist'),
    })
    
    return items

@plugin.route('/ilist')
def ilist():
    items = []
    items.append({
        'label': u'输入i号或者album号',
        'path': plugin.url_for('album'),
    })
    items.append({
        'label': u'从网络剪贴板(ykjtb.com)导入西瓜视频链接',
        'path': plugin.url_for('ykjtb'),
    })
    items.append({
        'label': u'从网络剪贴板(netcut.cn)导入西瓜视频链接',
        'path': plugin.url_for('netcut'),
    })
    return items

@plugin.route('/labels/<label>/')
def show_label(label):
    # 写抓取视频类表的方法
    #
    items = [
        {'label': label},
    ]
    return items



@plugin.route('/search')
def search():
    keyboard = xbmc.Keyboard('', '请输入搜索内容')
    xbmc.sleep(1500)
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        keyword = keyboard.getText()
        #url = HOST_URL + '/index.php?m=vod-search&wd=' + keyword
        # https://www.nfmovies.com/search.php?page=1&searchword='+keyword+'&searchtype=

        videos = get_search(keyword, 1)
        items = [{
            'label': video['name'],
            'path': plugin.url_for('sources', url=video['href']),
            'thumbnail': video['thumb'],
            'icon': video['thumb']
        } for video in videos]

        sorted_items = items
        # sorted_items = sorted(items, key=lambda item: item['label'])
        #nextpage = {'label': ' 下一页', 'path': plugin.url_for('searchMore', keyword=keyword, page=2)}
        #sorted_items.append(nextpage)
        return sorted_items

@plugin.route('/album')
def album():
    keyboard = xbmc.Keyboard('', '请输入i号（纯数字）或者album号（字母数字混合）：')
    xbmc.sleep(1500)
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        keyword = keyboard.getText()
        #url = HOST_URL + '/index.php?m=vod-search&wd=' + keyword
        # https://www.nfmovies.com/search.php?page=1&searchword='+keyword+'&searchtype=
        if str(keyword).isdigit():
            #纯数字
            videos = get_mp4('https://www.ixigua.com/i'+str(keyword))
            items = []
            for k,i in videos.items():

                item = {'label':'[' + k.encode('utf-8') + ']','path':i.encode('utf-8'),'is_playable': True,'info':('video')}
                items.append(item)
        else:
            #字母混合
            videos = get_duop('https://www.ixigua.com/cinema/album/'+str(keyword))
            items = [{
                'label': video['name'],
                'path': plugin.url_for('play', name=video['name'].encode('utf-8') , url=video['href']),
            } for video in videos]

        return items

@plugin.route('/ykjtb')
def ykjtb():
    keyboard = xbmc.Keyboard('', '请输入取件码(4位数)：')
    xbmc.sleep(1500)
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        yanzhenma = keyboard.getText()
        apiurl = 'https://ykjtb.com/v?g='
        rec = requests.get(apiurl + yanzhenma,headers=headers)
        #print(rec.text)
        soup = BeautifulSoup(rec.text, "html5lib")
        if soup.find('div',id='ycontent',class_='row viewcontent'):
            cut = soup.find('div',id='ycontent',class_='row viewcontent')
            cut = cut.text
            items = []
            if re.search(r'ixigua.com/cinema/album/[a-zA-Z0-9]+',cut) or re.search(r'ixigua.com/i[0-9]+',cut):

                if re.search(r'ixigua.com/cinema/album/[a-zA-Z0-9]+',cut):
                    parse = 'https://www.' + re.search(r'ixigua.com/cinema/album/[a-zA-Z0-9]+',cut).group()
                    dialog = xbmcgui.Dialog()
                    ok = dialog.ok('提示', '解析成功:album号视频\n解析地址：'+parse.encode('utf-8'))
                    items.append({
                        'label': parse,
                        'path': plugin.url_for('duop',url=parse),
                    })
                else:
                    parse = 'https://www.' + re.search(r'ixigua.com/i[0-9]+',cut).group()
                    dialog = xbmcgui.Dialog()
                    ok = dialog.ok('提示', '解析成功:i号视频\n解析地址：'+parse.encode('utf-8'))
                    items.append({
                        'label': parse,
                        'path': plugin.url_for('play',name=parse,url=parse),
                    })
            else:
                dialog = xbmcgui.Dialog()
                ok = dialog.ok('提示', '错误:不受支持的西瓜视频链接\n\n支持的链接：\n https://www.ixigua.com/cinema/album/842PbwV4gJU \n https://www.ixigua.com/i6792449977898500611')
        else:
            dialog = xbmcgui.Dialog()
            ok = dialog.ok('提示', '取件码错误')
        return items

@plugin.route('/netcut')
def netcut():
    keyboard = xbmc.Keyboard('', '请在netcut.cn创建剪切板后，在这里输入剪切板名称(请勿设置密码)：')
    xbmc.sleep(1500)
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        yanzhenma = keyboard.getText()
        apiurl = 'https://netcut.cn/'
        rec = requests.get(apiurl + yanzhenma,headers=headers)
        #print(rec.text)
        soup = BeautifulSoup(rec.text, "html5lib")
        jiami = soup.find('div',class_='tip-text')
        body = soup.find('body')
        dataid = body['data-id']
        #判断是否加密
        #dialog = xbmcgui.Dialog()
        #ok = dialog.ok('提示', jiami.text)
        try:
            if jiami.text:
                dialog = xbmcgui.Dialog()
                ok = dialog.ok('提示', '错误：都说了不要设置密码，你还偏设置密码，你让我导入个锤子？')

        except AttributeError:
            print('莫得加密')
            rec = requests.get('https://netcut.cn/api/note/data/?note_id='+dataid+'&_='+str(t),headers=headers,cookies=rec.cookies)
            j = json.loads(rec.text)
            if j['status'] == 0:
                dialog = xbmcgui.Dialog()
                ok = dialog.ok('提示', '错误：剪切板内容为空，请检查输入是否正确')
            else:
                #jixu
                text = j['data']['note_content']
                items = []
                if re.search(r'ixigua.com/cinema/album/[a-zA-Z0-9]+',text) or re.search(r'ixigua.com/i[0-9]+',text):

                    if re.search(r'ixigua.com/cinema/album/[a-zA-Z0-9]+',text):
                        parse = 'https://www.' + re.search(r'ixigua.com/cinema/album/[a-zA-Z0-9]+',text).group()
                        dialog = xbmcgui.Dialog()
                        ok = dialog.ok('提示', '解析成功:album号视频\n解析地址：'+parse.encode('utf-8'))
                        items.append({
                            'label': parse,
                            'path': plugin.url_for('duop',url=parse),
                        })
                    else:
                        parse = 'https://www.' + re.search(r'ixigua.com/i[0-9]+',text).group()
                        dialog = xbmcgui.Dialog()
                        ok = dialog.ok('提示', '解析成功:i号视频\n解析地址：'+parse.encode('utf-8'))
                        items.append({
                            'label': parse,
                            'path': plugin.url_for('play',name=parse,url=parse),
                        })
                else:
                    dialog = xbmcgui.Dialog()
                    ok = dialog.ok('提示', '错误:不受支持的西瓜视频链接\n\n支持的链接：\n https://www.ixigua.com/cinema/album/842PbwV4gJU \n https://www.ixigua.com/i6792449977898500611')
            
    return items

if __name__ == '__main__':
    plugin.run()