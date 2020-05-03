#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from xbmcswift2 import Plugin
import requests
from bs4 import BeautifulSoup
import xbmcgui
import time
import base64
import json
import urllib2
import sys
import HTMLParser
import re
import cfscrape
import random



def unescape(string):
    string = urllib2.unquote(string).decode('utf8')
    quoted = HTMLParser.HTMLParser().unescape(string).encode('utf-8')
    #转成中文
    return re.sub(r'%u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})', lambda m: unichr(int(m.group(1), 16)), quoted)


plugin = Plugin()


headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
tmp = plugin.get_storage('tmp')

#用户设置存储
storage = plugin.get_storage('storage')


def chushihua(key,default):
    if key in storage:
        switch = storage[key]
    else:
        storage[key] = default
        switch = storage[key]
    if switch == 1:
        value = '开'
    else:
        value = '关'
    return value

#违禁词替换
def check_filter(text):
    if 'keyword' in storage and chushihua('keywordswitch',0) == '开':
        keywords = storage['keyword']
        return re.sub("|".join(keywords),'***', text)
    else:
        return text

#判断是否含有违禁词
def if_filter(text):
    keywords = storage['blacklist']
    if re.search("|".join(keywords),text):
        return True
    else:
        return False

def get_videos_mode(page,mode):
    item = eval('get_' + mode + '_videos')(page)
    return item

def get_mp4info_mode(url,mode):
    item = eval('get_' + mode + '_mp4info')(url)                                 
    return item
def get_mp4_mode(url,mode):
    item = eval('get_' + mode + '_mp4')(url)
    return item

@plugin.cached(TTL=2)
def get_html(url):
    r = requests.get(url,headers=headers)
    r.encoding = 'utf-8'
    return r.text

@plugin.cached(TTL=2)
def post_html(url,data):
    data =eval(data)
    r = requests.post(url,headers=headers,data=data)
    r.encoding = 'utf-8'
    return r.text

#"%Y-%m-%d %H:%M:%S"
def unix_to_data(uptime,format):
    uptime = float(uptime)
    time_local = time.localtime(uptime)
    #转换成新的时间格式(2016-05-05 20:28:54)
    uptime = time.strftime(format,time_local)
    return uptime

def get_categories():
    return [{'id':1,'name':'虎嗅 huxiu.com','link':'huxiu'},
            {'id':2,'name':'机核 gcores.com','link':'gcore'},
            {'id':3,'name':'穷游 qyer.com','link':'qyer'},
            {'id':4,'name':'ZEALER zealer.com','link':'zeal'},
            {'id':5,'name':'澎湃 thepaper.cn','link':'pengpai'},
            {'id':6,'name':'新京报 bjnews.com.cn','link':'bjnews'},
            {'id':7,'name':'界面 jiemian.com','link':'jiemian'},
            {'id':8,'name':'36kr 36kr.com','link':'36kr'},
            {'id':9,'name':'环球 huanqiu.com','link':'huanqiu'}]

def get_huxiu_videos(page):
    videos = []
    if int(page) == 1:
        lasttime = time.time()
    else:
        lasttime = tmp['huxiulasttime'+str(page)]
    p = {'platform': 'www', 'last_time': lasttime,'channel_id' : 10}
    url='https://article-api.huxiu.com/web/channel/articleList'
    r = post_html(url,str(p))
    j = json.loads(r)
    tmp['huxiulasttime'+str(int(page)+1)] = j['data']['last_time']
    vlist = j['data']['datalist']
    for index in range(len(vlist)):
        videoitem = {}
        videoitem['name'] =  vlist[index]['title']
        videoitem['href'] =  'https://www.huxiu.com/article/' + str(vlist[index]['aid']) + '.html'
        videoitem['thumb'] = vlist[index]['origin_pic_path']
        videoitem['info'] = {'plot':vlist[index]['title'] + '\n\n' + vlist[index]['summary']}
        videos.append(videoitem)

    return videos

