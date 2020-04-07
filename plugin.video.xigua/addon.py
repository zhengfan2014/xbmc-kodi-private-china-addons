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

cookie = plugin.get_storage('cookie',TTL=60)
cookiebak = plugin.get_storage('cookiebak')
apicache = plugin.get_storage('apicache',TTL=60)

#@plugin.cached(TTL=60*24)
def cook():
    if 'wafid' in cookie:
        q = 1

        dialog = xbmcgui.Dialog()
        dialog.notification('提示', '缓存中已有wafid,跳过获取wafid', xbmcgui.NOTIFICATION_INFO, 2000,False)
    else:
        #if 'wafid' in cookiebak:
            #r = requests.get('http://www.ixigua.com',headers=headers,cookies=cookiebak)
        #else:
        r = requests.get('http://www.ixigua.com',headers=headers)
        
    
        if r.cookies['wafid']:
            cookie['wafid']=r.cookies['wafid']
            cookiebak['wafid']=r.cookies['wafid']
            dialog = xbmcgui.Dialog()
            dialog.notification('提示', '成功获取wafid并存入缓存', xbmcgui.NOTIFICATION_INFO, 2000,False)
        else:
            cookie['wafid']=cookiebak['wafid']
            dialog = xbmcgui.Dialog()
            ok = dialog.ok('提示', '未成功获取wafid,已尝试导入备份wafid\n\n如无法正常使用，请在 i号 - 导入西瓜视频wafid 中手动导入')
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', str(cookie['wafid']))
    cokie = {}
    cokie['wafid'] = cookie['wafid']
    return cokie

headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
cookies = cook()
#cook = plugin.get_storage('cook')

def writewafid(keyword):
    dialog = xbmcgui.Dialog()
    ret = dialog.yesno('即将导入', keyword)
    if ret:
        cookie['wafid'] = keyword
        cookiebak['wafid'] = keyword
        dialog = xbmcgui.Dialog()
        dialog.notification('提示', 'wafid已导入', xbmcgui.NOTIFICATION_INFO, 5000)

def testvideo():
    dialog = xbmcgui.Dialog()
    ret = dialog.contextmenu(['测试多P视频：纳米核心', '测试多P视频：干物妹小埋', '测试单P视频：秋名山电影'])
    if ret == 0:
        videos = get_duop('https://www.ixigua.com/cinema/album/7TiuG0Hp3iU','nocache')
    else:
        if ret == 1:
            videos = get_duop('https://www.ixigua.com/cinema/album/85ygYnLCcF9','nocache')
        else:
            videos = get_duop('https://www.ixigua.com/cinema/album/7MzYdM5GZIN','nocache')
    items = [{
        'label': video['name'],
        'path': plugin.url_for('play', name=video['name'].encode('utf-8') , url=video['href']),
    } for video in videos]
    return items

@plugin.cached(TTL=10)
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

    return mp4list

#@plugin.cached(TTL=1)
def get_duop(url,mode):
    if (url in apicache) and mode == 'cache':
        #dialog = xbmcgui.Dialog()
        #ok = dialog.ok('错误提示', '跳过')
        videos = apicache[url]
        q = '快进到魏文帝'
    else:
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
            ok = dialog.ok('错误提示', 'wafid失效')
    
        try:
            for index in range(len(j['Teleplay']['playlist'])):
                videoitem = {}
                videoitem['name'] = '['+ str(index+1) + ']' + j['Teleplay']['playlist'][index]['title']
                videoitem['href'] = 'http://www.ixigua.com/i'+str(j['Teleplay']['playlist'][index]['episodeId'])
                videos.append(videoitem)  
        except TypeError:
            dialog = xbmcgui.Dialog()
            ok = dialog.ok('错误提示', 'wafid失效')
    if videos and mode == 'cache':
        apicache[url] = videos
    return videos

