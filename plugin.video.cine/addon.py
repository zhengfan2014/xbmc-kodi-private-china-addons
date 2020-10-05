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
import urllib
import xml.etree.ElementTree as ET
import difflib

from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
 
from urllib import unquote

def diff_float(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()

def urldecode(fname):
    fname = unquote(fname.encode('utf-8'))
    fname = unicode(fname.decode('utf-8'))
    return fname
# def unescape(string):
#     string = urllib2.unquote(string).decode('utf8')
#     quoted = HTMLParser.HTMLParser().unescape(string).encode('utf-8')
#     #转成中文
#     return re.sub(r'%u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})', lambda m: unichr(int(m.group(1), 16)), quoted)


plugin = Plugin()


macheaders = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4 Supplemental Update) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15'}
ipadheaders = {'user-agent': 'Mozilla/5.0 (iPad; CPU OS 10_15_4 Supplemental Update like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Mobile/15E148 Safari/605.1.15'}
iphoneheaders = {'user-agent': 'Mozilla/5.0 (iPhone; CPU OS 10_15_4 Supplemental Update like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Mobile/14E304 Safari/605.1.15'}
mheaders = {'user-agent':'Mozilla/5.0 (Linux; Android 10; Z832 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Mobile Safari/537.36'}
headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
tmp = plugin.get_storage('tmp')

#用户设置存储
storage = plugin.get_storage('storage')
#搜索历史纪录
his = plugin.get_storage('his')


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

@plugin.cached(TTL=2)
def get_html(url,ua='pc',cf='',mode='html',encode='utf-8'):
    #UA相关
    if ua == 'pc':
        head = headers
    if ua == 'mobile':
        head = mheaders
    if ua == 'iphone':
        head = iphoneheaders
    if ua == 'ipad':
        head = ipadheaders
    if ua == 'mac':
        head = macheaders
    
    #超时重试3次
    s0 = requests.Session()
    s0.mount('http://', HTTPAdapter(max_retries=3))
    s0.mount('https://', HTTPAdapter(max_retries=3))

    #获取网页源代码
    if mode == 'html':
        #cloudflare相关
        if cf == '':
            r = s0.get(url,headers=head)
        else:
            scraper = cfscrape.create_scraper()
            s = scraper.get_tokens(url,headers=head)
            r = s0.get(url,headers=head,cookies=s[0])
        #编码相关
        if encode == 'utf-8':
            r.encoding = 'utf-8'
        if encode == 'gbk':
            r.encoding = 'gbk'
        html = r.text
    
    #用于获取302跳转网页的真实url
    if mode == 'url':
        #cloudflare相关
        if cf == '':
            r = s0.get(url,headers=head,timeout=5,stream=True)
        else:
            scraper = cfscrape.create_scraper()
            s = scraper.get_tokens(url,headers=head)
            r = s0.get(url,headers=head,cookies=s[0],timeout=5,stream=True)
        
        html = r.url
        
    return html

@plugin.cached(TTL=2)
def post_html(url,data='',ua='pc',cf='',mode='html',encode='utf-8',jsons=''):
    if data != '':
        data =eval(data)
    if jsons != '':
        jsons =eval(jsons)

    #UA相关
    if ua == 'pc':
        head = headers
    if ua == 'mobile':
        head = mheaders
    if ua == 'iphone':
        head = iphoneheaders
    if ua == 'ipad':
        head = ipadheaders
    if ua == 'mac':
        head = macheaders

    #超时重试3次
    s0 = requests.Session()
    s0.mount('http://', HTTPAdapter(max_retries=3))
    s0.mount('https://', HTTPAdapter(max_retries=3))

    #cloudflare相关
    if data != '' or jsons != '':
        if cf == '':
            if data != '':
                r = s0.post(url,headers=head,data=data)
            if jsons != '':
                r = s0.post(url,headers=head,json=jsons)

            if encode == 'utf-8':
                r.encoding = 'utf-8'
            if encode == 'gbk':
                r.encoding = 'gbk'
            html = r.text

            if mode == 'url':
                html = r.url
            else:
                html = r.text
        else:
            scraper = cfscrape.create_scraper()
            s = scraper.get_tokens(url,headers=head)
            if data != '':
                r = s0.post(url,data=data,headers=head,cookies=s[0])
            if jsons != '':
                r = s0.post(url,json=jsons,headers=head,cookies=s[0])

            if encode == 'utf-8':
                r.encoding = 'utf-8'
            if encode == 'gbk':
                r.encoding = 'gbk'

            if mode == 'url':
                html = r.url
            else:
                html = r.text
        return html

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

def tiqu_num(string):
    try:
        a = re.search('\d+',string).group()
        return a
    except AttributeError:
        return ''

def get_categories_mode(mode):
    item = eval('get_' + mode + '_categories')()
    return item
def get_videos_mode(url,mode,page):
    item = eval('get_' + mode + '_videos')(url,int(page))
    return item
def get_source_mode(url,mode):
    item = eval('get_' + mode + '_source')(url)
    return item
def get_mp4info_mode(url,mode):
    item = eval('get_' + mode + '_mp4info')(url)
    return item
def get_mp4_mode(url,mode):
    item = eval('get_' + mode + '_mp4')(url)
    return item
def get_search_mode(keyword,page,mode):
    item = eval('get_' + mode + '_search')(keyword,int(page))
    return item

##########################################################
###主入口
##########################################################

def get_categories():
    return [{'id':1,'name':'喜欢看影视(138vcd.com)','link':'138vcd','author':'zhengfan2014','upload':'2020-5-7','videos':48,'search':36},
            {'id':2,'name':'片库(pianku.tv)','link':'pianku','author':'zhengfan2014','upload':'2020-5-7','videos':42,'search':10},
            {'id':3,'name':'老豆瓣(laodouban.com)','link':'laodouban','author':'zhengfan2014','upload':'2020-5-7','videos':12,'search':10},
            {'id':4,'name':'美剧天堂(meijutt.tv)','link':'meijutt','author':'zhengfan2014','upload':'2020-5-23','videos':20,'search':20},
            {'id':5,'name':'豆瓣电影资源(douban777.com)','link':'douban777','author':'zhengfan2014','upload':'2020-6-10','videos':20},
            {'id':6,'name':'快影资源(kyzy.tv)','link':'kyzy','author':'zhengfan2014','upload':'2020-6-10','videos':20},
            {'id':7,'name':'卧龙资源(wlzy.tv)','link':'wlzy','author':'zhengfan2014','upload':'2020-6-10','videos':25},
            {'id':8,'name':'OK资源(okzyw.com)','link':'okzy','author':'zhengfan2014','upload':'2020-6-11','videos':30},
            {'id':9,'name':'麻花资源(mahuazy.net)','link':'mahuazy','author':'zhengfan2014','upload':'2020-6-12','videos':20},
            {'id':10,'name':'最大资源(zuidazy3.net)','link':'zdziyuan','author':'zhengfan2014','upload':'2020-6-12','videos':40},
            {'id':11,'name':'采集资源(caijizy.vip)','link':'caijizy','author':'zhengfan2014','upload':'2020-6-12','videos':35},
            {'id':12,'name':'哈酷资源(666zy.com)','link':'666zy','author':'zhengfan2014','upload':'2020-6-12','videos':20},
            {'id':13,'name':'kuku(pan.kuku.me)','link':'kukume','author':'zhengfan2014','upload':'2020-9-26'},
            {'id':14,'name':'Share With You(ty.let-me-try.com)','link':'letmetry','author':'zhengfan2014','upload':'2020-9-26'},
            {'id':15,'name':'goindex测试','link':'ddosi','author':'zhengfan2014','upload':'2020-9-26'},
            {'id':16,'name':'goindex多盘版测试','link':'yanzai','author':'zhengfan2014','upload':'2020-9-26'},
            {'id':17,'name':'goindex多盘版acrou','link':'acrou','author':'zhengfan2014','upload':'2020-9-26'}]

##########################################################
###以下是模块，网站模块请粘贴在这里面
##########################################################

#138vcd
def get_138vcd_categories():
    return [{"name": "动作片", "link": "https://www.138vcd.com/index.php/vod/show/id/26"},
          {"name": "喜剧片", "link": "https://www.138vcd.com/index.php/vod/show/id/27"}, 
          {"name": "爱情片", "link": "https://www.138vcd.com/index.php/vod/show/id/28"}, 
          {"name": "科幻片", "link": "https://www.138vcd.com/index.php/vod/show/id/29"},
          {"name": "剧情片", "link": "https://www.138vcd.com/index.php/vod/show/id/30"},
          {"name": "战争片", "link": "https://www.138vcd.com/index.php/vod/show/id/31"},
          {"name": "恐怖片", "link": "https://www.138vcd.com/index.php/vod/show/id/36"}]