def get_huxiu_mp4info(url):
    rtext = get_html(url)
    rt = rtext
    str1 = rt.find('window.__INITIAL_STATE__=')
    str2 = rt.find(';(function(){var s;')
    cutjson = rt[str1+25:str2]
    j = json.loads(cutjson)
    mp4info = {}
    info = j['articleDetail']['articleDetail']
    mp4info['title'] = info['title']
    #作者
    mp4info['cast'] = [ info['author'] ]
    #简介
    mp4info['plot'] = info['summary']
    #unix时间
    mp4info['aired'] = unix_to_data(info['dateline'],'%Y-%m-%d')
    #图片
    mp4info['img'] = info['pic_path']
    #tag
    tags = []
    for tag in info['tags_info']:
        tags.append(tag['name'])
    mp4info['genre'] = tags
    return mp4info

def get_huxiu_mp4(url):
    videos = []
    rt = get_html(url)
    str1 = rt.find('window.__INITIAL_STATE__=')
    str2 = rt.find(';(function(){var s;')
    cutjson = rt[str1+25:str2]
    j = json.loads(cutjson)
    #mp4
    mp4list = j['articleDetail']['articleDetail']['video_info']
    if 'fhd_link' in mp4list:
        mp4 = mp4list['fhd_link']
    else:
        if 'hd_link' in mp4list:
            mp4 = mp4list['hd_link']
        else:
            if 'sd_link' in mp4list:
                mp4 = mp4list['sd_link']
            else:
                mp4 = ''
    return mp4

#机核
def get_gcore_videos(page):
    #爬视频列表的
    videos = []
    page = 12*(int(page)-1)
    url='https://www.gcores.com/gapi/v1/videos?page[limit]=12&page[offset]='+str(page)+'&sort=-published-at&include=category,user,djs&filter[list-all]=0&fields[videos]=title,desc,is-published,thumb,app-cover,cover,comments-count,likes-count,bookmarks-count,is-verified,published-at,option-is-official,option-is-focus-showcase,duration,category,user,djs'

    r = get_html(url)
    j = json.loads(r)
    vlist = j['data']
    for index in range(len(vlist)):
        videoitem = {}
        videoitem['name'] =  vlist[index]['attributes']['title']
        videoitem['href'] =  str(vlist[index]['id'])
        videoitem['thumb'] = 'https://image.gcores.com/' + vlist[index]['attributes']['thumb']
        videoitem['info'] = {'plot':vlist[index]['attributes']['title'] + '\n\n' + vlist[index]['attributes']['desc']}
        videos.append(videoitem)

    return videos

def get_gcore_mp4info(url):
    url = 'https://www.gcores.com/videos/'+str(url)
    rtext = get_html(url)
    soup = BeautifulSoup(rtext, "html5lib")
    mp4info = {}
    up = soup.find_all('a',class_='avatar avatar-lg avatar-v avatar-noBold mx-3 mb-3')
    cast = []
    for index in range(len(up)):
        cast.append(up[index].text)
    mp4info['cast'] = cast

    plot = soup.find('div',class_='story story-show')
    mp4info['plot'] = plot.text

    tags = soup.find_all('a',class_='label is_tags')
    tag = []
    for index in range(len(tags)):
        tag.append(tags[index].text)
    mp4info['genre'] = tag

    mp4info['img'] = tmp['gcoreimg']
    return mp4info

def get_gcore_mp4(url):
    videos = []
    url = 'https://www.gcores.com/gapi/v1/videos/'+str(url)+'?include=category,user,media,djs,user.role,tags,entities,entries,similarities.user,similarities.djs,similarities.category,collections&preview=1'
    rtext = get_html(url)
    j = json.loads(rtext)
    vid = j['data']['relationships']['media']['data']['id']
    for i in range(len(j['included'])):
        if int(j['included'][i]['id']) == int(vid):
            src = j['included'][i]['attributes']['original-src']
    if src != '':
        rt = get_html(src)
        soup = BeautifulSoup(rt, "html5lib")
        mp = soup.find('video',class_='video-js vjs-big-play-centered vjs-default-skin fill')
        mp4 = mp['data-url']
        tmp['gcoreimg'] = mp['poster']
    else:
        mp4 = ''
    return mp4

