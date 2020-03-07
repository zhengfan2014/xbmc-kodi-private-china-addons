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
import random
 



def unescape(string):
    string = urllib2.unquote(string).decode('utf8')
    quoted = HTMLParser.HTMLParser().unescape(string).encode('utf-8')
    #转成中文
    return re.sub(r'%u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})', lambda m: unichr(int(m.group(1), 16)), quoted)


plugin = Plugin()


headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
mheaders = {'user-agent' : 'Mozilla/5.0 (Linux; Android 10; Z832 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36'}







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
    rectext = r.text
    cutjson =str(rectext.encode('utf-8'))
    str1 = cutjson.find('window.__INITIAL_STATE__=')
    str2 = cutjson.find(';(function(){var s;')
    rankinfojson = cutjson[str1+25:str2]
    j = json.loads(rankinfojson)

    #urlnum = category[:-4]
    #cut = re.compile('\d+')
    #rid = cut.findall(urlnum)

    
    #rec = requests.get('https://api.bilibili.com/x/web-interface/ranking?day=1&rid='+str(rid[0]))
    #rectext = rec.text
    #j = json.loads(rectext)
    #k = j['data']['list'][0]['pic']
    #k = k.encode('utf-8')

    #if urlnum.find('all') != None:
        #普通排行榜
    #else:
        #if urlnum.find('bangumi') != None:
            #番剧排行榜


    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', rankinfojson)
    if videoelements is None:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('错误提示', '没有播放源')
    else:
        #dialog = xbmcgui.Dialog()
        #sss = str(len(videoelements))
        #ok = dialog.ok('video数量', sss)
        num = 0
        for videoelement in videoelements:
            #img = videoelement.find('img')['alt']
            #imgcut = img.find('.png@')
            #img = img[:imgcut] + '.png'
            #dialog = xbmcgui.Dialog()
            #ok = dialog.ok('错误提示', img)
            img = j['rankList'][num]['pic']
            img = img.encode('utf-8')
            videoitem = {}
            videoitem['name'] = videoelement.find('img')['alt']
            videoitem['href'] = videoelement.find('a')['href']
            videoitem['thumb'] = img
            videoitem['genre'] = '豆瓣电影'
            
            videos.append(videoitem)
            num = num+1
        return videos