def get_138vcd_videos(url,page):
    videos = []
    if page == 1:
        r = get_html(url + '.html')
    else:
        r = get_html(url + '/page/' +str(page) +'.html')
    soup = BeautifulSoup(r, "html5lib")
    ul = soup.find('ul',class_='myui-vodlist clearfix')
    alist = ul.find_all('a',class_='myui-vodlist__thumb lazyload')
    for i in range(len(alist)):
        videoitem = {}
        videoitem['name'] =  alist[i]['title'] 
        videoitem['href'] =  'https://www.138vcd.com/' + alist[i]['href']
        videoitem['thumb'] = alist[i]['data-original']
        videos.append(videoitem)
    return videos

def get_138vcd_source(url):
    videos = []
    r = get_html(url)
    soup = BeautifulSoup(r, 'html.parser')
    ul = soup.find('ul',class_='myui-content__list sort-list clearfix')
    alist = ul.find_all('a')
    
    duopdict = {}
    for i in range(len(alist)):
        duopdict[alist[i].text] = 'https://www.138vcd.com' + alist[i]['href']
        
    videoitem = {}
    videoitem['name'] = '播放线路1'
    videoitem['href'] = str(duopdict)
    videos.append(videoitem)
    tmp['bghtml'] = r
    return videos

def get_138vcd_mp4(url):
    r = get_html(url)
    mp4 = re.search('(?<=link_pre\":\"\",\"url\":\").*?(?=\",\"url_next)',r).group()
    mp4 = mp4.replace('\\','')
    return mp4

def get_138vcd_search(keyword,page):
    videos = []
    
    if page == 1:
        r = get_html('https://www.138vcd.com/vodsearch.html?wd='+keyword+'&submit=')
    else:
        r = get_html('https://www.138vcd.com/vodsearch/page/'+str(page)+'/wd/'+keyword+'.html')
    soup = BeautifulSoup(r, "html5lib")
    ul = soup.find('ul',id='searchList')
    alist = ul.find_all('a',class_='myui-vodlist__thumb img-lg-150 img-md-150 img-sm-150 img-xs-100 lazyload')
    for i in range(len(alist)):
        videoitem = {}
        videoitem['name'] =  alist[i]['title'] 
        videoitem['href'] =  'https://www.138vcd.com/' + alist[i]['href']
        videoitem['thumb'] = alist[i]['data-original']
        videos.append(videoitem)
    return videos

#pianku
def get_pianku_categories():
    return [{"name": "电影", "link": "https://www.pianku.tv/mv/-----1-"},
          {"name": "剧集", "link": "https://www.pianku.tv/tv/-----1-"}, 
          {"name": "动漫", "link": "https://www.pianku.tv/ac/-----1-"}]

def get_pianku_videos(url,page):
    videos = []
    if page == 1:
        r = get_html(url + '1.html')
    else:
        r = get_html(url + str(page) +'.html')
    soup = BeautifulSoup(r, "html5lib")
    ul = soup.find('ul',class_='content-list')
    ilist = ul.find_all('div',class_='li-img')
    for i in range(len(ilist)):
        videoitem = {}
        videoitem['name'] =  ilist[i].a['title'] 
        videoitem['href'] =  'https://www.pianku.tv' + ilist[i].a['href']
        videoitem['thumb'] = ilist[i].a.img['src']
        videos.append(videoitem)
    return videos

def get_pianku_source(url):
    videos = []
    r1 = get_html(url)
    vtype = re.search('(?<=pianku.tv\/)[a-zA-Z]+(?=\/)',url).group()
    vid = re.search('[a-zA-Z]+(?=.html)',url).group()
    apiurl = 'https://www.pianku.tv/ajax/downurl/'+vid+'_'+vtype+'/'
    r = get_html(apiurl)
    
    soup = BeautifulSoup(r, 'html.parser')
    ul = soup.find('ul',class_='py-tabs')
    # dialog = xbmcgui.Dialog()
    # dialog.textviewer('错误提示', str(r.encode('utf-8')))
    li = ul.find_all('li')
    vlist =soup.find_all('ul',class_='player ckp')
    
    for index in range(len(li)):
        duopname = li[index].text
        alist = vlist[index].find_all('a')
        duopdict = {}
        for i in range(len(alist)):
            duopdict[alist[i].text] = 'https://www.pianku.tv' + alist[i]['href']
        
        videoitem = {}
        videoitem['name'] = duopname
        videoitem['href'] = str(duopdict)
        videos.append(videoitem)
    tmp['bghtml'] = r1
    return videos

def get_pianku_mp4(url):
    r = get_html(url)
    str1 = r.find('new DPlayer({')
    cut = r[str1:]
    mp4 = re.search('https?:..+\.m3u8',cut).group()
    mp4 = mp4.replace('\\','')
    # dialog = xbmcgui.Dialog()
    # ok = dialog.ok('错误提示', mp4)
    return mp4

def get_pianku_search(keyword,page):
    videos = []
    
    if page == 1:
        url = get_html('https://www.pianku.tv/s/go.php?q='+keyword,mode='url')
        tmp['piankusearch'] = url
    else:
        url = tmp['piankusearch'][:-5] + '-' + str(page) + '.html'
    r = get_html(url)

    # dialog = xbmcgui.Dialog()
    # dialog.textviewer('错误提示', r.encode('utf-8'))
    soup = BeautifulSoup(r, "html5lib")
    ul = soup.find('div',class_='sr_lists')
    vlist = ul.find_all('dl')
    for i in range(len(vlist)):
        img = vlist[i].find('img')
        a = vlist[i].dd.find('a')
        videoitem = {}
        videoitem['name'] =  a.text
        videoitem['href'] =  'https://www.pianku.tv' + a['href']
        videoitem['thumb'] = img['src']
        videos.append(videoitem)
    return videos

#老豆瓣
def get_laodouban_categories():
    return [{"name": "电影", "link": "https://www.laodouban.com/dianying/"},
          {"name": "电视剧", "link": "https://www.laodouban.com/dianshiju/"}, 
          {"name": "动漫", "link": "https://www.laodouban.com/dongman/"},
          {"name": "综艺", "link": "https://www.laodouban.com/zongyi/"}]

def get_laodouban_videos(url,page):
    videos = []
    if page != 1:
        url += str(page)
    r = get_html(url)
    soup = BeautifulSoup(r, "html5lib")
    ul = soup.find('div',class_='tubiao row no-gutters')
    ilist = ul.find_all('div',class_='zu d-flex flex-column col-4 col-sm-3 col-md-3 col-lg-3 col-xl-3 mb-4')
    for i in range(len(ilist)):
        img = ilist[i].find('img')
        a = ilist[i].find('a',class_='text-secondary')
        videoitem = {}
        videoitem['name'] =  a.text
        videoitem['href'] =  'https://www.laodouban.com' + a['href']
        videoitem['thumb'] = img['src']
        videos.append(videoitem)
    return videos

def get_laodouban_source(url):
    videos = []
    if re.match('https?',url):
        r = get_html(url)
        soup = BeautifulSoup(r, 'html.parser')
        ul = soup.find('ul',class_='nav nav-tabs mt-3')
    
        li = ul.find_all('li')
        vlist =soup.find_all('div',class_='tab-pane')
    

        #dialog = xbmcgui.Dialog()
        #dialog.textviewer('错误提示', str(vlist[0].encode('utf-8')))
        for index in range(len(li)):
            duopname = li[index].a.text.strip()
            if li[index].find('span'):
                duopname = duopname[:-1]
                duopname += u' · [COLOR red]' + li[index].span.text + u'[/COLOR]'
            blist = vlist[index].find_all('button')
            duopdict = {}
            for i in range(len(blist)):
                duopdict[blist[i].text.strip()] = 'https://www.laodouban.com/b?h=' + blist[i]['ldb-bianhao'] + '&y=' + blist[i]['ldb-suoyin']
        
            videoitem = {}
            videoitem['name'] = duopname.strip()
            videoitem['href'] = str(duopdict)
            videos.append(videoitem)
        tmp['bghtml'] = r
    else:
        ddict = eval(url)
        for k,i in ddict.items():
            duopname = k
            vlist = eval(i)
            duopdict = {}
            for index in range(len(vlist)):
                duopdict[vlist[index]['biaoji']] = vlist[index]['dizhi']
            videoitem = {}
            videoitem['name'] = duopname
            videoitem['href'] = str(duopdict)
            videos.append(videoitem)
    
    return videos

def get_laodouban_mp4(url):
    if re.search('https?:..+\.m3u8',url):
        mp4 = url
    else:
        r = get_html(url)
        str1 = r.find('var videoObject = {')
        cut = r[str1:]
        mp4 = re.search('https?:..+\.m3u8',cut).group()
        mp4 = mp4.replace('\\','')
    # dialog = xbmcgui.Dialog()
    # ok = dialog.ok('错误提示', mp4)
    return mp4

