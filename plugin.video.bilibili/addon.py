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
import hashlib
 




def unescape(string):
    string = urllib2.unquote(string).decode('utf8')
    quoted = HTMLParser.HTMLParser().unescape(string).encode('utf-8')
    #转成中文
    return re.sub(r'%u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})', lambda m: unichr(int(m.group(1), 16)), quoted)


plugin = Plugin()



apikey = plugin.get_storage('apikey',TTL=30)
xbbxmp4 = plugin.get_storage('xbbxmp4',TTL=60)
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
mheaders = {'user-agent' : 'Mozilla/5.0 (Linux; Android 10; Z832 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36'}

@plugin.cached(TTL=10)
def get_hash():
    hashurl = 'https://weibomiaopai.com/online-video-download-helper/bilibili'
    rec = requests.get(hashurl,headers=headers)
    rec.encoding = 'utf-8'
    rte = rec.text
    str1 = rte.find('var freeservice=')
    str2 = rte.find('var thepage="bilibili";')
    cut = rte[str1+16:str2]
    cut = cut.replace('\n','')
    cut = cut.replace(';','')
    cut = cut.split("' + '")
    q = ''
    i = 2
    while (i < len(cut)):
        q += cut[i]
        i+=3
    q =  base64.b64decode(q)
    q =str(q)
    return q

@plugin.cached(TTL=60)
def get_bangumijson(url):
    cutep = url.find('y/ep')
    epnum = url[cutep+4:]
    epnum = re.sub(r'\D','',epnum)
    apiurl = 'https://api.bilibili.com/pgc/player/web/playurl/html5?ep_id='
    rec = requests.get(apiurl+epnum,headers=mheaders)
    #rec.encoding = 'utf-8'
    rectext = rec.text
    rectext = rectext.encode('utf-8')
    j = json.loads(rec.text)
    return j



@plugin.cached(TTL=60)
def get_api1(url,quality):
    bvid = re.search(r'BV[a-zA-Z0-9]+', url)
    bvurl = 'https://api.bilibili.com/x/web-interface/view?bvid='+bvid.group()
    r = requests.get(bvurl,headers=headers)
    j = json.loads(r.text)
    cid = j['data']['pages'][0]['cid']


    entropy = 'rbMCKn@KuamXWlPMoJGsKcbiJKUfkPF_8dABscJntvqhRSETg'
    appkey, sec = ''.join([chr(ord(i) + 2) for i in entropy[::-1]]).split(':')
    params = 'appkey=%s&cid=%s&otype=json&qn=%s&quality=%s&type=' % (appkey, cid, quality, quality)
    tmp = params + sec
    tmp = tmp.encode('utf-8')
    chksum = hashlib.md5(bytes(tmp)).hexdigest()
    url_api = 'https://interface.bilibili.com/v2/playurl?%s&sign=%s' % (params, chksum)
    apiheaders = {
        'Referer': url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    }
    # print(url_api)
    html = requests.get(url_api, headers=apiheaders).json()
    # print(json.dumps(html))
    video_list = []
    for i in html['durl']:
        video_list.append(i['url'])
    # print(video_list)
    return video_list[0]



@plugin.cached(TTL=60)
def get_api2(url):
    #判断缓存是否存在
    if ('sxe' in apikey.keys()):
        sxe = apikey['sxe']
    else:
        #提取sxe值
        r = requests.get('https://www.xbeibeix.com/api/bilibili/')
        soup = BeautifulSoup(r.text, 'html.parser')
        sxe = soup.find_all('input',type='hidden')
        sxe = sxe[1]['value']
        apikey['sxe'] = sxe



    #向xbeibeix.com api发送post请求，抓出视频地址
    payload = {'urlav': url,'sxe':sxe}
    
    r = requests.post("https://www.xbeibeix.com/api/bilibili/",data=payload,headers=mheaders)
    r.encoding = 'UTF-8'
    #print(r.text)
    soup = BeautifulSoup(r.text, 'html.parser')
    videodown = soup.find_all('option')
    rtext = r.text
   

    #cuthtml2 =str(rtext.encode('utf-8'))
    # str1 = cuthtml2.find('封面：')
    #str2 = cuthtml2.find('ng</p></li>')
    #apiimage = cuthtml2[str1+3:str2] + 'ng'
    mp4url = []
    for index in range(len(videodown)):
        try:
            mp4url.append(videodown[index]['value'])
        except KeyError:
            qqqqqq=1
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', str(mp4url))



    
    #xbbxmp4[url] = mp4url
    return mp4url




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