#穷游网
def get_qyer_videos(page):
    videos = []
    url='https://www.qyer.com/video/'

    rt = get_html(url)
    str1 = rt.find('window.__INITIAL_STATE__=')
    str2 = rt.find(';(function(){var s;')
    j =json.loads(rt[str1+25:str2])
    vlist = j['renderData']['data']['data']['partnervideos']
    for index in range(len(vlist)):
        tagname = vlist[index]['tagname']
        vvlist = vlist[index]['videos'][0]['videolist']
        for i in range(len(vvlist)):
            videoitem = {}
            videoitem['name'] =  u'[' + tagname + u']' + vvlist[i]['title']
            videoitem['href'] =  'https:' + vvlist[i]['pc_url']
            videoitem['thumb'] = 'https:' + vvlist[i]['cover_path']
            videoitem['info'] = {'plot':vvlist[i]['title']}
            videos.append(videoitem)

    return videos

def get_qyer_mp4info(url):
    rt = get_html(url)
    str1 = rt.find('window.__INITIAL_STATE__=')
    str2 = rt.find(';(function(){var s;')
    j =json.loads(rt[str1+25:str2])
    info = j['renderData']['data']['data']['video']
    mp4info ={}
    mp4info['title'] = info['title']
    mp4info['plot'] = info['description']
    mp4info['aired'] = info['date']
    mp4info['duration'] = info['duration']
    mp4info['img'] = 'http:' + info['cover_path']
    mp4info['cast'] = [(j['renderData']['data']['data']['partner']['name'],j['renderData']['data']['data']['partner']['description'])]
    return mp4info

def get_qyer_mp4(url):
    videos = []
    
    rt = get_html(url)
    str1 = rt.find('window.__INITIAL_STATE__=')
    str2 = rt.find(';(function(){var s;')
    j =json.loads(rt[str1+25:str2])
    mp4 = u'https:' + j['renderData']['data']['data']['video']['source_path']
    return mp4

#zealer
def get_zeal_videos(page):
    videos = []
    url='https://api.hub.zealer.com/postCategory/list?categoryPlatform=MEDIA&categoryType=CONTENT_TYPE&categoryId=0&pageNum='+str(page)+'&pageSize=6&sortType=latest'
    rt = get_html(url)
    j =json.loads(rt)
    vlist = j['data']['result']

    url2='https://api.hub.zealer.com/postCategory/list?categoryId=0&categoryPlatform=X&categoryType=CONTENT_TYPE&pageNum='+str(page)+'&pageSize=6&sortType=latest'
    rt2 = get_html(url2)
    j2 =json.loads(rt2)
    vlist2 = j2['data']['result']
    for index in range(len(vlist)):
        videoitem = {}
        videoitem['name'] =  vlist[index]['title']
        videoitem['href'] =  vlist[index]['id']
        videoitem['thumb'] = vlist[index]['cover']
        videoitem['info'] = {'plot':vlist[index]['title']}
        videos.append(videoitem)
        videoitem = {}
        videoitem['name'] =  vlist2[index]['title']
        videoitem['href'] =  vlist2[index]['id']
        videoitem['thumb'] = vlist2[index]['cover']
        videoitem['info'] = {'plot':vlist2[index]['title']}
        videos.append(videoitem)
    return videos

def get_zeal_mp4info(url):
    mp4info = {}
    r = get_html('https://api.hub.zealer.com/post?id=' + str(url))
    j =json.loads(r)
    d = j['data']['postInfo']
    mp4info ['title'] = d['title']
    mp4info ['plot'] = d['coverIntro']
    mp4info['img'] = d['coverUrl']
    mp4info['aired'] = unix_to_data(int(str(d['createdAt'])[:-3]),'%Y-%m-%d')
    
    tag = []
    for index in range(len(j['data']['contentTags'])):
        tag.append(j['data']['contentTags'][index]['name'])
    mp4info['genre'] = tag
    mp4info['tag'] = tag
    return mp4info