def get_laodouban_search(keyword,page):
    videos = []
    
    # if page == 1:
    #     url = 'https://www.laodouban.com/s?c=' + keyword
    #     r = get_html(url)
    url = 'https://www.laodouban.com/api/sousuo/'
    data = {'guanjianzi':keyword,'yeshu':page}
    r = post_html(url,str(data))
    j = json.loads(r)
    for index in range(len(j)):
        videoitem = {}
        videoitem['name'] = j[index]['mingcheng']
        videoitem['thumb'] = j[index]['jietu']
        videoitem['href'] = str({j[index]['bofangdizhi']['mingcheng']:str(j[index]['bofangdizhi']['dizhizu'])})
        videos.append(videoitem)
    # # dialog = xbmcgui.Dialog()
    # # dialog.textviewer('错误提示', r.encode('utf-8'))
    # soup = BeautifulSoup(r, "html5lib")
    # ul = soup.find('div',class_='zuoce col-12 col-sm-12 col-md-12 col-lg-8 col-xl-8')
    # li1 = ul.find('div',class_='tuwenbiao row no-gutters mb-4')


    # vlist1 = li1.find_all('div',class_='col-12 d-flex pt-3 pb-4')
    # for i in range(len(vlist1)):
    #     img = vlist1[i].find('img')
    #     a = vlist1[i].find('a',class_='text-info')
    #     videoitem = {}
    #     videoitem['name'] =  a.text
    #     videoitem['href'] =  'https://www.laodouban.com' + a['href']
    #     videoitem['thumb'] = img['src']
    #     videos.append(videoitem)
    return videos

#美剧天堂
def get_meijutt_categories():
    return [{"name": "魔幻/科幻", "link": "https://www.meijutt.tv/file/list1"},
          {"name": "灵异/惊悚", "link": "https://www.meijutt.tv/file/list2"}, 
          {"name": "都市/情感", "link": "https://www.meijutt.tv/file/list3"},
          {"name": "犯罪/历史", "link": "https://www.meijutt.tv/file/list4"},
          {"name": "选秀/综艺", "link": "https://www.meijutt.tv/file/list5"},
          {"name": "动漫/卡通", "link": "https://www.meijutt.tv/file/list6"}]

def get_meijutt_videos(url,page):
    videos = []
    if page != 1:
        url += '_' + str(page) + '.html'
    else:
        url += '.html'
    r = get_html(url,encode='gbk')
    soup = BeautifulSoup(r, "html5lib")
    ilist = soup.find_all('div',class_='cn_box2')
    for i in range(len(ilist)):
        img = ilist[i].find('img')
        a = ilist[i].find('a')
        videoitem = {}
        videoitem['name'] =  a['title']
        videoitem['href'] =  'https://www.meijutt.tv' + a['href']
        videoitem['thumb'] = img['src']
        videos.append(videoitem)
    return videos

def get_meijutt_source(url):
    videos = []
    vid = re.search('[0-9]+(?=.html)',url).group()
    r = get_html(url,encode='gbk')
    r1 = get_html('https://www.meijutt.tv/video/'+str(vid)+'-0-0.html',encode='gbk')
    jsurl = re.search('/playdata/[0-9]+/[0-9]+.js',r1).group()
    r2 = get_html('https://www.meijutt.tv' + jsurl )
    str1 = r2.find('var VideoListJson=')
    str2 = r2.find(',urlinfo=')
    cutjson = r2[str1+18:str2]
    j = json.loads(cutjson)
    

    for index in range(len(j)):
        if j[index][0] != u'百度网盘' and j[index][0] != u'西瓜影音':
            duopname = j[index][0]
            duopdict = {}
            for i in range(len(j[index][1])):
                duopdict[j[index][1][i][0]] = j[index][1][i][1]
            videoitem = {}
            videoitem['name'] = duopname
            videoitem['href'] = str(duopdict)
            videos.append(videoitem)
    tmp['bghtml'] = r
    return videos

def get_meijutt_mp4(url):
    if re.search('m3u8',url):
        if re.search('9m3u8',url):
            url = url.replace('9m3u8','m3u8')
    else:
        url = url[:-5] + url[-4:]
        
        domain = re.search('(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})',url).group()
        r = get_html(url)
        url = domain + re.search('(?<=\")[\S]+.m3u8\?sign\=[a-z0-9]+',r).group()
        # dialog = xbmcgui.Dialog()
        # dialog.textviewer('错误提示', domain)
    return url

def get_meijutt_search(keyword,page):
    videos = []
    if page == 1:
        url = 'https://www.meijutt.tv/search/index.asp'
        data = {'searchword':keyword.decode('utf-8').encode('gbk')}
        r = post_html(url,data=str(data),encode='gbk')
    else:
        url = 'https://www.meijutt.tv/search/index.asp?page='+str(page)+'&searchword='+(urllib.quote(keyword.decode('utf-8').encode('gbk')).encode('utf-8'))+'&searchtype=-1'
        r = get_html(url,encode='gbk')
    soup = BeautifulSoup(r, "html5lib")
    ilist = soup.find_all('div',class_='cn_box2')
    for i in range(len(ilist)):
        img = ilist[i].find('img')
        a = ilist[i].find('a')
        videoitem = {}
        videoitem['name'] =  a['title']
        videoitem['href'] =  'https://www.meijutt.tv' + a['href']
        videoitem['thumb'] = img['src']
        videos.append(videoitem)
    return videos

#豆瓣资源
def get_douban777_categories():
    return get_maccms_xml('http://v.1988cj.com/inc/dbm3u8.php',banid='1,2')

def get_douban777_videos(url,page):
    return get_maccms_xml('http://v.1988cj.com/inc/dbm3u8.php',url=url,page=page)

def get_douban777_source(url):
    return get_maccms_xml('http://v.1988cj.com/inc/dbm3u8.php',url=url)

def get_douban777_mp4info(url):
    return get_maccms_xml('http://v.1988cj.com/inc/dbm3u8.php',url=url,keyword='douban777')

def get_douban777_mp4(url):
    if url[:5] == 'https':
        url = 'http' + url[5:]
    return url

# def get_douban777_search(keyword,page):
#     return get_maccms_xml('http://v.1988cj.com/inc/dbm3u8.php',keyword=keyword,page=page)


#快影资源
def get_kyzy_categories():
    return get_maccms_json('https://www.kyzy.tv/api.php/kym3u8/vod/',banid='1,2,20')

def get_kyzy_videos(url,page):
    return get_maccms_json('https://www.kyzy.tv/api.php/kym3u8/vod/',url=url,page=page)

def get_kyzy_source(url):
    return get_maccms_json('https://www.kyzy.tv/api.php/kym3u8/vod/',url=url)

def get_kyzy_mp4info(url):
    return get_maccms_json('https://www.kyzy.tv/api.php/kym3u8/vod/',url=url,keyword='douban777')

def get_kyzy_mp4(url):
    return url

def get_kyzy_search(keyword,page):
    return get_maccms_json('https://www.kyzy.tv/api.php/kym3u8/vod/',keyword=keyword,page=page)

#卧龙资源
def get_wlzy_categories():
    return get_maccms_xml('http://cj.wlzy.tv/inc/api_mac_m3u8.php',banid='2,26,30,31')

def get_wlzy_videos(url,page):
    return get_maccms_xml('http://cj.wlzy.tv/inc/api_mac_m3u8.php',url=url,page=page)

def get_wlzy_source(url):
    return get_maccms_xml('http://cj.wlzy.tv/inc/api_mac_m3u8.php',url=url)

def get_wlzy_mp4info(url):
    return get_maccms_xml('http://cj.wlzy.tv/inc/api_mac_m3u8.php',url=url,keyword='douban777')

def get_wlzy_mp4(url):
    return url

# def get_wlzy_search(keyword,page):
#     return get_maccms_xml('http://cj.wlzy.tv/inc/api_mac_m3u8.php',keyword=keyword,page=page)

#ok资源
def get_okzy_categories():
    return get_maccms_xml('http://cj.okzy.tv/inc/apickm3u8s.php',banid='1,2,3,4,20,33')

def get_okzy_videos(url,page):
    return get_maccms_xml('http://cj.okzy.tv/inc/apickm3u8s.php',url=url,page=page)

def get_okzy_source(url):
    return get_maccms_xml('http://cj.okzy.tv/inc/apickm3u8s.php',url=url)

def get_okzy_mp4info(url):
    return get_maccms_xml('http://cj.okzy.tv/inc/apickm3u8s.php',url=url,keyword='douban777')

def get_okzy_mp4(url):
    return url

# def get_okzy_search(keyword,page):
#     return get_maccms_xml('http://cj.okzy.tv/inc/apickm3u8s.php',keyword=keyword,page=page)