def get_sources(url):
    sources = []
    if re.match('https://',url) == None:
      if re.match('http://',url) != None:
        url = 'https://'+url[7:]
      else:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('错误提示', '非法url')

    ifbangumiurl = re.match('https://www.bilibili.com/bangumi/play/ss',url)
    ifvideourl = re.match('https://www.bilibili.com/video/av',url)
    if ifbangumiurl or ifvideourl != None:
      if ifbangumiurl != None:
    
        rec = requests.get('http://m'+url[11:],headers=mheaders)
        rec.encoding = 'utf-8'
        soup = BeautifulSoup(rec.text, 'html.parser')
        htmll = soup.find_all('script')
        rectext = rec.text


        #切出番剧信息的json
        cutjson =str(rectext.encode('utf-8'))
        str1 = cutjson.find('window.__INITIAL_STATE__=')
        str2 = cutjson.find(';(function(){var s;')
        videoinfojson = cutjson[str1+25:str2]
        #print(videoinfojson)

        j = json.loads(videoinfojson)
        #j是字典
        k = j['epList']
        
        #print(len(k))
        for index in range(len(k)):
            item = k[index]
            title = item['long_title']
            title = title.encode('utf-8')
            videosource = {}
            #print('视频标题：')
            videosource['name'] = '【P'+str(index+1)+'】'+title
            #print('视频图片：')
            videosource['thumb'] = item['cover']
            #print('视频地址：')
            videosource['href'] = plugin.url_for('play', url=item['link'])
            videosource['category'] = '番剧'
            sources.append(videosource)
        return sources





      else:
        #print('视频')
        rec = requests.get(url,headers=headers)
        soup = BeautifulSoup(rec.text, 'html.parser')
        ifpnum = soup.find_all('div',class_='multi-page report-wrap-module report-scroll-module')
        if ifpnum != []:
          #print('多p')
          rec = requests.get('http://m'+url[11:],headers=mheaders)
          cutjson =str(rec.text)
          str1 = cutjson.find('window.__INITIAL_STATE__=')
          str2 = cutjson.find('if(window.__INITIAL_STATE__.abserver)')
          videoinfojson = cutjson[str1+25:str2-6]
          #print(videoinfojson)
          j = json.loads(videoinfojson)
          #j是字典
          k = j['reduxAsyncConnect']['videoInfo']['pages']
          #print(len(k))
          #图片
          #print(j['reduxAsyncConnect']['videoInfo']['pic'])
          #名
          #print(j['reduxAsyncConnect']['videoInfo']['title'])
          #介绍
          #print(j['reduxAsyncConnect']['videoInfo']['desc'])
          for index in range(len(k)):
            duration = k[index]['duration']
            min = str(duration//60)
            sec = duration%60-1
            if sec < 10:
              sec = str('0') + str(sec)
            sec = str(sec)

            videosource = {}
            videosource['name'] = '【P' + str(index+1) + '】' + k[index]['part'] + ' - ' + min + ':' + sec
            videosource['thumb'] = j['reduxAsyncConnect']['videoInfo']['pic']
            videosource['category'] = '多p'
            videosource['href'] = url + '?p=' + str(index+1)
            sources.append(videosource)
          return sources


        else:
          #print('单p')
          rec = requests.get(url,headers=headers)
          rec.encoding = 'UTF-8'
          soup = BeautifulSoup(rec.text, 'html.parser')
          videotitle = soup.find(name='title')
          videoimage = soup.find(itemprop='image')
          videodesc = soup.find(itemprop='description')
          #dialog = xbmcgui.Dialog()
          #ok = dialog.ok('错误提示', videoimage['content'])
          videotitle = videotitle.text[:-26]
          videoimage = videoimage['content']
          
          

          videosource = {}
          videosource['name'] = '【P1】' + videotitle.encode('utf-8')
          videosource['thumb'] = videoimage.encode('utf-8')
          videosource['category'] = 'danp'
          videosource['href'] = plugin.url_for('play', url=url)
          sources.append(videosource)
          return sources
          #print(str(videodesc['content']))



@plugin.route('/play/<url>/')
def play(url):
    #r = requests.get(url, headers=headers)
    #r.encoding = 'UTF-8'
    #pattern = re.compile("now\=unescape\(\"([^\"]*)\"\)")
    #playurl = unescape(str(pattern.findall(r.text)[0]))



    hash = '05b29af8d098b8ca46bbd2d73fc52ab0'
    apilist1=['https://happyukgo.com/','https://helloacm.com/','https://steakovercooked.com/','https://anothervps.com/','https://isvbscriptdead.com/','https://zhihua-lai.com/','https://weibomiaopai.com/','https://steemyy.com/']

    #url = 'https://m.bilibili.com/video/av84351845'
    apiurl = apilist1[random.randint(0,7)]+'api/video/?cached&lang=ch&page=bilibili&hash='+hash+'&video='+url

    #print(apiurl)

    #headers = {'user-agent' : 'Mozilla/5.0 (Linux; Android 10; Z832 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36'}
    


    #api2
    payload = {'urlav': url}

    r = requests.post("https://www.xbeibeix.com/api/bilibili.php",data=payload,headers=mheaders)
    r.encoding = 'UTF-8'
    #print(r.text)
    soup = BeautifulSoup(r.text, 'html.parser')
    videodown = soup.find(download='视频.mp4')
    #bangumidown = soup.find('iframe',class_='embed-responsive-item')
    #bangumidown = bangumidown['src']

    rtext = r.text
    
    cuthtml1 =str(rtext.encode('utf-8'))
    str1 = cuthtml1.find('清晰度：')
    str2 = cuthtml1.find('P</p></li>')
    apiqingxidu = cuthtml1[str1+8:str2]
    #print('【1080P】 FLV - 由' + j['server']+'的api解析')

    #print(j['url'])
    #print('【'+apiqingxidu+'P】 MP4 - 由xbeibeix.com的api解析')

    cuthtml2 =str(rtext.encode('utf-8'))
    str1 = cuthtml2.find('封面：')
    str2 = cuthtml2.find('ng</p></li>')
    apiimage = cuthtml2[str1+3:str2] + 'ng'
    #print(apiimage)

    #print('--'*100)
    #print(videodown['href'])




    ifbangumiurl = re.match('https://www.bilibili.com/bangumi/play/ep',url)
    ifvideourl = re.match('https://www.bilibili.com/video/av',url)
    if ifbangumiurl or ifvideourl != None:
      if ifbangumiurl != None:
        #番剧
        cutep = url.find('y/ep')
        epnum = url[cutep+4:]
        epnum = re.sub(r'\D','',epnum)
        apiurl = 'https://api.bilibili.com/pgc/player/web/playurl/html5?ep_id='
        rec = requests.get(apiurl+epnum,headers=mheaders)
        #rec.encoding = 'utf-8'
        rectext = rec.text
        rectext = rectext.encode('utf-8')
        j = json.loads(rec.text)


        if j['code'] == 0:
          k = j['result']['durl']

          #dialog = xbmcgui.Dialog()
          #ok = dialog.ok('错误提示', str(k[0]['url']))

          #item = {'label': '【P】 MP4 - 由xbeibeix.com的api解析','path': videodown['href'],'is_playable': True}
          item = {'label': '【540P】 6分钟教育片 - 本地解析 ','path': k[0]['url'],'is_playable': True}
          items = []
          items.append(item)
        else:
          if j['code'] == -10403:
            #大会员错误码
            dialog = xbmcgui.Dialog()
            ok = dialog.ok('错误提示', '此为大会员专享视频，无法解析')
          else:
            #
            dialog = xbmcgui.Dialog()
            ok = dialog.ok('错误提示', '未知的api错误代码,可能是b站官方更改了接口')
        


        k = j['result']['durl']

        #dialog = xbmcgui.Dialog()
        #ok = dialog.ok('错误提示', str(k[0]['url']))

        #item = {'label': '【P】 MP4 - 由xbeibeix.com的api解析','path': videodown['href'],'is_playable': True}
        item = {'label': '【540P】 6分钟教育片 - 本地解析 ','path': k[0]['url'],'is_playable': True}
        items = []
        items.append(item)
        return items
      else:
        
        #视频
        #api1
        items = []
        rec = requests.get(apiurl,headers=mheaders)
        if rec.status_code == 200 :
          result = eval(repr(rec.text).replace('\\', ''))
          #print(result)
          j = json.loads(result)

          item = {'label': '【'+apiqingxidu+'P】 FLV - 由weibomiaopai.com的api解析','path': j['url'],'is_playable': True}
          items = []
          items.append(item)
        else:
          if rec.status_code == 503 :
            item = {'label': '解析失败 ,hash失效','path': '123','is_playable': True}
            
            items.append(item)


        
        #items = []
        
        item = {'label': '【'+apiqingxidu+'P】 MP4 - 由xbeibeix.com的api解析','path': videodown['href'],'is_playable': True}
        items.append(item)
        return items



@plugin.route('/sources/<url>/')
def sources(url):
    sources = get_sources(url)
    items = [{
        'label': source['name'],
        'path': source['href']
        #'is_playable': True
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
        'path': plugin.url_for('sources', url=video['href']),
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
    items.append({
        'label': u'[COLOR yellow]搜索[/COLOR]',
        'path': plugin.url_for('search'),
    })
    
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


def get_search(keyword, page):
    # if int(page) == 1:
    #     pageurl = category
    # else:
    #     pageurl = category + 'index_'+page+'.html'
    serachUrl = 'https://api.bilibili.com/x/web-interface/search/all/v2?keyword=' + keyword + '&page=' + str(page)

    r = requests.get(serachUrl, headers=headers)
    r.encoding = 'UTF-8'
    j = json.loads(r.text)
    k = j['data']['result'][8]['data']
    videos = []
    #k = k.encode('utf-8')
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', arcurl)

    for index in range(len(k)):
        arcurl = k[index]['arcurl']
        title = k[index]['title']
        pic = k[index]['pic']
        duration = k[index]['duration']
        #清除b站api数据污染
        title = title.replace('<em class="keyword">', '')
        title = title.replace('</em>', '')
        
        videoitem = {}
        videoitem['name'] = title
        videoitem['href'] = arcurl
        videoitem['thumb'] = 'http://'+pic
        videoitem['genre'] = '喜剧片'
        videos.append(videoitem)
    return videos

    


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