def get_zeal_mp4(url):
    r = get_html('https://api.hub.zealer.com/post?id=' + str(url))
    j =json.loads(r)
    appid = j['data']['postParameter']['appID']
    fileid = j['data']['postParameter']['fileID']
    sign = j['data']['postParameter']['sign']
    t = j['data']['postParameter']['t']
    us = j['data']['postParameter']['us']
    r = get_html('https://playvideo.qcloud.com/getplayinfo/v2/'+ str(appid) +'/'+ str(fileid) +'?exper=0&playerid=399601&sign='+ str(sign) +'&t='+ str(t) +'&us='+ str(us))
    j =json.loads(r)
    vlist = j['videoInfo']['transcodeList']
    width = 0
    for index in range(len(vlist)):
        if int(vlist[index]['width']) > width:
            width = int(vlist[index]['width'])
            mp4 = vlist[index]['url']
    return mp4

#澎湃新闻
def get_pengpai_videos(page):
    #爬视频列表的
    videos = []
    url = 'https://www.thepaper.cn/load_video_chosen.jsp?channelID=26916&pageidx=' +str(page)
    r = get_html(url)
    soup = BeautifulSoup(r, 'html.parser')

    imgsrc = soup.find_all('img')
    ahref = soup.find_all('a',class_='play has_pic')
    title = soup.find_all('div',class_='video_title')
    li = soup.find_all('li',class_='video_news')
    
    for index in range(len(li)):
        titletext = title[index].text
        titletext = titletext.strip()
        imgsrcurl = imgsrc[index]['src']
        videoitem = {}
        videoitem['name'] = titletext
        videoitem['href'] = 'https://thepaper.cn/' + ahref[index]['href']
        videoitem['thumb'] = 'http' + imgsrcurl[5:]
        videoitem['info'] = {'plot':li[index].p.text}
        videos.append(videoitem)
    return videos

def get_pengpai_mp4info(url):
    mp4info = {}
    r = get_html(url)
    soup = BeautifulSoup(r, 'html.parser')

    img = soup.find('video',class_='video_detail video-js vjs-default-skin vjs-big-play-centered')
    j = json.loads(img['data-setup'])
    mp4info['img'] = j['poster']

    plot = soup.find('div',class_='video_txt_l')
    mp4info['plot'] = plot.p.text.strip()
    
    tag = soup.find('a',class_='genzong')
    genre = soup.find('div',class_='video_txt_r_icon')
    mp4info['genre'] = [tag.text[4:],genre.p.text.strip()]
    mp4info['tag'] = [tag.text[4:],genre.p.text.strip()]

    data = soup.find('div',class_='video_info_left')
    mp4info['aired'] = re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}',data.text).group()
    return mp4info

def get_pengpai_mp4(url):
    r = get_html(url)
    soup = BeautifulSoup(r, 'html.parser')
    mp4 = soup.find('source',type='video/mp4')
    return mp4['src']

#新京报
def get_bjnews_videos(page):
    videos = []
    url = 'http://www.bjnews.com.cn/video/?page=' +str(page)
    r = get_html(url)
    soup = BeautifulSoup(r, 'html.parser')
    li = soup.find_all('li',class_='li_img')

    url2 = 'http://www.bjnews.com.cn/wevideo/?page=' +str(page)
    r2 = get_html(url2)
    soup2 = BeautifulSoup(r2, 'html.parser')
    li2 = soup2.find_all('li',class_='li_img')
    for index in range(len(li)):
        img = li[index].find('div',class_='fl')
        a = li[index].find('div',class_='li_rt')
        videoitem = {}
        videoitem['name'] = a.a.text
        videoitem['href'] = a.a['href']
        videoitem['thumb'] = img.a.img['src']
        videoitem['info'] = {'plot':a.a.text}
        videos.append(videoitem)
        img2 = li2[index].find('div',class_='fl')
        a2 = li2[index].find('div',class_='li_rt')
        videoitem = {}
        videoitem['name'] = a2.a.text
        videoitem['href'] = a2.a['href']
        videoitem['thumb'] = img2.a.img['src']
        videoitem['info'] = {'plot':a2.a.text}
        videos.append(videoitem)
    
    #for index in range(len(li)):
        
    return videos