#麻花资源
def get_mahuazy_categories():
    return get_maccms_xml('https://www.mhapi123.com/inc/api.php',banid='1,2,4,49,42,44,46,38,54')

def get_mahuazy_videos(url,page):
    return get_maccms_xml('https://www.mhapi123.com/inc/api.php',url=url,page=page)

def get_mahuazy_source(url):
    return get_maccms_xml('https://www.mhapi123.com/inc/api.php',url=url)

def get_mahuazy_mp4info(url):
    return get_maccms_xml('https://www.mhapi123.com/inc/api.php',url=url,keyword='douban777')

def get_mahuazy_mp4(url):
    return url

# def get_mahuazy_search(keyword,page):
#     return get_maccms_xml('https://www.mhapi123.com/inc/api.php',keyword=keyword,page=page)

#最大资源
def get_zdziyuan_categories():
    return get_maccms_xml('http://www.zdziyuan.com/inc/api_zuidam3u8.php',banid='1,2')

def get_zdziyuan_videos(url,page):
    return get_maccms_xml('http://www.zdziyuan.com/inc/api_zuidam3u8.php',url=url,page=page)

def get_zdziyuan_source(url):
    return get_maccms_xml('http://www.zdziyuan.com/inc/api_zuidam3u8.php',url=url)

def get_zdziyuan_mp4info(url):
    return get_maccms_xml('http://www.zdziyuan.com/inc/api_zuidam3u8.php',url=url,keyword='douban777')

def get_zdziyuan_mp4(url):
    return url

#采集资源
def get_caijizy_categories():
    return get_maccms_xml('http://ts.caijizy.vip/api.php/provide/vod/at/xml/',banid='1,2,27')

def get_caijizy_videos(url,page):
    return get_maccms_xml('http://ts.caijizy.vip/api.php/provide/vod/at/xml/',url=url,page=page)

def get_caijizy_source(url):
    return get_maccms_xml('http://ts.caijizy.vip/api.php/provide/vod/at/xml/',url=url)

def get_caijizy_mp4info(url):
    return get_maccms_xml('http://ts.caijizy.vip/api.php/provide/vod/at/xml/',url=url,keyword='douban777')

def get_caijizy_mp4(url):
    return url

#哈酷资源
def get_666zy_categories():
    return get_maccms_xml('http://api.666zy.com/inc/hkm3u8.php',banid='1,2,27,36')

def get_666zy_videos(url,page):
    return get_maccms_xml('http://api.666zy.com/inc/hkm3u8.php',url=url,page=page)

def get_666zy_source(url):
    return get_maccms_xml('http://api.666zy.com/inc/hkm3u8.php',url=url)

def get_666zy_mp4info(url):
    return get_maccms_xml('http://api.666zy.com/inc/hkm3u8.php',url=url,keyword='douban777')

def get_666zy_mp4(url):
    return url


def get_kukume_categories():
    return get_sharelist('https://pan.kuku.me/')

def get_letmetry_categories():
    return get_sharelist('https://ty.let-me-try.com/')

def get_ddosi_categories():
    return get_goindex('https://w.ddosi.workers.dev/')

def get_yanzai_categories():
    return get_yanzaigoindex('https://yanzai-goindex.java.workers.dev/')
def get_acrou_categories():
    return get_yanzaigoindex('https://oss.achirou.workers.dev/')
########################################################################################################################################
########################################################################################################################################
###以下是核心代码区，看不懂的请勿修改
########################################################################################################################################
########################################################################################################################################

@plugin.route('/play/<name>/<url>/<mode>/')
def play(name,url,mode):
    items = []
    mp4 = get_mp4_mode(url,mode)
    if re.search('https?',url):
        mp4 += u'|referer=' + url
    try:
        mp4info = get_mp4info_mode(url,mode)
        mp4info['mediatype'] = 'video'
        mp4info['title'] = name
        
        item = {'label': name,'path':mp4,'is_playable': True,'info':mp4info,'info_type':'video','thumbnail': tmp['bgimg'],'icon': tmp['bgimg']}
    except NameError:
        item = {'label': name,'path':mp4,'is_playable': True,'info_type':'video','thumbnail': tmp['bgimg'],'icon': tmp['bgimg']}
    dialog = xbmcgui.Dialog()
    dialog.notification('亲，请勿轻信视频内非法广告！','天上不会掉馅饼，世上没有免费的午餐',xbmcgui.NOTIFICATION_INFO, 5000)
    items.append(item)
    return items

#判断是否含数字
def hannum(x):
    if re.search('\d+',x):
        return True
    else:
        return False

#求差集，在B中但不在A中
def diff(listA,listB):
    retD = list(set(listB).difference(set(listA)))
    return retD

@plugin.route('/duop/<name>/<list>/<mode>/')
def duop(name,list,mode):
    list = eval(list)
    sslist = sorted(list)
    slist = filter(hannum,sslist)
    slist = sorted(slist,key=lambda x:int(re.search('\d+',x).group()),reverse = True)
    slist = slist + diff(slist,sslist)
    
    kongge = ' - '
    kongge = kongge.encode('utf-8')
    items = []
    for index in range(len(slist)):
        item = {'label':slist[index].encode('utf-8'),'path':plugin.url_for('play',name=slist[index].encode('utf-8')+ kongge +name,url= list[slist[index]],mode=mode)}
        items.append(item)
    return items

@plugin.route('/source/<name>/<url>/<img>/<mode>/')
def source(name,url,img,mode):
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', url)
    sources = get_source_mode(url,mode)
    tmp['bgimg'] = img
    items = [{
        'label': s['name'],
        'path': plugin.url_for('duop', name=name,list=s['href'],mode=mode),
    } for s in sources]

    sorted_items = items
    #sorted_items = sorted(items, key=lambda item: item['label'])
    return sorted_items

@plugin.route('/category/<name>/<url>/<mode>/<page>/')
def category(name,url,mode,page):
    videos = get_videos_mode(url,mode,page)
    items = []
    if videos != []:
        if 'info' in videos[0]:
            for video in videos:
                info = video['info']
                info['mediatype'] = 'video'
                items.append({'label': video['name'],
                'path': plugin.url_for('source', name=video['name'].encode('utf-8'),url=video['href'],img=video['thumb'], mode=mode),
    	    'thumbnail': video['thumb'],
                'icon': video['thumb'],
                'info': info,
            })
        else:
            for video in videos:
                items.append({'label': video['name'],
                'path': plugin.url_for('source', name=video['name'].encode('utf-8'),url=video['href'],img=video['thumb'], mode=mode),
    	    'thumbnail': video['thumb'],
                'icon': video['thumb'],
            })

    categories = get_categories()
    for index in range(len(categories)):
        if mode == categories[index]['link']:
            if 'videos' in categories[index]:
                if int(categories[index]['videos']) == len(videos):
                    items.append({
                        'label': '[COLOR yellow]下一页[/COLOR]',
                        'path': plugin.url_for('category',name=name,url=url,mode=mode,page=int(int(page)+1)),
                    })
    return items


@plugin.route('/home/<mode>/')
def home(mode):
    categories = get_categories_mode(mode)
    if categories[0]['name'] == 'mode':
        items = []
        netdiskmod = categories[0]['link']
        del categories[0]
        pnum = 0
        allnum = len(categories)
        pDialog = xbmcgui.DialogProgress()
        pDialog.create('解析网盘文件下载地址', '准备开始发送请求...')
            
        for category in categories:
            
            if re.match('[^/]+\.[a-zA-Z0-9]{1,4}',urldecode(category['name'])):
                #解析文件
                pDialog.update(int(float(pnum)/float(allnum)*100), '解析网盘文件地址：解析文件地址中...  [' + str(pnum+1) + '/' + str(allnum) + ']')
                r = requests.get(category['link'], stream=True,headers=headers)
                items.append({'label': category['name'],'path': r.url,'is_playable':True})
            else:
                #判断是否文件夹，是继续循环调用
                pDialog.update(int(float(pnum)/float(allnum)*100), '解析网盘文件地址：判断为文件夹,跳过...  [' + str(pnum+1) + '/' + str(allnum) + ']')
                items.append({'label': category['name'],
                'path': plugin.url_for('onetogo', name=category['name'].encode('utf-8'), url=category['link'].encode('utf-8'),mode=netdiskmod,page=1),
                })
            pnum += 1
    else:
        items = [{
            'label': category['name'],
            'path': plugin.url_for('category', name=category['name'] , url=category['link'],mode=mode,page=1),
        } for category in categories]
        try:
            eval('get_' + mode + '_search')
            items.append({
                'label': '[COLOR yellow]搜索[/COLOR]',
                'path': plugin.url_for('history',name='搜索',url='search',mode=mode),
           })
        except NameError:
            pass
    return items