#@plugin.cached(TTL=1)
def get_videos(cag):
    if cag in apicache:
        #dialog = xbmcgui.Dialog()
        #ok = dialog.ok('错误提示', '跳过')
        videos = apicache[cag]
        q = '快进到魏文帝'
    else:

        errornum = 0
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
        try:
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
        except TypeError:
            errornum += 1 
        except ValueError:
            errornum += 1 
    #api2
        url = 'https://www.ixigua.com/channel/'+cag + '/'
        rec = requests.get(url,headers=headers,cookies=cookies)

        rectext = rec.text
        str1 = rectext.find('<script id="SSR_HYDRATED_DATA">window._SSR_HYDRATED_DATA=')
        str2 = rectext.find('<!-- script -->')
        cutjson = rectext[str1+57:str2-9]
        #print(cutjson)
        #xbmc.log('api2'+cutjson,debug)
        try:
            j = json.loads(cutjson)
            for index in range(len(j['Channel'][cag]['operationData']['list'])):
                videoitem = {}
                videoitem['name'] = api22+j['Channel'][cag]['operationData']['list'][index]['title']
                videoitem['href'] = j['Channel'][cag]['operationData']['list'][index]['shareUrl']
                videoitem['thumb'] = j['Channel'][cag]['operationData']['list'][index]['coverList'][0]['url']
                videos.append(videoitem)  
        except TypeError:
            errornum += 1 
        except ValueError:
            errornum += 1 
        if errornum == 2:
            dialog = xbmcgui.Dialog()
            ok = dialog.ok('错误提示', 'wafid失效')
    if videos:
        apicache[cag] = videos
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
    videos = get_duop(url,'cache')
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
        'label': u'输入i号或者album号播放西瓜视频',
        'path': plugin.url_for('album'),
    })
    items.append({
        'label': u'输入完整链接播放西瓜视频',
        'path': plugin.url_for('link'),
    })
    items.append({
        'label': u'从网络剪贴板(ykjtb.com)导入西瓜视频链接',
        'path': plugin.url_for('ykjtb',mode='url'),
    })
    items.append({
        'label': u'从网络剪贴板(netcut.cn)导入西瓜视频链接',
        'path': plugin.url_for('netcut',mode='url'),
    })
    items.append({
        'label': u'导入西瓜视频wafid',
        'path': plugin.url_for('wafid'),
    })
    items.append({
        'label': u'从网络剪贴板(ykjtb.com)导入西瓜视频wafid',
        'path': plugin.url_for('ykjtb',mode='wafid'),
    })
    items.append({
        'label': u'从网络剪贴板(netcut.cn)导入西瓜视频wafid',
        'path': plugin.url_for('netcut',mode='wafid'),
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





@plugin.route('/link')
def link():
    keyboard = xbmc.Keyboard('', '请输入西瓜视频链接（ixigua.com）：')
    xbmc.sleep(1500)
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        keyword = keyboard.getText()
        if re.search(r'ixigua.com/cinema/album/[a-zA-Z0-9]+',keyword) or re.search(r'ixigua.com/i[0-9]+',keyword):
            items = []
            if re.search(r'ixigua.com/cinema/album/[a-zA-Z0-9]+',keyword):
                parse = 'https://www.' + re.search(r'ixigua.com/cinema/album/[a-zA-Z0-9]+',keyword).group()
                dialog = xbmcgui.Dialog()
                ok = dialog.ok('提示', '解析成功:album号视频\n解析地址：'+parse.encode('utf-8'))
                items.append({
                    'label': parse,
                    'path': plugin.url_for('duop',url=parse),
                })
            else:
                parse = 'https://www.' + re.search(r'ixigua.com/i[0-9]+',keyword).group()
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
            videos = get_duop('https://www.ixigua.com/cinema/album/'+str(keyword),'cache')
            items = [{
                'label': video['name'],
                'path': plugin.url_for('play', name=video['name'].encode('utf-8') , url=video['href']),
            } for video in videos]

        return items

@plugin.route('/wafid')
def wafid():
    keyboard = xbmc.Keyboard('', '请输入西瓜视频cookie里wafid的值：')
    xbmc.sleep(1500)
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        keyword = keyboard.getText()
        #url = HOST_URL + '/index.php?m=vod-search&wd=' + keyword
        # https://www.nfmovies.com/search.php?page=1&searchword='+keyword+'&searchtype=
        items = [] 
        writewafid(keyword)
        dialog = xbmcgui.Dialog()
        ret = dialog.yesno('提示', '是否测试解析视频？')
        if ret:
            items = testvideo()
        
        return items

@plugin.route('/ykjtb/<mode>/')
def ykjtb(mode):
    if mode == 'url':
        imputinfo = '请输入取件码(4位数)提取链接：'
    else:
        imputinfo = '请输入取件码(4位数)提取wafid：'
    keyboard = xbmc.Keyboard('', imputinfo)
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
            if mode == 'url': 
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
                try:
                    parse = re.search(r'[A-Za-z0-9\-]+',cut).group()
                    writewafid(parse)
                    dialog = xbmcgui.Dialog()
                    ret = dialog.yesno('提示', '是否测试解析视频？')
                    if ret:
                        items = testvideo()
                except TypeError:
                    dialog = xbmcgui.Dialog()
                    ok = dialog.ok('提示', '123')
        else:
            dialog = xbmcgui.Dialog()
            ok = dialog.ok('提示', '取件码错误')
        return items

@plugin.route('/netcut/<mode>/')
def netcut(mode):
    if mode == 'url':
        imputinfo = '请输入剪切板名称(请勿设置密码)提取链接：'
    else:
        imputinfo = '请输入剪切板名称(请勿设置密码)提取wafid：'
    keyboard = xbmc.Keyboard('', imputinfo)
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
                if mode =='url':
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
                else:
                    try:
                        parse = re.search(r'[A-Za-z0-9\-]+',text).group()
                        writewafid(parse)
                        dialog = xbmcgui.Dialog()
                        ret = dialog.yesno('提示', '是否测试解析视频？')
                        if ret:
                            items = testvideo()
                    except TypeError:
                        print('766')
            
    return items

if __name__ == '__main__':
    plugin.run()