def get_bjnews_mp4info(url):
    mp4info = {}
    r = get_html(url)
    soup = BeautifulSoup(r, 'html.parser')

    img = soup.find('video',id='example_video_1')
    mp4info['img'] = img['poster']

    plot = soup.find('p',class_='ctdesc')
    mp4info['plot'] = plot.text.strip()

    data = soup.find('span',class_='date')
    mp4info['aired'] = re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}',data.text).group()
    return mp4info

def get_bjnews_mp4(url):
    r = get_html(url)
    soup = BeautifulSoup(r, 'html.parser')
    mp4 = soup.find('video',id='example_video_1')
    return mp4.source['src']

#界面新闻
def get_jiemian_videos(page):
    videos = []
    if int(page) == 1:
        url = 'https://www.jiemian.com/video/lists/index_1.html'
        r = get_html(url)
    else:
        url = 'https://www.jiemian.com/video/lists/0_'+str(page)+'.html'
        rr = get_html(url)
        j = json.loads(rr)
        r = j['rst']
    soup = BeautifulSoup(r, 'html.parser')
    li = soup.find_all('div',class_='news-view left card')
    for index in range(len(li)):
        img = li[index].find('img')
        a = li[index].find('h3')
        videoitem = {}
        videoitem['name'] = a.a.text
        videoitem['href'] = a.a['href']
        videoitem['thumb'] = 'http:' + img['src']
        videoitem['info'] = {'plot':a.a.text}
        videos.append(videoitem)
    return videos

def get_jiemian_mp4info(url):
    mp4info = {}
    r = get_html(url)
    soup = BeautifulSoup(r, 'html.parser')

    img = soup.find('video',controls='controls')
    mp4info['img'] = 'http:' + img['poster']

    plot = soup.find('div',class_='article-content')
    mp4info['plot'] = plot.text.strip()
    return mp4info

def get_jiemian_mp4(url):
    r = get_html(url)
    soup = BeautifulSoup(r, 'html.parser')
    mp4 = soup.find('video',controls='controls')
    return mp4['src']

#36kr新闻
def get_36kr_videos(page):
    videos = []
    if int(page) == 1:
        url = 'https://36kr.com/video'
        html = get_html(url)
        str1 = html.find('window.initialState=')
        str2 = html.find('}</script>')
        cut = html[str1+20:str2+1]
        j = json.loads(cut)
        tmp['36krpageCallback'] = j['videoCatalogData']['data']['videoList']['data']['pageCallback']
        vlist = j['videoCatalogData']['data']['videoList']['data']['itemList']
        for index in range(len(vlist)):
            videoitem = {}
            videoitem['name'] = vlist[index]['templateMaterial']['widgetTitle']
            videoitem['href'] = 'https://36kr.com/video/' + str(vlist[index]['templateMaterial']['itemId'])
            videoitem['thumb'] = vlist[index]['templateMaterial']['widgetImage']
            videoitem['info'] = {'plot':vlist[index]['templateMaterial']['widgetTitle'] + '\n' + vlist[index]['templateMaterial']['summary']}
            videos.append(videoitem)
    else:
        pageCallback = tmp['36krpageCallback']
        url = 'https://gateway.36kr.com/api/mis/nav/video/flow'
        d = {'timestamp':int(time.time()*100),'partner_id':'web','param':{'pageSize': 20, 'pageEvent': 1,'platformId':2,'siteId':1,'pageCallback':pageCallback.encode('utf-8')}}
        #d = str(d)
        krhead = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
                 'content-length':'260',
                 'content-type': 'application/json',
                 'origin':'https://36kr.com',
                 'referer':'https://36kr.com/video'}
        html = requests.post(url,headers=krhead,data=json.dumps(d))
        j = json.loads(html.text)
        vlist = j['data']['itemList']
        for index in range(len(vlist)):
            videoitem = {}
            videoitem['name'] = vlist[index]['templateMaterial']['widgetTitle']
            videoitem['href'] = vlist[index]['templateMaterial']['itemId']
            videoitem['thumb'] = vlist[index]['templateMaterial']['widgetImage']
            videoitem['info'] = {'plot':vlist[index]['templateMaterial']['widgetTitle'] + '\n' + vlist[index]['templateMaterial']['summary']}
            videos.append(videoitem)
    
    
    return videos