@plugin.route('/onetogo/<name>/<url>/<mode>/<page>/')
def onetogo(name,url,mode,page):
    try:
        categories = eval('get_' + mode)(url)
    
        if categories[0]['name'] == 'mode':
            items = []
            del categories[0]
            pnum = 0
            allnum = len(categories)
            pDialog = xbmcgui.DialogProgress()
            pDialog.create('解析网盘文件下载地址', '准备开始发送请求...')
            
            for category in categories:
            
                if re.match('[^/]+\.[a-zA-Z0-9]{1,4}',urldecode(category['name'])):
                    #解析文件
                    pDialog.update(int(float(pnum)/float(allnum)*100), '解析网盘文件地址：解析文件地址中...  [' + str(pnum+1) + '/' + str(allnum) + ']')

                    # s = requests.Session()
                    # s.mount('http://', HTTPAdapter(max_retries=3))
                    # s.mount('https://', HTTPAdapter(max_retries=3))

                    # try:
                    #     r = s.get(category['link'],timeout=5,stream=True,headers=headers)
                    # except requests.exceptions.RequestException as e:
                    #     dialog = xbmcgui.Dialog()
                    #     dialog.textviewer('错误提示',str(e))
                    # r = requests.get(category['link'], stream=True,headers=headers)
                    r = get_html(category['link'],mode='url')
                    items.append({'label': category['name'],'path':r,'is_playable':True})
                else:
                    #判断是否文件夹，是继续循环调用
                    pDialog.update(int(float(pnum)/float(allnum)*100), '解析网盘文件地址：判断为文件夹,跳过...  [' + str(pnum+1) + '/' + str(allnum) + ']')
                    items.append({'label': category['name'],
                    'path': plugin.url_for('onetogo', name=category['name'].encode('utf-8'), url=category['link'].encode('utf-8'),mode=mode,page=1),
                    })
                pnum += 1
    
    except NameError:
        pass

    return items



@plugin.route('/search/<value>/<page>/<mode>/')
def search(value,page,mode):
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
    videos = get_search_mode(keyword,page,mode)
    items = []
    if videos != []:
        if 'info' in videos[0]:
            for video in videos:
                info = video['info']
                info['mediatype'] = 'video'
                items.append({'label': video['name'],
                'path': plugin.url_for('source', name=video['name'].encode('utf-8'),url=video['href'],img=video['thumb'], mode=mode),
    	    'thumbnail': video['thumb'],
                'icon': video['thumb'],
                'info': info,
            })
        else:
            for video in videos:
                items.append({'label': video['name'],
                'path': plugin.url_for('source', name=video['name'].encode('utf-8'),url=video['href'],img=video['thumb'], mode=mode),
    	    'thumbnail': video['thumb'],
                'icon': video['thumb'],
            })
    
    categories = get_categories()
    for index in range(len(categories)):
        if mode == categories[index]['link']:
            if 'search' in categories[index]:
                if int(categories[index]['search']) == len(videos):
                    nextpage = {'label': '[COLOR yellow]下一页[/COLOR]', 'path': plugin.url_for('search', value=keyword,mode=mode,page=str(int(page)+1))}
                    items.append(nextpage)
    return items

def get_key (dict, value):
  return [k for k, v in dict.items() if v == value]