@plugin.cached(TTL=60)
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

@plugin.cached(TTL=60)
def get_sources(url):
    sources = []
    if re.match('https://',url) == None:
      if re.match('http://',url) != None:
        url = 'https://'+url[7:]
      else:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('错误提示', '非法url')

    ifbangumiurl = re.match('https://www.bilibili.com/bangumi/play/ss',url)
    ifvideourl = re.match('https://www.bilibili.com/video/',url)
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
            videosource['href'] = plugin.url_for('play',name='【P'+str(index+1)+'】'+title,url=item['link'])
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
          videotitle = videotitle.text[:-26]
          videoimage = videoimage['content']
          
          

          videosource = {}
          videosource['name'] = '【P1】' + videotitle.encode('utf-8')
          videosource['thumb'] = videoimage.encode('utf-8')
          videosource['category'] = 'danp'
          videosource['href'] = plugin.url_for('play', name=videotitle.encode('utf-8'),url=url)
          sources.append(videosource)
          return sources
          #print(str(videodesc['content']))



@plugin.route('/play/<name>/<url>/')
def play(name,url):
    ifbangumiurl = re.match('https://www.bilibili.com/bangumi/play/ep',url)
    ifvideourl = re.match('https://www.bilibili.com/video/',url)
    if ifbangumiurl or ifvideourl != None:
      if ifbangumiurl != None:
        #番剧
        items = []
        item = {'label': '6分钟试看 本地解析','path': plugin.url_for('bangumiapi', name=name,url=url)}
        items.append(item)
        return items
      else:
        
        #视频
        items = []
        item = {'label': '【1080p】使用 b站官方api 解析（万分感谢GitHub的Henryhaohao的开源项目）','path': plugin.url_for('api1', name=name,url=url,quality=80)}
        items.append(item)
        item = {'label': '【720p】使用 b站官方api 解析（万分感谢GitHub的Henryhaohao的开源项目）','path': plugin.url_for('api1', name=name,url=url,quality=64)}
        items.append(item)
        item = {'label': '【480p】使用 b站官方api 解析（万分感谢GitHub的Henryhaohao的开源项目）','path': plugin.url_for('api1', name=name,url=url,quality=32)}
        items.append(item)
        item = {'label': '【320p】使用 b站官方api 解析（万分感谢GitHub的Henryhaohao的开源项目）','path': plugin.url_for('api1', name=name,url=url,quality=16)}
        items.append(item)
        item = {'label': '【最高清晰度】使用 xbeibeix.com 解析','path': plugin.url_for('api2', name=name,url=url)}
        items.append(item)
        return items


@plugin.route('/bangumiapi/<name>/<url>/')
#解析番剧地址
def bangumiapi(name,url):
    j = get_bangumijson(url)
    if j['code'] == 0:
        k = j['result']['durl']
        item = {'label': '【540P】'+name,'path': k[0]['url'],'is_playable': True}
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
    return items

@plugin.route('/api1/<name>/<url>/<quality>/')
#使用weibomiaopai api解析
def api1(name,url,quality):
    mp4url = get_api1(url,quality)
    items = []
    head = '|Referer=https://api.bilibili.com/x/web-interface/view?bvid='
    item = {'label': '[FLV]'+name,'path': mp4url+head,'is_playable': True}
    items.append(item)
    return items

@plugin.route('/api2/<name>/<url>/')
def api2(name,url):
    mp4url = get_api2(url)
    head = '|Referer=https://api.bilibili.com/x/web-interface/view?bvid='
    items = []
    item = {'label': '[MP4]'+name,'path': mp4url[0],'is_playable': True}
    items.append(item)
    item = {'label': '[FLV]'+name,'path': mp4url[1]+head,'is_playable': True}
    items.append(item)
    item = {'label': '[FLV备用]'+name,'path': mp4url[2]+head,'is_playable': True}
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