def get_36kr_mp4info(url):
    mp4info = {}
    html = get_html(url)
    str1 = html.find('window.initialState=')
    str2 = html.find('}</script>')
    cut = html[str1+20:str2+1]
    j = json.loads(cut)
    m = j['videoDetail']['data']
    mp4info['img'] = m['widgetImage']
    mp4info['aired'] = unix_to_data(str(m['publishTime'])[:-3],'%Y-%m-%d')
    mp4info['cast'] = [(m['authorName'],m['authorSummary'])]
    mp4info['plot'] = m['widgetContent']
    return mp4info

def get_36kr_mp4(url):
    r = get_html(url)
    soup = BeautifulSoup(r, 'html.parser')
    mp4 = soup.find('video')
    return mp4['src']

#环球网
def get_huanqiu_videos(page):
    #爬视频列表的
    videos = []
    page = 10*(int(page)-1)
    url='https://v.huanqiu.com/api/list?node=%22/e3pmh2fmu/e3pmh2g69%22,%22/e3pmh2fmu/e3pn61vrg%22,%22/e3pmh2fmu/e3prkldqd%22,%22/e3pmh2fmu/e3prvucof%22,%22/e3pmh2fmu/e3ptgqp01%22,%22/e3pmh2fmu/e3ptgqp01/e3ptrminr%22&offset='+str(page)+'&limit=20'

    r = get_html(url)
    j = json.loads(r)
    
    vlist = j['list']
    for index in range(len(vlist)-1):
        videoitem = {}
        videoitem['name'] =  vlist[index]['title']
        videoitem['href'] =  'https://v.huanqiu.com/article/' + str(vlist[index]['aid'])
        videoitem['thumb'] = vlist[index]['cover']
        videoitem['info'] = {'plot':vlist[index]['title'] + u'\n\n来自' + vlist[index]['source']['name'] + '\n' +unix_to_data(str(vlist[index]['ctime'])[:-3],'%Y-%m-%d %H:%M:%S')}
        videos.append(videoitem)

    return videos

def get_huanqiu_mp4info(url):
    
    r = get_html(url)
    soup = BeautifulSoup(r, "html5lib")
    mp4info = {}
    mp4 = soup.find('video')
    mp4info['img'] = mp4['data-cover']
    plot = soup.find('div',class_='metadata-info')
    mp4info['plot'] = plot.text
    return mp4info

def get_huanqiu_mp4(url):
    videos = []
    r = get_html(url)
    soup = BeautifulSoup(r, "html5lib")
    mp4 = soup.find('video')
    return mp4['src']

@plugin.route('/play/<name>/<url>/<mode>/')
def play(name,url,mode):
    items = []
    mp4 = get_mp4_mode(url,mode)
    mp4info = get_mp4info_mode(url,mode)
    mp4info['mediatype'] = 'video'
    mp4info['title'] = name
    item = {'label': name,'path':mp4,'is_playable': True,'info':mp4info,'info_type':'video','thumbnail': mp4info['img'],'icon': mp4info['img']}
    items.append(item)
    return items