@plugin.route('/history/<name>/<url>/<mode>/')
def history(name,url,mode):
    items = []
    items.append({
        'label': '[COLOR yellow]'+ name +'[/COLOR]',
        'path': plugin.url_for(url,value='null',page=1,mode=mode),
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
                'path': plugin.url_for(url,value=get_key(hi,val[index])[0],page=1,mode=mode),
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
                vlist['author'] = get_categories()[index]['author']
                vlist['upload'] = get_categories()[index]['upload']
                if 'plot' in get_categories()[index]:
                    vlist['plot'] = get_categories()[index]['plot']
                for i in range(len(storage['homesort'])):
                    if storage['homesort'][i]['link'] == get_categories()[index]['link']:
                        vlist['id'] = storage['homesort'][i]['id']
                        #vlist['name'] = storage['homesort'][i]['name']
                        #vlist['link'] = storage['homesort'][i]['link']
                newhomesort.append(vlist)
            storage['homesort'] = newhomesort
            categories = sorted(newhomesort,key=lambda k:k.get('id'))
            dialog = xbmcgui.Dialog()
            dialog.notification('首页已更新', h +'个网站', xbmcgui.NOTIFICATION_INFO, 5000)
        else:
            newhomesort = []
            for index in range(len(get_categories())):
                vlist = {}
                vlist['id'] = get_categories()[index]['id']
                vlist['name'] = get_categories()[index]['name']
                vlist['link'] = get_categories()[index]['link']
                vlist['author'] = get_categories()[index]['author']
                vlist['upload'] = get_categories()[index]['upload']
                if 'plot' in get_categories()[index]:
                    vlist['plot'] = get_categories()[index]['plot']
                for i in range(len(storage['homesort'])):
                    if storage['homesort'][i]['link'] == get_categories()[index]['link']:
                        vlist['id'] = storage['homesort'][i]['id']
                        #vlist['name'] = storage['homesort'][i]['name']
                        #vlist['link'] = storage['homesort'][i]['link']
                newhomesort.append(vlist)
            storage['homesort'] = newhomesort
            categories = sorted(storage['homesort'],key=lambda k:k.get('id'))
    else:
        storage['homesort'] = get_categories()
        categories = sorted(get_categories(),key=lambda k:k.get('id'))

    items = []
    for category in categories:
        if category['id'] != 0:
            if 'plot' in category:
                items.append({
                'label': category['name'],
                'path': plugin.url_for('home',mode=category['link']),
                'info': {'plot':'@[COLOR blue]' + category['author'] + '[/COLOR]'  + ':\n\n    ' + category['plot'],'status':category['upload']+ ' 更新','cast':[(category['author'],'插件作者')],'mediatype':'video'},
                })
            else:
                items.append({
                    'label': category['name'],
                    'path': plugin.url_for('home',mode=category['link']),
                    'info': {'status':category['upload']+ '更新','cast':[(category['author'],'插件作者')],'mediatype':'video'},
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

########################################################################################################################################
########################################################################################################################################
#####以下是本插件独占代码，bangumi插件没有 - 用于让用户快速对接支持maccms等采集站
########################################################################################################################################
########################################################################################################################################

def get_xml(url,t=1,debug='no'):
    if debug == 'no':
        if t == 1:
            value = get_xml_1hour(url)
        if t == 24:
            value = get_xml_1day(url)
    else:
        r = requests.get(url,headers=headers)
        r.encoding = 'utf-8'
        r = r.text
        value = ET.fromstring(r.encode('utf-8'))
    return value
 
@plugin.cached(TTL=60)
def get_xml_1hour(url):
    r = requests.get(url,headers=headers)
    r.encoding = 'utf-8'
    r = r.text
    value = ET.fromstring(r.encode('utf-8'))
    return value

@plugin.cached(TTL=60*24)
def get_xml_1day(url):
    r = requests.get(url,headers=headers)
    r.encoding = 'utf-8'
    r = r.text
    value = ET.fromstring(r.encode('utf-8'))
    return value

def get_maccms_xml(api,url=0,keyword=0,page=0,banid='',debug='no'):
    if url != 0 and page != 0 and keyword == 0:
        #分类视频列表
        root = get_xml(api + '?ac=videolist&t=' + str(url) + '&pg=' + str(page),debug=debug)
        typelist = []
        lis = root.find('list')
        if int(lis.get('recordcount')) != 0:
            dialog = xbmcgui.Dialog()
            dialog.notification('第' + str(page) + '/' + lis.get('pagecount') + '页', '共' + lis.get('recordcount') + '个结果', xbmcgui.NOTIFICATION_INFO, 5000,False)
            for vide in lis.findall('video'):
                videoitem = {}
                videoitem['name'] = vide.find('name').text
                videoitem['href'] =  vide.find('id').text
                videoitem['thumb'] = vide.find('pic').text
                
                videoitem['info'] = {}
                videoitem['info']['title'] = vide.find('name').text
                plot = unicode(vide.find('des').text)
                plot = re.sub('<.*?>','',plot)
                plot = re.sub('&#?[a-z0-9]+;','',plot)
                plot = plot.replace(u'None','')
                videoitem['info']['plot'] = plot
                videoitem['info']['dateadded'] = vide.find('last').text
                videoitem['info']['genre'] = [vide.find('type').text]        
                videoitem['info']['country'] = [vide.find('area').text]
                videoitem['info']['year'] = vide.find('year').text

                #演员
                acto = unicode(vide.find('actor').text)
                if acto.find(u',') != -1:
                    actor = acto.split(u',')
                else:
                    actor = [acto]
                videoitem['info']['cast'] = actor

                #导演
                directo = unicode(vide.find('director').text)
                if directo.find(u',') != -1:
                    director = directo.split(u',')
                else:
                    director = directo
                videoitem['info']['director'] = director
                videoitem['info']['mediatype'] = 'video'
                typelist.append(videoitem)
            
    else:
        if url == 0 and keyword != 0 and page != 0:
            #搜索列表
            root = get_xml(api + '?ac=videolist&wd=' + str(keyword) + '&pg=' + str(page),debug=debug)
            typelist = []
            lis = root.find('list')
            if int(lis.get('recordcount')) != 0:
                dialog = xbmcgui.Dialog()
                dialog.notification('第' + str(page) + '/' + lis.get('pagecount') + '页', '共' + lis.get('recordcount') + '个结果', xbmcgui.NOTIFICATION_INFO, 5000,False)
                for vide in lis.findall('video'):
                    videoitem = {}
                    videoitem['name'] = vide.find('name').text
                    videoitem['href'] =  vide.find('id').text
                    videoitem['thumb'] = vide.find('pic').text
                
                    videoitem['info'] = {}
                    videoitem['info']['title'] = vide.find('name').text
                    plot = unicode(vide.find('des').text)
                    plot = re.sub('<.*?>','',plot)
                    plot = re.sub('&#?[a-z0-9]+;','',plot)
                    plot = plot.replace(u'None','')
                    videoitem['info']['plot'] = plot
                    videoitem['info']['dateadded'] = vide.find('last').text
                    videoitem['info']['genre'] = [vide.find('type').text]        
                    videoitem['info']['country'] = [vide.find('area').text]
                    videoitem['info']['year'] = vide.find('year').text

                    #演员
                    acto = unicode(vide.find('actor').text)
                    if acto.find(u',') != -1:
                        actor = acto.split(u',')
                    else:
                        actor = [acto]
                    videoitem['info']['cast'] = actor

                    #导演
                    directo = unicode(vide.find('director').text)
                    if directo.find(u',') != -1:
                        director = directo.split(u',')
                    else:
                        director = directo
                    videoitem['info']['director'] = director
                    videoitem['info']['mediatype'] = 'video'
                    typelist.append(videoitem)
        else:
            if url != 0 and keyword == 0 and page == 0:
                #资源列表
                root = get_xml(api + '?ac=videolist&ids=' + str(url),debug=debug,t=24)
                typelist = []
                dl = root.find('list').find('video').find('dl')
                
                for dd in dl.findall('dd'):
                    duopname = dd.get('flag')
                    strduop = unicode(dd.text)
                    duopdict = {}
                    if strduop.find(u'#') != -1:
                        duoplist = strduop.split(u'#')
                        for index in range(len(duoplist)):
                            cut = duoplist[index].split(u'$')
                            duopdict[cut[0]] = cut[1]
                    else:
                        cut = strduop.split(u'$')
                        duopdict[cut[0]] = cut[1]
                    typelist.append({'name':duopname,'href':str(duopdict)})
                tmp['maccmsids'] = url
                
            else:
                if url == 0 and keyword == 0 and page == 0:
                    #分类列表
                    root = get_xml(api + '?ac=list',debug=debug,t=24)
                    clas = root.find('class')
                    typelist = []
                    #debug
                    if debug != 'no':
                        pDialog = xbmcgui.DialogProgress()
                        pDialog.create('Debug模式', '收集信息中...')
                        banlist = ''
                        dnum = 1
                        pagesize = '0'
                        num = 1
                    for ty in clas.findall('ty'):
                        #debug
                        if debug != 'no':
                            tid = ty.get('id')
                            root1 = get_xml(api + '?ac=videolist&pg=1&t=' + tid,debug=debug)
                            lis1 = root1.find('list')
                            pagesize = str(lis1.get('pagesize'))
                            num = (float(dnum)/float(len(clas.findall('ty'))))*100
                            dnum += 1
                            pDialog.update(int(num), '收集信息中...' + str(round(num,2)) + '%')
                            if int(lis1.get('recordcount')) <= int(lis1.get('pagesize')):
                                banlist += ty.text.encode('utf-8') + '  ' + tid + '\n'
                        if banid != '':
                            if re.search(',',banid):
                                banidlist = banid.split(',')
                            else:
                                banidlist = [banid]
                            if str(ty.get('id')) not in banidlist:
                                typelist.append({'name':ty.text.encode('utf-8'),'link':ty.get('id')})
                        else:
                            typelist.append({'name':ty.text.encode('utf-8'),'link':ty.get('id')})
                    #debug
                    if debug != 'no':
                        txt = '建议banid：\n'
                        txt += str(banlist)
                        if pagesize != '0':
                            txt += '\n'
                            txt += '-'*50
                            txt += '\n建议设置的video值：' + pagesize + '\n'
                        #搜索可用判断
                        pDialog.update(50, '测试搜索中(1/2)...')
                        r2 = get_html(api + '?ac=videolist&wd=万万')
                        pDialog.update(100, '测试搜索中(2/2)...')
                        r3 = get_html(api + '?ac=videolist&wd=季')
                        txt += '-'*50
                        txt += '\n搜索api可用情况：'
                        if diff_float(r2,r3) > 0.95:
                            txt += '不同关键词搜索结果相似度' + str(round(diff_float(r2,r3)*100,2)) + '%，高于95%，判断此搜索api不可用，建议屏蔽搜索功能'
                        else:
                            txt += '不同关键词搜索结果相似度' + str(round(diff_float(r2,r3)*100,2)) + '%，低于95%，判断此搜索api可用'
                        dialog = xbmcgui.Dialog()
                        dialog.textviewer('debug',txt)
                else:
                    #mp4info
                    info = {}
                    root = get_xml(api + '?ac=videolist&ids=' + tmp['maccmsids'],debug=debug,t=24)
                    vide = root.find('list').find('video')
                    info['title'] = vide.find('name').text
                    plot = unicode(vide.find('des').text)
                    plot = re.sub('<.*?>','',plot)
                    plot = re.sub('&#?[a-z0-9]+;','',plot)
                    plot = plot.replace(u'None','')
                    info['plot'] = plot
                    info['dateadded'] = vide.find('last').text
                    info['genre'] = [vide.find('type').text]
                    info['country'] = [vide.find('area').text]
                    info['year'] = vide.find('year').text

                    #演员
                    acto = unicode(vide.find('actor').text)
                    if acto.find(u',') != -1:
                        actor = acto.split(u',')
                    else:
                        actor = [acto]
                    info['cast'] = actor

                    #导演
                    directo = unicode(vide.find('director').text)
                    if directo.find(u',') != -1:
                        director = directo.split(u',')
                    else:
                        director = directo
                    info['director'] = director
                    info['mediatype'] = 'video'
                    typelist = info
    # dialog = xbmcgui.Dialog()
    # dialog.textviewer('错误提示', str(xx.encode('utf-8')))

    return typelist
########################################################################################################################################
########################################################################################################################################
#####json
########################################################################################################################################
########################################################################################################################################
def get_json(url,t=1,debug='no'):
    if debug == 'no':
        if t == 1:
            value = get_json_1hour(url)
        if t == 24:
            value = get_json_1day(url)
    else:
        r = requests.get(url,headers=headers)
        r.encoding = 'utf-8'
        r = r.text
        value = json.loads(r)
    return value
 
@plugin.cached(TTL=60)
def get_json_1hour(url):
    r = requests.get(url,headers=headers)
    r.encoding = 'utf-8'
    r = r.text
    value = json.loads(r)
    return value

@plugin.cached(TTL=60*24)
def get_json_1day(url):
    r = requests.get(url,headers=headers)
    r.encoding = 'utf-8'
    r = r.text
    value = json.loads(r)
    return value

def get_maccms_json(api,url=0,keyword=0,page=0,banid='',debug='no'):
    if url != 0 and page != 0 and keyword == 0:
        #分类视频列表
        j = get_json(api + '?ac=videolist&t=' + str(url) + '&pg=' + str(page),debug=debug)
        typelist = []
        lis = j['list']
        if int(j['total']) != 0:
            dialog = xbmcgui.Dialog()
            dialog.notification('第' + str(page) + '/' + str(j['pagecount']) + '页', '共' + str(j['total']) + '个结果', xbmcgui.NOTIFICATION_INFO, 5000,False)
            for i in range(len(lis)):
                videoitem = {}
                videoitem['name'] = lis[i]['vod_name']
                videoitem['href'] =  lis[i]['vod_id']
                videoitem['thumb'] = lis[i]['vod_pic']
                
                videoitem['info'] = {}
                videoitem['info']['title'] = lis[i]['vod_name']
                videoitem['info']['dateadded'] = lis[i]['vod_time']
                videoitem['info']['country'] = [lis[i]['vod_area']]
                videoitem['info']['year'] = lis[i]['vod_year']
                plot = lis[i]['vod_content']
                plot = re.sub('<.*?>','',plot)
                plot = re.sub('&#?[a-z0-9]+;','',plot)
                plot = plot.replace('None','')
                videoitem['info']['plot'] = plot
                #分类
                genr = lis[i]['vod_class']
                if genr.find(u',') != -1:
                    genre = genr.split(u',')
                else:
                    genre = [genr]
                videoitem['info']['genre'] = genre

                #演员
                acto = lis[i]['vod_actor']
                if acto.find(u',') != -1:
                    actor = acto.split(u',')
                else:
                    actor = [acto]
                videoitem['info']['cast'] = actor

                #导演
                directo = lis[i]['vod_director']
                if directo.find(u',') != -1:
                    director = directo.split(u',')
                else:
                    director = directo
                videoitem['info']['director'] = director
                videoitem['info']['mediatype'] = 'video'
                typelist.append(videoitem)
            
    else:
        if url == 0 and keyword != 0 and page != 0:
            #搜索列表
            j = get_json(api + '?ac=videolist&wd=' + str(keyword) + '&pg=' + str(page),debug=debug)
            typelist = []
            lis = j['list']
            if int(j['total']) != 0:
                dialog = xbmcgui.Dialog()
                dialog.notification('第' + str(page) + '/' + str(j['pagecount']) + '页', '共' + str(j['total']) + '个结果', xbmcgui.NOTIFICATION_INFO, 5000,False)
                for i in range(len(lis)):
                    videoitem = {}
                    videoitem['name'] = lis[i]['vod_name']
                    videoitem['href'] =  lis[i]['vod_id']
                    videoitem['thumb'] = lis[i]['vod_pic']
                
                    videoitem['info'] = {}
                    videoitem['info']['title'] = lis[i]['vod_name']
                    videoitem['info']['dateadded'] = lis[i]['vod_time']
                    videoitem['info']['country'] = [lis[i]['vod_area']]
                    videoitem['info']['year'] = lis[i]['vod_year']

                    plot = lis[i]['vod_content']
                    plot = re.sub('<.*?>','',plot)
                    plot = re.sub('&#?[a-z0-9]+;','',plot)
                    plot = plot.replace(u'None','')
                    videoitem['info']['plot'] = plot
                    #分类
                    genr = lis[i]['vod_class']
                    if genr.find(u',') != -1:
                        genre = genr.split(u',')
                    else:
                        genre = [genr]
                    videoitem['info']['genre'] = genre

                    #演员
                    acto = lis[i]['vod_actor']
                    if acto.find(u',') != -1:
                        actor = acto.split(u',')
                    else:
                        actor = [acto]
                    videoitem['info']['cast'] = actor

                    #导演
                    directo = lis[i]['vod_director']
                    if directo.find(u',') != -1:
                        director = directo.split(u',')
                    else:
                        director = directo
                    videoitem['info']['director'] = director
                    videoitem['info']['mediatype'] = 'video'
                    typelist.append(videoitem)
        else:
            if url != 0 and keyword == 0 and page == 0:
                #资源列表
                j = get_json(api + '?ac=videolist&ids=' + str(url),debug=debug,t=24)
                typelist = []
                dl = j['list'][0]
                
                duopname = dl['vod_play_from']
                strduop = dl['vod_play_url']
                duopdict = {}
                if strduop.find(u'#') != -1:
                    duoplist = strduop.split(u'#')
                    for index in range(len(duoplist)):
                        cut = duoplist[index].split(u'$')
                        duopdict[cut[0]] = cut[1]
                else:
                    cut = strduop.split(u'$')
                    duopdict[cut[0]] = cut[1]
                typelist.append({'name':duopname,'href':str(duopdict)})
                tmp['maccmsids'] = url
                
            else:
                if url == 0 and keyword == 0 and page == 0:
                    #分类列表
                    j = get_json(api + '?ac=list',debug=debug,t=24)
                    typelist = []
                    #debug
                    if debug != 'no':
                        pDialog = xbmcgui.DialogProgress()
                        pDialog.create('Debug模式', '收集信息中...')
                        banlist = ''
                        dnum = 1
                        pagesize = '0'
                        num = 1
                    for i in range(len(j['class'])):
                        #debug
                        if debug != 'no':
                            tid = j['class'][i]['type_id']
                            j1 = get_json(api + '?ac=videolist&pg=1&t=' + str(tid),debug=debug)
                            pagesize = str(j['limit'])
                            num = (float(dnum)/float(len(j['class'])))*100
                            dnum += 1
                            pDialog.update(int(num), '收集信息中...' + str(round(num,2)) + '%')
                            if int(j1['total']) <= int(j1['limit']):
                                banlist += j['class'][i]['type_name'].encode('utf-8') + '  ' + str(tid) + '\n'
                        if banid != '':
                            if re.search(',',banid):
                                banidlist = banid.split(',')
                            else:
                                banidlist = [banid]
                            if str(j['class'][i]['type_id']) not in banidlist:
                                typelist.append({'name':j['class'][i]['type_name'].encode('utf-8'),'link':j['class'][i]['type_id']})
                        else:
                            typelist.append({'name':j['class'][i]['type_name'].encode('utf-8'),'link':j['class'][i]['type_id']})
                    #debug
                    if debug != 'no':

                        txt = '建议banid：\n'
                        txt += str(banlist)
                        if pagesize != '0':
                            txt += '\n'
                            txt += '-'*50
                            txt += '\n建议设置的video值：' + pagesize + '\n'
                        #搜索可用判断
                        pDialog.update(50, '测试搜索中(1/2)...')
                        r2 = get_html(api + '?ac=videolist&wd=万万')
                        pDialog.update(100, '测试搜索中(2/2)...')
                        r3 = get_html(api + '?ac=videolist&wd=季')
                        txt += '-'*50
                        txt += '\n搜索api可用情况：'
                        if diff_float(r2,r3) > 0.95:
                            txt += '不同关键词搜索结果相似度' + str(round(diff_float(r2,r3)*100,2)) + '%，高于95%，判断此搜索api不可用，建议屏蔽搜索功能'
                        else:
                            txt += '不同关键词搜索结果相似度' + str(round(diff_float(r2,r3)*100,2)) + '%，低于95%，判断此搜索api可用'
                        dialog = xbmcgui.Dialog()
                        dialog.textviewer('debug',txt)
                else:
                    #mp4info
                    info = {}
                    j = get_json(api + '?ac=videolist&ids=' + tmp['maccmsids'],debug=debug,t=24)
                    typelist = []
                    vide = j['list'][0]
                    info['title'] = vide['vod_name']
                    plot = vide['vod_content']
                    plot = re.sub('<.*?>','',plot)
                    plot = re.sub('&#?[a-z0-9]+;','',plot)
                    plot = plot.replace(u'None','')
                    info['plot'] = plot
                    info['dateadded'] = vide['vod_time']
                    info['country'] = [vide['vod_area']]
                    info['year'] = vide['vod_year']

                    #分类
                    genr = vide['vod_class']
                    if genr.find(u',') != -1:
                        genre = genr.split(u',')
                    else:
                        genre = [genr]
                    info['genre'] = genre

                     #演员
                    acto = vide['vod_actor']
                    if acto.find(u',') != -1:
                        actor = acto.split(u',')
                    else:
                        actor = [acto]
                    info['cast'] = actor

                    #导演
                    directo = vide['vod_director']
                    if directo.find(u',') != -1:
                        director = directo.split(u',')
                    else:
                        director = directo
                    info['director'] = director
                    info['mediatype'] = 'video'
                    typelist = info
    # dialog = xbmcgui.Dialog()
    # dialog.textviewer('错误提示', str(xx.encode('utf-8')))

    return typelist




#对接sharelist搭建的网盘站
def get_sharelist(home):
    typelist = []
    typelist.append({'name':'mode','link':'sharelist'})
    r = get_html(home)
    rurl = get_html(home,mode='url')
    soup = BeautifulSoup(r, "html5lib")
    files = soup.find_all('a')

    baseurl = re.search('(http(s)?:\/\/).*?\/',rurl).group()
    
    if baseurl[-1:] == '/':
        baseurl = baseurl[:-1]

    for index in range(len(files)):
        try:
            x = 0
            if files[index]['href'] != '/':
                files[index]['href'] = files[index]['href'].replace('?preview','')
                if files[index]['href'][:4] != 'http':
                    flink = baseurl + files[index]['href']
                else:
                    flink = files[index]['href']

                if files[index]['href'][-1:] == '/':
                    fname = files[index]['href'][:-1]
                else:
                    fname = files[index]['href']
                
                if fname != '':
                    fname = re.search('[^/]+(?!.*/)',fname).group()
                fname = urldecode(fname)

                if typelist != []:
                    #对比和已有列表是否有重复项
                    for i in range(len(typelist)):
                        if typelist[i]['link'] != flink:
                            x = x+1
                    
                    if x ==  len(typelist) and fname != '':
                        typelist.append({'name':fname + ' - [COLOR gray]' + urldecode(flink) + '[/COLOR]','link':flink})
                            
                else:
                    typelist.append({'name':fname + ' - [COLOR gray]' + urldecode(flink) + '[/COLOR]','link':flink})
                    # nowlist.append(fname)
                
                
        except KeyError:
            pass
    # lastlist = nowlist
    # dialog = xbmcgui.Dialog()
    # dialog.textviewer('错误提示', str(lastlist))
    return typelist


#对接原版goindex
def get_goindex(home):
    typelist = []
    typelist.append({'name':'mode','link':'goindex'})
    if re.search('workers.dev',home):
        r = post_html(home,str({"password":"null"}),cf=1)
    else:
        r = post_html(home,str({"password":"null"}))

    j = json.loads(r)
    fl = j['files']
    for i in range(len(fl)):
        if re.match('[^/]+\.[a-zA-Z0-9]{1,4}',fl[i]['name']):
            #文件
            typelist.append({'name':fl[i]['name'] + u' - [COLOR gray]' + home.decode('utf-8') + urldecode(fl[i]['name']) + u'[/COLOR]','link':home.decode('utf-8') + fl[i]['name']})
        else:
            #文件夹
            typelist.append({'name':fl[i]['name'] + u' - [COLOR gray]' + home.decode('utf-8') + urldecode(fl[i]['name']) + u'/[/COLOR]','link':home.decode('utf-8') + fl[i]['name'] + u'/'})
    return typelist

#对接yanzai修改版goindex - 官网demo 2020-4-28版本测试通过
def get_yanzaigoindex(home):
    if re.search('\|',home):
        
        ho = home.split('|')
        home = ho[0]
        if len(ho) == 3:
            pindex = int(ho[1])
            ptoken = ho[2]
    else:
        pindex = 0
        ptoken = ''

    typelist = []
    typelist.append({'name':'mode','link':'yanzaigoindex'})

    if re.search('\/[0-9]+\:\/',home):
        #不是首页，不检索有几个网盘
        if re.search('workers.dev',home):
            r0 = requests.get(home)
            if r0.status_code != requests.codes.ok:
                #检测到状态码401 需要登录

                # dialog = xbmcgui.Dialog()
                # dialog.textviewer('错误提示', str(r0.status_code))
                if tmp['yanzaiuser'] and tmp['yanzaipass']:
                    #尝试用缓存的账号密码登录
                    scraper = cfscrape.create_scraper()
                    s = scraper.get_tokens(home,headers=headers,auth=HTTPBasicAuth(tmp['yanzaiuser'], tmp['yanzaipass']))

                    r = requests.post(home,data={"password":"","page_token":ptoken,"page_index":pindex},headers=headers,cookies=s[0],auth=HTTPBasicAuth(tmp['yanzaiuser'], tmp['yanzaipass']))
                    if r.status_code == 200:
                        #登录成功
                        j = json.loads(r.text)
                    else:
                        #失败，要求输入账号密码
                        dialog = xbmcgui.Dialog()
                        username = dialog.input('查看加密文件夹(1/2)\n-- 请输入用户名 --', type=xbmcgui.INPUT_ALPHANUM)
                        password = dialog.input('查看加密文件夹(2/2)\n-- 请输入密码 --', type=xbmcgui.INPUT_ALPHANUM)
                        scraper = cfscrape.create_scraper()
                        s = scraper.get_tokens(home,headers=headers,auth=HTTPBasicAuth(username, password))
                        r = requests.post(home,data={"password":"","page_token":ptoken,"page_index":pindex},headers=headers,cookies=s[0],auth=HTTPBasicAuth(username, password))
                        j = json.loads(r.text)
                        tmp['yanzaiuser'] = username
                        tmp['yanzaipass'] = password
                else:
                    dialog = xbmcgui.Dialog()
                    username = dialog.input('查看加密文件夹(1/2)\n-- 请输入用户名 --', type=xbmcgui.INPUT_ALPHANUM)
                    password = dialog.input('查看加密文件夹(2/2)\n-- 请输入密码 --', type=xbmcgui.INPUT_ALPHANUM)
                    scraper = cfscrape.create_scraper()
                    s = scraper.get_tokens(home,headers=headers,auth=HTTPBasicAuth(username, password))
                
                    r = requests.post(home,data={"password":"","page_token":ptoken,"page_index":pindex},headers=headers,cookies=s[0],auth=HTTPBasicAuth(username, password))
                    # dialog = xbmcgui.Dialog()
                    # dialog.textviewer('错误提示', str(r.status_code))
                    j = json.loads(r.text)
                    tmp['yanzaiuser'] = username
                    tmp['yanzaipass'] = password
            else:
                #网盘没有加密
                r = post_html(home,str({"password":"","page_token":ptoken,"page_index":pindex}),cf=1)
                try:
                    j = json.loads(r)
                except ValueError:
                    r = post_html(home,jsons=str({"password":"","page_token":ptoken,"page_index":pindex,"q": ""}),cf=1)
                    j = json.loads(r)
        else:
            r0 = requests.get(home)
            if r0.status_code != requests.codes.ok:
                #检测到状态码401 需要登录
                if tmp['yanzaiuser'] and tmp['yanzaipass']:
                    #尝试用缓存的账号密码登录
                    r = requests.post(home,data={"password":"","page_token":ptoken,"page_index":pindex},headers=headers,auth=HTTPBasicAuth(tmp['yanzaiuser'],tmp['yanzaipass']))
                    if r.status_code == 200:
                        #登录成功
                        j = json.loads(r.text)
                    else:
                        #失败，要求输入账号密码
                        dialog = xbmcgui.Dialog()
                        username = dialog.input('查看加密文件夹(1/2)\n-- 请输入用户名 --', type=xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)
                        password = dialog.input('查看加密文件夹(2/2)\n-- 请输入密码 --', type=xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)
                        r = requests.post(home,data={"password":"","page_token":ptoken,"page_index":pindex},headers=headers,auth=HTTPBasicAuth(username, password))
                        j = json.loads(r.text)
                        tmp['yanzaiuser'] = username
                        tmp['yanzaipass'] = password
                else:
                    dialog = xbmcgui.Dialog()
                    username = dialog.input('查看加密文件夹(1/2)\n-- 请输入用户名 --', type=xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)
                    password = dialog.input('查看加密文件夹(2/2)\n-- 请输入密码 --', type=xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)
                    r = requests.post(home,data={"password":"","page_token":ptoken,"page_index":pindex},headers=headers,auth=HTTPBasicAuth(username, password))
                    j = json.loads(r.text)
                    tmp['yanzaiuser'] = username
                    tmp['yanzaipass'] = password
            else:
                #网盘没有加密
                r = post_html(home,str({"password":"","page_token":ptoken,"page_index":pindex}))
                try:
                    j = json.loads(r)
                except ValueError:
                    r = post_html(home,jsons=str({"password":"","page_token":ptoken,"page_index":pindex,"q": ""}))
                    j = json.loads(r)
        
        
        fl = j['data']['files']
        for i in range(len(fl)):
            if re.match('[^/]+\.[a-zA-Z0-9]{1,4}',fl[i]['name']):
                #文件
                typelist.append({'name':fl[i]['name'] + u' - [COLOR gray]' + home.decode('utf-8') + urldecode(fl[i]['name']) + u'[/COLOR]','link':home.decode('utf-8') + fl[i]['name']})
            else:
                #文件夹
                typelist.append({'name':fl[i]['name'] + u' - [COLOR gray]' + home.decode('utf-8') + urldecode(fl[i]['name']) + u'/[/COLOR]','link':home.decode('utf-8') + fl[i]['name'] + u'/'})
        if j['nextPageToken']:
            # dialog = xbmcgui.Dialog()
            # dialog.textviewer('错误提示', str(j['nextPageToken'].encode('utf-8')))
            typelist.append({'name':u'[COLOR yellow]下一页[/COLOR]','link':home + '|' + str(pindex+1) + '|' + j['nextPageToken'].encode('utf-8')})
        
    else:
        #检索有几个网盘
        if re.search('workers.dev',home):
            r = get_html(home,cf=1)
        else:
            r = get_html(home)
        try:
            ser = re.search('\[(\"|\').*?(\"|\')\]',r).group()
            dlist = eval(ser)
            for i in range(len(dlist)):
                typelist.append({'name':dlist[i].decode('utf-8') + u' - [COLOR gray]' + home.decode('utf-8') + str(i) +  u':/[/COLOR]','link':home.decode('utf-8') + str(i) +  u':/'})
        except NameError:
            pass
    return typelist

    























if __name__ == '__main__':
    plugin.run()