@plugin.route('/category/<page>/<mode>/')
def category(page,mode):
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', url)
    
    videos = get_videos_mode(page,mode)
    
    items = []
    for video in videos:
        if 'blacklist' not in storage or chushihua('blacklistswitch',0) != '开':
            items.append({'label': check_filter(video['name'].encode('utf-8')),
                'path': plugin.url_for('play', name=check_filter(video['name'].encode('utf-8')),url=video['href'], mode=mode),
	            'thumbnail': video['thumb'],
                'icon': video['thumb'],
                'info':video['info']})
        else:
            if if_filter(video['name'].encode('utf-8')) == False:
                items.append({'label': check_filter(video['name'].encode('utf-8')),
                    'path': plugin.url_for('play', check_filter(video['name'].encode('utf-8')),url=video['href'], mode=mode),
	                'thumbnail': video['thumb'],
                    'icon': video['thumb'],
                    'info':video['info']})

    if mode != 'qyer':
        items.append({
            'label': u'下一页',
            'path': plugin.url_for('category', page=str(int(page)+1),mode=mode),
        })
    return items


@plugin.route('/')
def index():
    if 'homesort' in storage:
        #用户设置的列表
        nlist = []
        for index in range(len(storage['homesort'])):
            nlist.append(storage['homesort'][index]['link'])
        nlist = set(nlist)
        #默认列表
        glist = []
        for index in range(len(get_categories())):
            glist.append(get_categories()[index]['link'])
        glist = set(glist)
        if nlist != glist:
            if len(glist)-len(nlist) > 0:
                h = '新增 '+str(len(glist)-len(nlist))
            else:
                h = '删减 '+str(abs(len(glist)-len(nlist)))
            newhomesort = []
            for index in range(len(get_categories())):
                vlist = {}
                vlist['id'] = get_categories()[index]['id']
                vlist['name'] = get_categories()[index]['name']
                vlist['link'] = get_categories()[index]['link']
                for i in range(len(storage['homesort'])):
                    if storage['homesort'][i]['link'] == get_categories()[index]['link']:
                        vlist['id'] = storage['homesort'][i]['id']
                        vlist['name'] = storage['homesort'][i]['name']
                        vlist['link'] = storage['homesort'][i]['link']
                newhomesort.append(vlist)
            storage['homesort'] = newhomesort
            categories = sorted(newhomesort,key=lambda k:k.get('id'))
            dialog = xbmcgui.Dialog()
            dialog.notification('首页已更新', h +'个网站', xbmcgui.NOTIFICATION_INFO, 5000)
        else:
            categories = sorted(storage['homesort'],key=lambda k:k.get('id'))
    else:
        storage['homesort'] = get_categories()
        categories = sorted(get_categories(),key=lambda k:k.get('id'))

    items = []
    for category in categories:
        if category['id'] != 0:
            items.append({
            'label': category['name'],
            'path': plugin.url_for('category', page=1,mode=category['link']),
            })
    items.append({
        'label': u'[COLOR yellow]设置[/COLOR]',
        'path': plugin.url_for('setting'),
    })
    
    return items

@plugin.route('/setting')
def setting():
    items = []
    items.append({
        'label': u'首页排序与屏蔽',
        'path': plugin.url_for('homesort'),
    })
    items.append({
        'label': u'关键词过滤 - 符合关键词的文字被替换成*，但是视频仍然显示在视频列表',
        'path': plugin.url_for('keyword',key='keyword',name='关键词过滤'),
    })
    items.append({
        'label': u'黑名单屏蔽 - 符合关键词的内容将不显示在视频列表中',
        'path': plugin.url_for('keyword',key='blacklist',name='黑名单屏蔽'),
    })
    return items

@plugin.route('/homesort')
def homesort():
    items = []
    if 'homesort' in storage:
        hlist = sorted(storage['homesort'],key=lambda k:k.get('id'))
        for index in range(len(hlist)):
            items.append({
                'label':'id:' + str(hlist[index]['id']) + ' - ' + hlist[index]['name'],
                'path':plugin.url_for('homeedit',value=hlist[index]['link']),
            })
    else:
        hhlist = get_categories()
        hlist = sorted(hhlist,key=lambda k:k.get('id'))
        for index in range(len(hlist)):
            items.append({
                'label':'id:' + str(hlist[index]['id']) + ' - ' + hlist[index]['name'],
                'path':plugin.url_for('homeedit',value=hlist[index]['link']),
            })
        storage['homesort'] = hlist
    return items

@plugin.route('/homeedit/<value>/')
def homeedit(value):
    hlist = storage['homesort']
    for index in range(len(hlist)):
        if hlist[index]['link'] == value:
            dialog = xbmcgui.Dialog()
            d = dialog.input('--------修改id--------\nid从小到大排列，改为0不显示', defaultt=str(hlist[index]['id']),type=xbmcgui.INPUT_NUMERIC)
            if d != '' and int(d) != int(hlist[index]['id']):
                hlist[index]['id'] = int(d)
                dialog.notification('提示', '修改成功', xbmcgui.NOTIFICATION_INFO, 5000)



@plugin.route('/keyword/<key>/<name>')
def keyword(key,name):
    items = []
    items.append({
        'label': '[COLOR yellow]新增'+name+'[/COLOR]',
        'path': plugin.url_for('keywordxad',key=key,value='/null/',mode=3),
    })
    items.append({
        'label': '[COLOR yellow]' + name + ' (状态:'+chushihua(key+'switch',0) +')[/COLOR]',
        'path': plugin.url_for('switch',key=key+'switch'),
    })
    #storage['keyword'] = ['fuck','getout']
    if key in storage:
        ky = storage[key]
    else:
        ky = ['示例1','helloworld']
        storage[key] = ky
    
    for index in range(len(ky)):
        items.append({
            'label': ky[index],
            'path': plugin.url_for('keywordxad',key=key,value=ky[index],mode=0),
        })
    return items

@plugin.route('/keywordxad/<key>/<value>/<mode>/')
def keywordxad(key,value,mode):
    if int(mode) == 0:
        items = []
        items.append({
            'label': '修改 - ' +str(value),
            'path': plugin.url_for('keywordxad',key=key,value=value,mode=1),
        })
        items.append({
            'label': '删除 - ' +str(value),
            'path': plugin.url_for('keywordxad',key=key,value=value,mode=2),
        })
        return items
    #修改
    if int(mode) == 1:
        dialog = xbmcgui.Dialog()
        d = dialog.input('修改 '+ value, defaultt=value,type=xbmcgui.INPUT_ALPHANUM)
        ky = storage[key]
        if d != '':
            if d != value:
                ky.remove(value)
                ky.append(d)

                storage[key] = list(set(ky))
                dialog.notification('提示', '修改成功', xbmcgui.NOTIFICATION_INFO, 5000)
            
            
    #删除
    if int(mode) == 2:
        dialog = xbmcgui.Dialog()
        ret = dialog.yesno('确认删除吗？', '删除：' + value)
        if ret:
            ky = storage[key]
            ky.remove(value)
            storage[key] = list(set(ky))
            dialog = xbmcgui.Dialog()
            dialog.notification('提示', '删除成功', xbmcgui.NOTIFICATION_INFO, 5000)
    #新增
    if int(mode) == 3:
        dialog = xbmcgui.Dialog()
        d = dialog.input('新增关键词，多个请用英文逗号隔开',type=xbmcgui.INPUT_ALPHANUM)
        ky = storage[key]
        if d != '':
            if d.find(',') != -1:
                k = d.split(',')
                ky = k + ky
            else:
                ky.append(d)
            storage[key] = list(set(ky))
            dialog.notification('提示', '添加成功', xbmcgui.NOTIFICATION_INFO, 5000)


@plugin.route('/switch/<key>/')
def switch(key):
    if storage[key] == 1:
        storage[key] = 0
        dialog = xbmcgui.Dialog()
        dialog.notification('提示', '已关闭', xbmcgui.NOTIFICATION_INFO, 5000)
    else:
        storage[key] = 1
        dialog = xbmcgui.Dialog()
        dialog.notification('提示', '已开启', xbmcgui.NOTIFICATION_INFO, 5000)

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
