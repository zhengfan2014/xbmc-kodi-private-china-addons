#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from xbmcswift2 import Plugin,xbmcaddon,xbmc
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
import os

__addon__      = xbmcaddon.Addon()
__author__     = __addon__.getAddonInfo('author')
__scriptid__   = __addon__.getAddonInfo('id')
__scriptname__ = __addon__.getAddonInfo('name')
__version__    = __addon__.getAddonInfo('version')
__language__   = __addon__.getLocalizedString

__cwd__        = xbmc.translatePath( __addon__.getAddonInfo('path') ).decode("utf-8")
__profile__    = xbmc.translatePath( __addon__.getAddonInfo('profile') ).decode("utf-8")
__resource__   = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'lib' ) ).decode("utf-8")
__temp__       = xbmc.translatePath( os.path.join( __profile__, 'temp') ).decode("utf-8")

sys.path.append (__resource__)
# from zhconv import convert


def unescape(string):
    string = urllib2.unquote(string).decode('utf8')
    quoted = HTMLParser.HTMLParser().unescape(string).encode('utf-8')
    #转成中文
    return re.sub(r'%u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})', lambda m: unichr(int(m.group(1), 16)), quoted)

def sat(word,fanyi='zh-hans',sub=''):
    if type(word) == str:
        word = word.decode('utf-8')
    if sub != '':
        sub = eval(sub)
        for key in sub:
            word = word.replace(key.decode('utf-8'),sub[key].decode('utf-8'))
    word = convert(word,fanyi)
    return word.encode('utf-8')

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
    if cf == '':
        if ua == 'pc':
            r = requests.get(url,headers=headers)
        if ua == 'mobile':
            r = requests.get(url,headers=mheaders)
        if ua == 'iphone':
            r = requests.get(url,headers=iphoneheaders)
        if ua == 'ipad':
            r = requests.get(url,headers=ipadheaders)
        if ua == 'mac':
            r = requests.get(url,headers=macheaders)
        if encode == 'utf-8':
            r.encoding = 'utf-8'
        if encode == 'gbk':
            r.encoding = 'gbk'
        if mode == 'url':
            html = r.url
        else:
            html = r.text
    else:
        scraper = cfscrape.create_scraper()
        if ua == 'pc':
            s = scraper.get_tokens(url,headers=headers)
            r = requests.get(url,headers=headers,cookies=s[0])
        if ua == 'mobile':
            s = scraper.get_tokens(url,headers=mheaders)
            r = requests.get(url,headers=mheaders,cookies=s[0])
        if ua == 'iphone':
            s = scraper.get_tokens(url,headers=iphoneheaders)
            r = requests.get(url,headers=iphoneheaders,cookies=s[0])
        if ua == 'ipad':
            s = scraper.get_tokens(url,headers=ipadheaders)
            r = requests.get(url,headers=ipadheaders,cookies=s[0])
        if ua == 'mac':
            s = scraper.get_tokens(url,headers=macheaders)
            r = requests.get(url,headers=macheaders,cookies=s[0])

        if encode == 'utf-8':
            r.encoding = 'utf-8'
        if encode == 'gbk':
            r.encoding = 'gbk'

        if mode == 'url':
            html = r.url
        else:
            html = r.text
    return html

@plugin.cached(TTL=2)
def post_html(url,data,ua='pc',cf='',encode='utf-8'):
    data =eval(data)
    if cf == '':
        if ua == 'pc':
            r = requests.post(url,headers=headers,data=data)
        if ua == 'mobile':
            r = requests.post(url,headers=mheaders,data=data)
        if ua == 'iphone':
            r = requests.post(url,headers=iphoneheaders,data=data)
        if ua == 'ipad':
            r = requests.post(url,headers=ipadheaders,data=data)
        if ua == 'mac':
            r = requests.post(url,headers=macheaders,data=data)
        
        if encode == 'utf-8':
            r.encoding = 'utf-8'
        if encode == 'gbk':
            r.encoding = 'gbk'
        html = r.text
    else:
        scraper = cfscrape.create_scraper()
        html = scraper.post(url,data).content
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
    item = eval('get_' + mode + '_videos')(url,page)
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
    item = eval('get_' + mode + '_search')(keyword,page)
    return item

damakulist = ['bimibimi','yhdm','agefans','silisili','iafuns','qinmei','srsg','ningmoe']
##########################################################
###主入口
##########################################################

def get_categories():
    return [{'id':1,'name':'哔咪哔咪(bimibimi.tv)[COLOR pink][/COLOR]','link':'bimibimi','author':'zhengfan2014','upload':'2020-6-26','videos':24,'search':24,'plot':'更新速度比樱花稍慢，但是总体画质比樱花高'},
            {'id':2,'name':'樱花动漫(yhdm.tv)','link':'yhdm','author':'zhengfan2014','upload':'2020-6-26','videos':15,'search':20,'plot':'昨晚b站23点发布的BNA，今天早上就可以在樱花看了,更新速度杠杠滴'},
            {'id':3,'name':'Age动漫(agefans.tw)','link':'agefans','author':'zhengfan2014','upload':'2020-6-30','videos':24,'search':15,'plot':'海外站点，虽然访问速度偏慢，但是番剧mp4是国内的观看并不卡。更新番剧速度一般'},
            {'id':4,'name':'嘶哩嘶哩(silisili.in)','link':'silisili','author':'zhengfan2014','upload':'2020-6-30','videos':10,'search':20,'plot':'大部分有1080p，但是番剧收录少，居然没有4月新番bna'},
            {'id':5,'name':'八重樱动漫(iafuns.com)','link':'iafuns','author':'zhengfan2014','upload':'2020-6-30','plot':'更新速度一般'},
            {'id':6,'name':'番組計劃(guguani.me)','link':'srsg','author':'zhengfan2014','upload':'2020-6-30','plot':'更新很不及时。格莱普尼尔和b站最新差两集，而且现在没注册登录不能看番了，不过还好它们api目前对不登录的用户没有限制（也就是本插件目前还能用）'},
            {'id':7,'name':'Qinmei(qinmei.video)','link':'qinmei','author':'zhengfan2014','upload':'2020-6-30','videos':20,'search':20,'plot':'站长是酷安的，现在网站好像半凉了'},
            {'id':8,'name':'柠萌瞬间(ningmoe.com)','link':'ningmoe','author':'zhengfan2014','upload':'2020-6-30','videos':10,'search':10,'plot':'还不错，大部分有1080p，但是番剧收录少，bna木有'},
            {'id':9,'name':'吐槽弹幕网(tucao.one)','link':'tucao','author':'zhengfan2014','upload':'2020-6-26','videos':24,'search':12,'plot':'正版c站，11年到现在，现在除了番剧区的，其他区的视频基本凉凉放不了。更新快，还是1080p的，但是里面有些无修的黄番，未成年的朋友可以打开黑名单屏蔽功能，加 无修 和 BD 这两个关键词加以屏蔽'},
            {'id':10,'name':'clicli弹幕网(clicli.me)','link':'cliclime','author':'zhengfan2014','upload':'2020-6-30','plot':'基本都是1080p'},
            {'id':11,'name':'五弹幕(5dm.tv)','link':'5dmtv','author':'zhengfan2014','upload':'2020-6-30','videos':32,'search':32,'plot':'新番看不了的，可能得注册会员才能看，我没注册过，注册会员20大洋，现在这么多网站白嫖，愿意出20块的算是真爱粉了哈哈'},
            {'id':12,'name':'clicli弹幕网(clicli.co)','link':'cliclico','author':'zhengfan2014','upload':'2020-6-30','plot':'山寨c站，和clicli.me互掐'},
            {'id':13,'name':'zzzfun(zzzfun.com)','link':'zzzfun','author':'zhengfan2014','upload':'2020-6-30','videos':12,'search':10,'plot':''},
            {'id':14,'name':'动漫岛(dmd8.com)','link':'dmd8','author':'zhengfan2014','upload':'2020-6-30','videos':20,'search':10,'plot':''}]

##########################################################
###以下是模块，网站模块请粘贴在这里面
##########################################################

#bimibimi
def get_bimibimi_categories():
    return [{'name':'新番放送','link':'http://www.bimiacg.com/type/riman'},
            {'name':'国产动漫','link':'http://www.bimiacg.com/type/guoman'},
            {'name':'番组计划','link':'http://www.bimiacg.com/type/fanzu'},
            {'name':'剧场动画','link':'http://www.bimiacg.com/type/juchang'},
            {'name':'影视','link':'http://www.bimiacg.com/type/move'}]

def get_bimibimi_videos(url,page):
    videos = []
    if page == 1:
        r = get_html(url + '/')
    else:
        r = get_html(url + '-' +str(page) +'/')
    soup = BeautifulSoup(r, "html5lib")
    linelist = soup.find('ul',class_='drama-module clearfix tab-cont')
    alist = linelist.find_all('a',class_='img')
    plist = linelist.find_all('span',class_='fl')
    for i in range(len(alist)):
        videoitem = {}
        videoitem['name'] =  alist[i]['title'] + ' [' + plist[i].text + ']' 
        videoitem['href'] =  'http://www.bimiacg.com' + alist[i]['href']
        videoitem['thumb'] = alist[i].img['data-original']
        videoitem['info'] = {'plot' : alist[i]['title'] + '\n' + plist[i].text }
        videos.append(videoitem)
    return videos

def get_bimibimi_source(url):
    videos = []
    r = get_html(url)
    soup = BeautifulSoup(r, 'html.parser')
    linelist = soup.find_all('div',class_='play_box')
    sourcelist = []
    for index in range(len(linelist)):
        alist = linelist[index].find_all('a')
        duopdict = {}
        for i in range(len(alist)):
            duopdict[alist[i].text] = 'http://www.bimiacg.com/' + alist[i]['href']
        sourcelist.append(duopdict)

    for index in range(len(sourcelist)):
        videoitem = {}
        videoitem['name'] = '播放线路' + str(index+1)
        videoitem['href'] = str(sourcelist[index])
        videos.append(videoitem)
    tmp['bghtml'] = r
    return videos

def get_bimibimi_mp4info(url):
    rtext = tmp['bghtml']
    soup = BeautifulSoup(rtext, 'html.parser')
    li = soup.find_all('li',class_='clearfix')
    infodict={}
    infodict['title'] = soup.find('div',class_='tit').h1.text
    if re.search(u' ',infodict['title']):
        infodict['title'].split(u' ')[0]
    for index in range(len(li)):
        emtext = li[index].em.text
        emtext = emtext.replace(u'：','')
        if li[index].find_all('a'):
            a = li[index].find_all('a')
            if len(a) == 1:
                atex = a[0].text
                atext = atex
            else:
                atext = []
                for index in range(len(a)):
                    if a[index].text != '':
                        atex = a[index].text
                        atext.append(atex)
        else:
            atex = li[index].text
            atex = atex.replace(u'：','')
            atex = atex.replace(emtext,'')
            atext = atex.strip()
        emtext = emtext.replace(u'提醒','status')
        emtext = emtext.replace(u'声优','cast')
        emtext = emtext.replace(u'类型','genre')
        emtext = emtext.replace(u'导演','writer')
        emtext = emtext.replace(u'开播','premiered')
        emtext = emtext.replace(u'年份','year')
        emtext = emtext.replace(u'地区','country')
        emtext = emtext.replace(u'更新','dateadded')
        emtext = emtext.replace(u'简介','plot')
        if atext != '':
            infodict[emtext] = atext
    return infodict

def get_bimibimi_mp4(url):
    r = get_html(url)
    soup = BeautifulSoup(r, 'html.parser')
    str1 = r.find(u'var player_data=')
    str2 = r.find(u'</script><script type="text/javascript"')
    cutjson = r[str1+16:str2]
    #print(cutjson)
    j = json.loads(cutjson)
    #向接口发送请求
    if j['from']:
        if j['from'] == 'niux':
            apiurl = 'http://182.254.167.161/danmu/niux.php?id=' + j['url']
        else:
            apiurl = 'http://182.254.167.161/danmu/play.php?url=' + j['url']
        r = get_html(apiurl)
        soup = BeautifulSoup(r, 'html.parser')
        source = soup.find('source',type='video/mp4')
        try:
            mp4 = source['src']
        except:
            dialog = xbmcgui.Dialog()
            ok = dialog.ok('错误提示', '没有找到视频')
        #rt = []
        #rt.append(title.text)
        #rt.append(mp4)
    return mp4

def get_bimibimi_search(keyword,page):
    videos = []
    if int(page) == 1:
        url = 'http://www.bimiacg.com/vod/search/'
        data = str({'wd':keyword})
        r = post_html(url,data)
    else:
        url = 'http://www.bimiacg.com/vod/search/wd/'+keyword+'/page/'+ str(page) +'/'
        r = get_html(url)
    soup = BeautifulSoup(r, "html5lib")
    linelist = soup.find('ul',class_='drama-module clearfix tab-cont')
    alist = linelist.find_all('a',class_='img')
    plist = linelist.find_all('span',class_='fl')
    # dialog = xbmcgui.Dialog()
    # dialog.textviewer('错误提示', str(alist))
    for i in range(len(alist)):
        videoitem = {}
        videoitem['name'] =  alist[i]['title'] + '[' + plist[i].text + ']' 
        videoitem['href'] =  'http://www.bimiacg.com' + alist[i]['href']
        videoitem['thumb'] = alist[i].img['data-original']
        videoitem['info'] =  {'plot' : alist[i]['title'] + '\n' + plist[i].text  }
        videos.append(videoitem)
    return videos
#樱花
def get_yhdm_categories():
    return [{'name':'日本动漫','link':'http://www.yhdm.tv/japan/'},
            {'name':'国产动漫','link':'http://www.yhdm.tv/china/'},
            {'name':'美国动漫','link':'http://www.yhdm.tv/american/'},
            {'name':'动漫电影','link':'http://www.yhdm.tv/movie/'},
            {'name':'新番动漫','link':'http://www.yhdm.tv/2020/'},
            {'name':'剧场版','link':'http://www.yhdm.tv/37/'},
            {'name':'OVA版','link':'http://www.yhdm.tv/36/'},
            {'name':'真人动漫','link':'http://www.yhdm.tv/38/'}]

def get_yhdm_videos(url,page):
    videos = []
    if int(page) == 1:
        r = get_html(url)
    else:
        r = get_html(url + str(page) + '.html')
    soup = BeautifulSoup(r, 'html.parser')
    if soup.find('div',class_='lpic') or soup.find('div',class_='imgs'):
        if soup.find('div',class_='lpic'):
            linelist = soup.find('div',class_='lpic')
        else:
            linelist = soup.find('div',class_='imgs')
    #print(len(linelist))
    li = linelist.find_all('li')
    for index in range(len(li)):
        videoitem = {}
        videoitem['name'] =  li[index].a.img['alt']
        videoitem['href'] =  'http://www.yhdm.tv/' + li[index].a['href']
        videoitem['thumb'] = li[index].a.img['src']
        videoitem['info'] =  {'plot' :li[index].p.text}
        videos.append(videoitem)
    return videos

def get_yhdm_source(url):
    #爬视频列表的
    videos = []
    r = get_html(url)
    #print(r.text)
    soup = BeautifulSoup(r, 'html.parser')
    linelist = soup.find('div',class_='main0')
    #print(len(linelist))
    li = linelist.find_all('li')

    sourcelist = []
    duopdict = {}
    for index in range(len(li)):
        duopdict[li[index].a.text] = 'http://www.yhdm.tv/' + li[index].a['href']
    sourcelist.append(duopdict)

    
    videoitem = {}
    videoitem['name'] = '播放线路1'
    videoitem['href'] = str(sourcelist[0])
    videos.append(videoitem)
    tmp['bghtml'] = r
    return videos

def get_yhdm_mp4info(url):
    rtext = tmp['bghtml']
    soup = BeautifulSoup(rtext, 'html.parser')
    title = soup.find('div',class_='rate r').h1.text
    sinfo = soup.find('div',class_='sinfo')
    span = sinfo.find_all('span')
    info = soup.find('div',class_='info')
    infodict={}
    infodict['title'] = title
    for index in range(len(span)):
        text = span[index].label.text.strip()+span[index].a.text.strip()
        text = text.encode('utf-8')
        text = text.split(':')
        text[0] = text[0].replace('类型','genre')
        text[0] = text[0].replace('上映','year')
        text[0] = text[0].replace('地区','country')

        if text[1]:
            infodict[text[0]] = text[1]
    
    infodict['plot'] = info.text.strip()

    return infodict

def get_yhdm_mp4(url):
    r = get_html(url)
    soup = BeautifulSoup(r, 'html.parser')
    vid = soup.find('div',class_='bofang')
    vid = vid.div['data-vid']
    vid = vid.split('$')
    if vid[1] == 'mp4' or vid[1] == 'qz':
        if vid[1] == 'mp4':
            rt = vid[0]
        if vid[1] == 'qz':
            apiurl = 'https://js.voooe.cn/jiexi/api.php'
            q = vid[0]
            ref = 'http://tup.yhdm.tv/?vid=' + q +'$qz'
            refb64 = base64.b64encode(ref.encode('utf-8'))
            qb64 = base64.b64encode(q.encode('utf-8'))
            data = {'url': vid[0], 'referer': refb64,'time':int(time.time()),'other':qb64,'ref':'0','type':'','ios':''}
            r = requests.post(apiurl,headers=headers,data=data)
            j = json.loads(r.text)
            mp4 = j['url']
            mp4 = mp4.replace('\\','')
            rt = mp4
            return rt
    else:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('错误提示','不受支持的播放链接')
    

def get_yhdm_search(keyword,page):
    videos = []
    url = 'http://www.yhdm.tv/search/' + keyword + '/'
    r = get_html(url)
    soup = BeautifulSoup(r, 'html.parser')
    if soup.find('div',class_='lpic') or soup.find('div',class_='imgs'):
        if soup.find('div',class_='lpic'):
            linelist = soup.find('div',class_='lpic')
        else:
            linelist = soup.find('div',class_='imgs')
    #print(len(linelist))
    li = linelist.find_all('li')
    for index in range(len(li)):
        videoitem = {}
        videoitem['name'] =  li[index].a.img['alt']
        videoitem['href'] =  'http://www.yhdm.tv/' + li[index].a['href']
        videoitem['thumb'] = li[index].a.img['src']
        videoitem['info'] =  {'plot' :li[index].p.text}
        videos.append(videoitem)
    return videos

#agefan.tw
def get_agefans_categories():
    return [{'name':'每日推荐','link':'https://agefans.tw/recommend'},
            {'name':'最近更新','link':'https://agefans.tw/update'}]

def get_agefans_videos(url,page):
    #爬视频列表的
    videos = []
    html = get_html(url,cf=1)
    soup = BeautifulSoup(html,'html.parser')
    
    base = soup.find('ul',class_='row list-unstyled my-gutters-2')
    li = base.find_all('li')
    
    for index in range(len(li)):
        title = li[index].find('a')
        imgs = li[index].find('img')
        try:
            img = imgs['src']
        except KeyError:
            img = imgs['data-src']
        videoitem = {}
        videoitem['name'] =  title.div.text.strip()
        videoitem['thumb'] =  'http:' + img
        videoitem['href'] = 'https://agefans.tw' + title['href']
        videos.append(videoitem)
    return videos

def get_agefans_source(url):
    #爬视频列表的
    videos = []
    #bak = url
    #url = url.replace('detail','play')
    #aid = re.search('[0-9]+',url).group()
    html = get_html(url,cf=1)
    soup = BeautifulSoup(html, 'html.parser')
    #base = soup.find('div',class_='baseblock2')
    base = soup.find('section',class_='mb-0')
    #sourcelist = base.find_all('div',class_='blockcontent')
    sourcelist = base.find_all('ul',class_='row list-unstyled my-gutters-2')
    sclist = []
    for index in range(len(sourcelist)):
        #alist = sourcelist[index].find_all('a',class_='episode')
        alist = sourcelist[index].find_all('a')
        duopdict = {}
        for index in range(len(alist)):
            #uri = 'https://agefans.tw/_getplay_2?animeid='+ str(aid)+ '&routeidx='+ str(alist[index]['routeidx'])+ '&episodeidx='+ str(alist[index]['episodeidx'])+ '&lhf='+ str(alist[index]['lhf'])+ '&sign='+ alist[index]['sign']+ '&num='+ str(random.random())
            duopdict[alist[index].text.strip()] = 'https://agefans.tw' + alist[index]['href']
        sclist.append(duopdict)
    

    
    for index in range(len(sclist)):
        videoitem = {}
        videoitem['name'] = '播放线路' + str(index+1)
        videoitem['href'] = str(sclist[index])
        videos.append(videoitem)
    tmp['bghtml'] = html
    return videos

def get_agefans_mp4info(url):
    rtext = tmp['bghtml']
    infodict={}
    soup = BeautifulSoup(rtext, 'html.parser')
    #取中文名
    base = soup.find('div',class_='mycol-lg-90 mycol-md-80 mycol-120 mb-3')
    
    titles = base.find_all('div')
    title = titles[1].find_all('span')
    title = title[1].text

    dialog = xbmcgui.Dialog()
    dialog.textviewer('错误提示', title)
    if re.search(u'/',title):
        title = title.split(u'/')[0].strip()
    infodict['title'] = title
    # table = soup.find('table')
    # li = table.find_all('li')
    table = soup.find('ul',class_='list-unstyled mb-0')
    li = table.find_all('li')

    for index in range(len(li)):
        #text = li[index].find('span',class_='play_imform_tag').text.strip() + li[index].find('span',class_='play_imform_val').text.strip()
        #text = text.encode('utf-8')
        span = li[index].find_all('span')
        text = [span[0].text.strip(),span[1].text.strip()]
        #text = text.split('：')
        text[0] = text[0].replace(u'地區','country')
        text[0] = text[0].replace(u'標簽','tag')
        text[0] = text[0].replace(u'原版名稱','originaltitle')
        text[0] = text[0].replace(u'原作','writer')
        text[0] = text[0].replace(u'制作公司','studio')
        text[0] = text[0].replace(u'首播時間','premiered')
        text[0] = text[0].replace(u'播放狀態','status')
        text[0] = text[0].replace(u'劇情類型','genre')
        text[0] = text[0].replace(u'官方網站','showlink')
        if text[1]:
            if text[1].find(u',') != -1:
                text[1] = text[1].split(u',')
            infodict[text[0]] = text[1]
    pinfo = soup.find('p',class_='small')
    infodict['plot'] =pinfo.text.strip()
    # dialog = xbmcgui.Dialog()
    # dialog.textviewer('错误提示',str(infodict))
    return infodict

def get_agefans_mp4(url):
    r = get_html(url,cf=1)
    soup = BeautifulSoup(r, 'html.parser')
    video = soup.find('div',id='play')
    vid = str(video)
    if vid.find('<script type="text/javascript">') != -1:
        str1 = vid.find('$.get(')
        str2 = vid.find('function')
        url1 = vid.strip()[str1+7:str2-3]
        r1 = get_html('https://agefans.tw' + url1,cf=1)
        j = json.loads(r1)
        mp4 = j['result']['url']
        if not re.search('https?://',mp4):
            if re.search('//',mp4):
                mp4 = 'https:' + mp4
        # dialog = xbmcgui.Dialog()
        # dialog.textviewer('错误提示', str(url1) + '\n' + str(mp4))
    else:
        iframe = video.find('iframe')
        mp4 = re.search('https?:\/\/..+\.mp4',iframe['src']).group()
        #mp4 = iframe['src']
    # mp4 = unescape(html)
    # if mp4[:2] == '//':
    #     mp4 = 'http:' + mp4
    # if mp4.find('baidu.com') != -1:
    #     mp4 = re.search('https?:\/\/..+\.mp4',mp4).group()
    return mp4

def get_agefans_search(keyword,page):
    videos = []
    if int(page) == 1:
        url = 'https://agefans.tw/search?q=' +keyword
    else:
        url = 'https://agefans.tw/search?q=' +keyword + '&page=' +str(page)
    html = get_html(url,cf=1)
    soup = BeautifulSoup(html,'html.parser')
    base = soup.find('section',id='search_list')
    li = base.find_all('li',class_='card')
    # dialog = xbmcgui.Dialog()
    # dialog.textviewer('错误提示', str(li[1]))
    for index in range(len(li)):
        title = li[index].find('h5')
        imgs = li[index].find('img')
        link = li[index].find('a')
        try:
            img = imgs['src']
        except KeyError:
            img = imgs['data-src']
        videoitem = {}
        videoitem['name'] =  title.text.strip()
        videoitem['thumb'] =  'http:' + img
        videoitem['href'] = 'https://agefans.tw' + link['href']
        videos.append(videoitem)
    return videos

#qinmei
def get_qinmei_categories():
    return [{'name':'新番','link':'https://qinmei.video/api/v2/animates?sortBy=updatedAt&sortOrder=-1&size=20&page='},
            {'name':'剧场版','link':'https://qinmei.video/api/v2/animates?sortBy=updatedAt&sortOrder=-1&size=20&kind=5e359428d1f1dc2e17f84fd4&page='},
            {'name':'战斗','link':'https://qinmei.video/api/v2/animates?sortBy=updatedAt&sortOrder=-1&size=20&kind=5e341fc1d1f1dc2e17f84fae&page='},
            {'name':'日常','link':'https://qinmei.video/api/v2/animates?sortBy=updatedAt&sortOrder=-1&size=20&kind=5e341fc8e7bc242e192d23cf&page='},
            {'name':'搞笑','link':'https://qinmei.video/api/v2/animates?sortBy=updatedAt&sortOrder=-1&size=20&kind=5e341fced1f1dc2e17f84faf&page='},
            {'name':'治愈','link':'https://qinmei.video/api/v2/animates?sortBy=updatedAt&sortOrder=-1&size=20&kind=5e341fd8e7bc242e192d23d0&page='},
            {'name':'致郁','link':'https://qinmei.video/api/v2/animates?sortBy=updatedAt&sortOrder=-1&size=20&kind=5e341fe7d1f1dc2e17f84fb0&page='},
            {'name':'异界','link':'https://qinmei.video/api/v2/animates?sortBy=updatedAt&sortOrder=-1&size=20&kind=5e341feed1f1dc2e17f84fb1&page='}]

def get_qinmei_videos(url,page):
    #爬视频列表的
    videos = []
    r = get_html(url + str(page))
    j = json.loads(r)
    vlist = j['data']['list']
    for index in range(len(vlist)):
        img = vlist[index]['coverVertical']
        if img[:2] != 'ht':
            if img[:2] == '//':
                img = 'http:'+img
            else:
                img = 'http://qinmei.video' +img
        videoitem = {}
        videoitem['name'] =  vlist[index]['title']
        videoitem['href'] =  vlist[index]['slug']
        videoitem['thumb'] = img
        videos.append(videoitem)
    return videos

def get_qinmei_source(url):
    #爬视频列表的
    videos = []
    url = 'https://qinmei.video/api/v2/animates/' + url
    r = get_html(url)
    j = json.loads(r)
    sourcelist = []
    duopdict = {}
    for index in range(len(j['data']['eposides'])):
        duopdict[j['data']['eposides'][index]['title']] = j['data']['eposides'][index]['_id']
    sourcelist.append(duopdict)

    
    videoitem = {}
    videoitem['name'] = '播放线路1'
    videoitem['href'] = str(sourcelist[0])
    videos.append(videoitem)
    tmp['bghtml'] = r
    return videos

def get_qinmei_mp4info(url):
    rtext = tmp['bghtml']

    #t = json.dumps(r.text, ensure_ascii=False)  
    j = json.loads(rtext)
    infodict={}
#print(j['data']['status'])
    infodict['title'] = j['data']['title']
    infodict['plot'] = j['data']['introduce']
    staff = j['data']['staff']
    if staff != '':
        staff = staff.encode('utf-8')
        staff =staff.split('/')
        for i in range(len(staff)):
            act = staff[i]
            act = act.replace('导演','writer')
            act = act.split(':')
            infodict[act[1]] = act[0]

    actor = j['data']['actor']#角色：cv
    actor = actor.split('/')
    for i in range(len(actor)):
        try:
            act = actor[i]
            act = act.split(':')
            actor[i] = (act[1],act[0])
        except IndexError:
            pass
    infodict['castandrole'] = actor
    infodict['premiered'] = str(j['data']['firstPlay'][:4]) + '-' +str(j['data']['firstPlay'][4:6]) + '-' +str(j['data']['firstPlay'][6:8])
    #infodict['playcount'] = j['data']['countPlay']
    infodict['userrating'] = j['data']['countStar']
    try:
        infodict['country'] = j['data']['area'][0]['name']
    except IndexError:
        pass
    try:
        infodict['year'] = j['data']['year'][0]['name']
    except IndexError:
        pass


    return infodict

def get_qinmei_mp4(url):
    url = 'https://qinmei.video/api/v2/animates/' + url + '/play'
    r = get_html(url)
    #soup = BeautifulSoup(r, 'html.parser')
    j = json.loads(r)
    mp4 = j['data']['link'][0]['value']
    return mp4

def get_qinmei_search(keyword,page):
    #爬视频列表的
    videos = []
    url = 'https://qinmei.video/api/v2/animates?type=queryAnimate&title='+keyword+'&page='+ str(page) + '&size=20&sortBy=updatedAt&sortOrder=-1'
    r = get_html(url)
    j = json.loads(r)
    vlist = j['data']['list']
    for index in range(len(vlist)):
        img = vlist[index]['coverVertical']
        if img[:2] != 'ht':
            if img[:2] == '//':
                img = 'http:'+img
            else:
                img = 'http://qinmei.video' +img
        videoitem = {}
        videoitem['name'] =  vlist[index]['title']
        videoitem['href'] =  vlist[index]['slug']
        videoitem['thumb'] = img
        videos.append(videoitem)
    return videos

#柠檬瞬间
def get_ningmoe_categories():
    #return [{'name':'本月热门','link':'https://www.ningmoe.com/api/get_hot_bangumi'}]
    return [{'name':'2020年1月','link':'https://www.ningmoe.com/static/bangumi/bangumi.json'},
            {'name':'2019年10月','link':'https://www.ningmoe.com/api/get_hot_bangumi'},
            {'name':'2019年7月','link':'https://www.ningmoe.com/api/get_hot_bangumi'},
            {'name':'2019年4月','link':'https://www.ningmoe.com/api/get_hot_bangumi'},
            {'name':'2019年1月','link':'https://www.ningmoe.com/api/get_hot_bangumi'}]

def get_ningmoe_videos(url,page):
    #爬视频列表的
    videos = []
    r = get_html(url)
    j = json.loads(r)
    for index in range(len(j)):
        for i in range(len(j[index])):
            videoitem = {}
            videoitem['name'] =  j[index][i]['title']
            if 'zh-Hans' in j[index][i]['titleTranslate']:
                videoitem['name'] =  j[index][i]['titleTranslate']['zh-Hans'][0]
            
            videoitem['href'] =  j[index][i]['bangumi_id']
            videoitem['thumb'] = j[index][i]['cover']
            videos.append(videoitem)


    # data = str({'page': page, 'limit': 10})
    # r = post_html(url,data)
    # j = json.loads(r)
    # bgmlist = j['data']
    # for index in range(len(bgmlist)):
    #     if bgmlist[index]['classification']['cn_name'] != '':
    #         name = bgmlist[index]['classification']['cn_name']
    #     else:
    #         name = bgmlist[index]['classification']['en_name']
    #     videoitem = {}
    #     videoitem['name'] =  name
    #     videoitem['href'] =  bgmlist[index]['bangumi_id']
    #     videoitem['thumb'] = bgmlist[index]['classification']['bangumi_cover']
    #     videos.append(videoitem)
    return videos

def get_ningmoe_source(url):
    #爬视频列表的
    videos = []
    apiurl = 'https://www.ningmoe.com/api/get_bangumi'
    data = str({'bangumi_id':url})
    r = post_html(apiurl,data)
    j = json.loads(r)
    vlist = j['data']['posts']
    sourcelist = []
    s1dict = {}
    s2dict = {}
    for index in range(len(vlist)):
        if vlist[index]['url'] != '':
            s1dict[vlist[index]['eps_name']] = vlist[index]['url']
        if vlist[index]['bak_url'] != '':
            s2dict[vlist[index]['eps_name']] = vlist[index]['bak_url']
    sourcelist.append(s1dict)
    sourcelist.append(s2dict)
    videoitem = {}
    videoitem['name'] = '播放线路1'
    videoitem['href'] = str(sourcelist[0])
    videos.append(videoitem)
    videoitem = {}
    videoitem['name'] = '播放线路2'
    videoitem['href'] = str(sourcelist[1])
    videos.append(videoitem)
    tmp['bghtml'] = r
    return videos

def get_ningmoe_mp4info(url):
    rtext = tmp['bghtml']
    infodict={}
    
    j = json.loads(rtext)
    vcount = j['data']['video_total_count']
    infodict['countPlay'] = int(vcount)
    vinfo = j['data']['bangumi']
    infodict['originaltitle'] = vinfo['en_name']
    infodict['plot'] = vinfo['description']
    infodict['premiered'] = vinfo['air_date']

    infodict['title'] = vinfo['cn_name']

    return infodict

def get_ningmoe_mp4(url):
    if url.find('kingsnug.cn') != -1:
        apiurl = 'https://www.ningmoe.com/api/get_real_yun_url'
        data = str({'url':url})
        r = post_html(apiurl,data=data)
        j = json.loads(r)
        try:
            mp4 = j['data']['yun_url']
        except KeyError:
            dialog = xbmcgui.Dialog()
            ok = dialog.ok('错误提示','查询链接失败')
    else:
        mp4 = url
    return mp4

def get_ningmoe_search(keyword,page):
    #爬视频列表的
    videos = []
    url = 'https://www.ningmoe.com/api/search'
    data = str({'keyword': keyword, 'type': 'anime', 'bangumi_type': '', 'page': str(page), 'limit': 10})
    r = post_html(url,data)
    j = json.loads(r)
    bgmlist = j['data']
    for index in range(len(bgmlist)):
        if bgmlist[index]['classification']['cn_name'] != '':
            name = bgmlist[index]['classification']['cn_name']
        else:
            name = bgmlist[index]['classification']['en_name']
        videoitem = {}
        videoitem['name'] =  name
        videoitem['href'] =  bgmlist[index]['bangumi_id']
        videoitem['thumb'] = bgmlist[index]['classification']['bangumi_cover']
        videos.append(videoitem)
    return videos

    #8chongying
def get_iafuns_categories():
    return [{'name':'2020新番','link':'http://iafuns.com/catalog?year=2020'},
            {'name':'2019新番','link':'http://iafuns.com/catalog?year=2019'}]

def get_iafuns_videos(url,page):
    #爬视频列表的
    videos = []
    r = get_html(url)
    soup = BeautifulSoup(r, 'html.parser')
    li = soup.find_all('li',class_='col-lg-2 col-md-3 col-sm-3 col-4 st_col position-relative')
    for index in range(len(li)):
        videoitem = {}
        videoitem['name'] =  li[index].h6.text
        videoitem['href'] =  'http://iafuns.com' + li[index].a['href']
        videoitem['thumb'] = 'http:' + li[index].img['data-src']
        videos.append(videoitem)
    return videos

def get_iafuns_source(url):
    #爬视频列表的
    videos = []
    r = get_html(url)
    soup = BeautifulSoup(r, 'html.parser')
    ul = soup.find('ul',class_='nav nav-tabs flex-row flex-nowrap')
    li = ul.find_all('li')
    sourcelist = []
    for index in range(len(li)):
        sce = li[index].a
        sce1 = sce.text
        videoitem = {}
        videoitem['name'] = sce1.encode('utf-8')

        u = soup.find('div',id=sce['aria-controls'][1:])
        l = u.find_all('li')
        duopdict = {}
        for index in range(len(l)):
            if l[index].a.text.strip() in duopdict:
                duopdict[l[index].a.text.strip() + str(index)] = l[index]['play_cfg']+ ':' +l[index]['play_id']
            else:
                duopdict[l[index].a.text.strip()] = l[index]['play_cfg']+ ':' +l[index]['play_id']
        videoitem['href'] = str(duopdict)
        videos.append(videoitem)
  
    tmp['bghtml'] = r
    return videos

def get_iafuns_mp4info(url):
    rtext = tmp['bghtml']
    infodict={}

    soup = BeautifulSoup(rtext, 'html.parser')
    title = soup.find('li',class_='breadcrumb-item active')
    infodict['title'] = title.text

    tb = soup.find('table')
    tr = tb.find_all('tr')
    for index in range(len(tr)):
        key = tr[index].th.text
        key = key.encode('utf-8')
        key = key.replace('原名','originaltitle')
        key = key.replace('别名','tag')
        key = key.replace('地区','country')
        key = key.replace('首播','year')
        key = key.replace('原作','writer')
        key = key.replace('制作','studio')
        key = key.replace('剧情','genre')
        key = key.replace('状态','status')
        key = key.replace('系列','sorttitle')
        value = tr[index].td.text
        if value.find('/') != -1:
            value = value.split('/')
        else:
            if value.find(',') != -1:
                value = value.split(',')
        infodict[key] = value
    p = soup.find('span')
    infodict['plot'] = p.text

    return infodict


def get_iafuns_mp4(url):
    url = url.split(':')
    if url[0][:2].find('qz') != -1:
        apiurl = 'http://iafuns.com/_get_e_i?url=' + url + '&quote=1'
    else:
        if url[0][:4].find('quan') != -1:
            apiurl = 'http://iafuns.com/_get_qn?id=' +url[1]
        else:
            apiurl = 'http://iafuns.com/_get_raw?id=' +url[1]
            # else:
            #     dialog = xbmcgui.Dialog()
            #     ok = dialog.ok('错误提示', '不支持的视频格式，请向插件作者反馈 播放视频名字 和 播放线路')
    
    r = get_html(apiurl)

    if apiurl.find('_get_qn') != -1 or apiurl.find('_get_raw') != -1:
        if not re.search('https?',r):
            mp4 = 'http:' + r
        else:
            mp4 = r
        if re.search('ck-qq.com',r):
            r1 = get_html(r)
            str1 = r1.find('url:')
            str2 = r1.find('type:')
            mp4 = r1[str1+4:str2].strip()
            mp4 = mp4[1:-2]
    if apiurl.find('_get_e_i') != -1:
        j = json.loads(r)
        mp4 = j['result']
    #dialog = xbmcgui.Dialog()
    #dialog.textviewer('错误提示', mp4)
    return mp4

def get_iafuns_search(keyword,page):
    #爬视频列表的
    videos = []
    url = 'http://iafuns.com/search?q=' + keyword
    r = get_html(url)
    soup = BeautifulSoup(r, 'html.parser')
    li = soup.find_all('div',class_='col-lg-2 col-md-3 col-sm-3 col-4 st_col')
    for index in range(len(li)):
        videoitem = {}
        videoitem['name'] =  li[index].h6.text
        videoitem['href'] =  'http://iafuns.com' + li[index].a['href']
        videoitem['thumb'] = 'http:' + li[index].img['data-src']
        videos.append(videoitem)
    return videos

#silisili
def get_silisili_categories():
    return [{'name':'最新更新','link':'http://www.silisili.in/zxgx.html'},
            {'name':'日本动漫','link':'http://www.silisili.in/riyu/'},
            {'name':'国产动漫','link':'http://www.silisili.in/guoyu/'}]

def get_silisili_videos(url,page):
    videos = []
    if int(page) != 1 and url != 'http://www.silisili.in/zxgx.html':
        url = url + 'index_'+str(page)+'.html'
    r = get_html(url)
    soup = BeautifulSoup(r, 'html.parser')
    if url == 'http://www.silisili.in/zxgx.html':
        #最新更新
        li = soup.find_all('div',class_='ggwp')
        for index in range(len(li)):
            videoitem = {}
            videoitem['name'] =  li[index].a['title']
            videoitem['href'] =  'http://www.silisili.in'+li[index].a['href']
            videoitem['thumb'] = li[index].a.img['src']
            videos.append(videoitem)
    else:
        base = soup.find('div',class_='anime_list')
        # dialog = xbmcgui.Dialog()
        # dialog.textviewer('评论区',str(url))
        li = base.find_all('dl')
        for index in range(len(li)):
            videoitem = {}
            videoitem['name'] =  li[index].dd.h3.text
            videoitem['href'] =  'http://www.silisili.in'+li[index].dt.a['href']
            videoitem['thumb'] = li[index].dt.a.img['src'] 
            videos.append(videoitem)
    
    return videos

def get_silisili_source(url):
    #爬视频列表的
    videos = []
    r = get_html(url)
    soup = BeautifulSoup(r, 'html.parser')
    base = soup.find('div',class_='swiper-slide')
    li = base.find_all('li')
    sourcelist = []
    duopdict = {}
    for index in range(len(li)):
        duopdict[li[index].a.em.span.text] = 'http://www.silisili.in' + li[index].a['href']

    sourcelist.append(duopdict)
    videoitem = {}
    videoitem['name'] = '播放线路1'
    videoitem['href'] = str(sourcelist[0])
    videos.append(videoitem)
    tmp['bghtml'] = r
    return videos

def get_silisili_mp4info(url):
    rtext = tmp['bghtml']
    infodict={}
    soup = BeautifulSoup(rtext, 'html.parser')
    base = soup.find('div',class_='detail con24 clear')

    infodict['title'] = base.h1.text
    li = base.find_all('div',class_='d_label')
    li2 = base.find_all('div',class_='d_label2')
    for index in range(len(li)):
        key = li[index].b.text
        key = key.encode('utf-8')
        key = key.replace('地区：','country')
        key = key.replace('标签：','genre')
        key = key.replace('状态：','status')
        key = key.replace('年代：','year')

        if li[index].a:
            value = li[index].a.text
        else:
            text = li[index].text
            text = text.replace(li[index].b.text,'')
            value = text
        value = value.encode('utf-8')
        if value.find('年') != -1:
            value = value.split('年')
            value = value[0]
        else:
            if value.find(',') != -1:
                value = value.split(',')
        
        infodict[key] = value
    
    vinfo = li2[1].text
    vinfo = vinfo.encode('utf-8')
    vinfo = vinfo.split('：')
    infodict['plot'] = vinfo[1]


    return infodict

def get_silisili_mp4(url):
    r = get_html(url)
    soup = BeautifulSoup(r, 'html.parser')
    mp4 = soup.find('iframe')
    
    if re.search('\?http',mp4['src']):
        mp4 = mp4['src'].split('?')
        mp4 = mp4[1]
    else:
        r = get_html(mp4['src'])
        soup = BeautifulSoup(r, 'html.parser')
        mp4 = soup.find('source')['src']
    # dialog = xbmcgui.Dialog()
    # dialog.textviewer('错误提示', str(mp4.encode('utf-8')))
    return mp4

def get_silisili_search(keyword,page):
    videos = []
    if int(page) == 1:
        url = 'http://www.silisili.in/e/search/index.php'
        data = str({'show':'title','tbname':'movie','tempid':1,'keyboard':keyword,'button':'搜索'})
        r = post_html(url,data)
    else:
        url = 'http://www.silisili.in/e/search/result/index.php?page=' + str(int(page)-1) + '&searchid=' + str(tmp['silisearchid'])
        r = get_html(url)
    soup = BeautifulSoup(r, 'html.parser')
    div = soup.find('div',class_='page')

    if re.search('(?<=searchid=)\d+',div.a['href']) and int(page) == 1:
        searchid = re.search('(?<=searchid=)\d+',div.a['href']).group()
        tmp['silisearchid'] = searchid
    base = soup.find('div',class_='anime_list')
    
    li = base.find_all('dl')
    for index in range(len(li)):
        videoitem = {}
        videoitem['name'] =  li[index].dd.h3.text
        videoitem['href'] =  'http://www.silisili.in'+li[index].dt.a['href']
        videoitem['thumb'] = li[index].dt.a.img['src'] 
        videos.append(videoitem)
    
    return videos

#srsg
def get_srsg_categories():
    return [{'name':'全部番剧','link':'https://guguani.me/api/v1/bangumi'},
            {'name':'每日推荐','link':'https://guguani.me/api/v1/carousel'}]

def get_srsg_videos(url,page):
    #爬视频列表的
    videos = []
    r = get_html(url,cf=1)
    j = json.loads(r)
    if re.search('bangumi',url):
        for index in range(len(j['result'])):
            i = len(j['result']) - index - 1
            videoitem = {}
            videoitem['name'] = j['result'][i]['bangumi']['title']
            videoitem['thumb'] =  'https://cdn-guguani-img.fantasy-love.top/'+j['result'][i]['cover_v']['path']
            videoitem['href'] = str(j['result'][i]['bangumi']['id'])
            videoitem['info'] = {'plot':j['result'][i]['bangumi']['description'],'year':j['result'][i]['quarterly']['year']}
            videos.append(videoitem)
    else:
        for index in range(len(j['result'])):
            videoitem = {}
            videoitem['name'] = j['result'][index]['title']
            videoitem['thumb'] =  'https://cdn-guguani-img.fantasy-love.top/'+j['result'][index]['cover_src']
            videoitem['href'] = re.search('\d+',j['result'][index]['link']).group()
            videos.append(videoitem)
        r = get_html('https://guguani.me/api/v1/recommend?pageNo=1&pageSize=50',cf=1)
        j = json.loads(r)
        for index in range(len(j['result'])):
            videoitem = {}
            videoitem['name'] = j['result'][index]['title']
            videoitem['thumb'] =  'https://cdn-guguani-img.fantasy-love.top/'+j['result'][index]['cover_v']
            videoitem['href'] = j['result'][index]['id']
            videos.append(videoitem)
    return videos

def get_srsg_source(url):
    #爬视频列表的
    videos = []
    scraper = cfscrape.create_scraper()
    r = get_html('https://guguani.me/api/v1/episodes/' +url,cf=1)


    j = json.loads(r)
    sclist = []
    duopdict = {}
    try:
        for index in range(len(j)):
            duopdict[j[index]['title']] = j[index]['id']
        sclist.append(duopdict)
    except TypeError:
        dialog = xbmcgui.Dialog()
        dialog.textviewer('错误提示','没有视频')


    
    videoitem = {}
    videoitem['name'] = '播放线路1'
    videoitem['href'] = str(sclist[0])
    videos.append(videoitem)
    scraper = cfscrape.create_scraper()
    r = get_html('https://guguani.me/api/v1/bangumi/meta/' +url,cf=1)
    tmp['bghtml'] = r
    return videos

def get_srsg_mp4info(url):
    rtext = tmp['bghtml']
    infodict={}
    
    j = json.loads(rtext)
    infodict['title'] =sat(j['title'],sub=str({'期':'季'}))
    infodict['plot'] =j['description']
    tmp['bgimg'] ='https://cdn-guguani-img.fantasy-love.top/'+j['cover_v_src']
    #播出时间
    data = re.search(r'[0-9]{4}-[0-9]{2}-[0-9]{2}',j['broadcast_time']).group()
    year = re.search(r'[0-9]{4}',j['broadcast_time']).group()
    infodict['premiered'] = data
    infodict['year'] = year
    tag = []
    for index in range(len(j['tags'])):
        tag.append(j['tags'][index]['name'])
    infodict['genre'] = tag

    return infodict

def get_srsg_mp4(url):
    j = get_html('https://guguani.me/api/v1/ep/' + url,cf=1)
    j = json.loads(j)
    mp4 = 'https://cdn-guguani-tv.fantasy-love.top/' + j['parts'][0]['resources']['path'][:-3]+ 'm3u8'
    return mp4

#tucao.one
def get_tucao_categories():
    return [{'name':'连载新番','link':'http://www.tucao.one/list/11/'},
            {'name':'OAD·OVA·剧场版','link':'http://www.tucao.one/list/26/'},
            {'name':'完结番组','link':'http://www.tucao.one/list/10/'}]

def get_tucao_videos(url,page):
    #爬视频列表的
    videos = []
    if int(page) != 1:
        url = url + 'index_' + str(page) + '.html'
    html = get_html(url,cf=1)
    soup = BeautifulSoup(html,'html.parser')
    
    ullist = soup.find('div',class_='list')
    videolist = ullist.find_all('li')
    for index in range(len(videolist)):
        a = videolist[index].find('a',class_='pic')
        videoitem = {}
        videoitem['name'] =  a.img['alt']
        videoitem['thumb'] =  a.img['src']
        videoitem['href'] = a['href']
        videos.append(videoitem)
    return videos

def get_tucao_source(url):
    videos = []
    pDialog = xbmcgui.DialogProgress()
    pDialog.create('加载中', '初始化')
    pDialog.update(33, '尝试爬取网页数据...')
    html = get_html(url,cf=1)
    
    sclist = []

    str1 = html.find('<li>type=video')
    str2 = html.find('<script language="javascript">$(document).ready(function(){$("#shadow")')
    tmpstr = html[str1:str2]
    str3 = tmpstr.find('</li><li>')
    duopstr = tmpstr[4:str3]
    duoplist = duopstr.split('**')
    try:
        duopdict = {}
        for index in range(len(duoplist)):
            info = duoplist[index].split('|')
            duopdict[info[1].decode('utf-8')] = info[0][16:]
        sclist.append(duopdict)
    except:
        pDialog.update(66, '爬取失败，使用官方API接口再次尝试...(一般版权原因404的番剧可以用api爬到)')
        #尝试json接口
        hid = re.search('(?<=play/h)[0-9]+',url).group()
        apiurl = 'http://www.tucao.one/api_v2/view.php?apikey=25tids8f1ew1821ed&hid=' +str(hid)
        r = get_html(apiurl,cf=1)
        j = json.loads(r)
        duoplist = j['result']['video']
        duopdict = {}
        for index in range(len(duoplist)):
            duopdict[duoplist[index]['title']] = duoplist[index]['file']
        sclist.append(duopdict)
    
    videoitem = {}
    videoitem['name'] = '播放线路1'
    videoitem['href'] = str(sclist[0])
    videos.append(videoitem)

    tmp['bghtml'] = html
    return videos

def get_tucao_mp4info(url):
    rtext = tmp['bghtml']
    infodict={}
    try:
        j = json.loads(rtext)
        infodict['plot'] = j['description']
    except:
        soup = BeautifulSoup(rtext, 'html.parser')
        plot = soup.find('div',class_='show_content')
        infodict['plot'] = re.sub('\n\n\n\n','',plot.text)
    return infodict

def get_tucao_mp4(url):
    mp4 = url
    return mp4

def get_tucao_search(keyword,page):
    videos = []
    if int(page) == 1:
        url = 'https://www.tucao.one/index.php?m=search&c=index&a=init2&catid=&time=&order=&username=&tag=&q=' +keyword
    else:
        url = 'https://www.tucao.one/index.php?m=search&c=index&a=init2&catid=&time=&order=&username=&tag=&q=' +keyword + '&page=' +str(page)
    html = get_html(url,cf=1)
    soup = BeautifulSoup(html,'html.parser')
    
    videolist = soup.find_all('div',class_='list')
    for index in range(len(videolist)):
        img = videolist[index].find('div',class_='pic')
        videoitem = {}
        videoitem['name'] =  img.a.img['alt']
        videoitem['thumb'] =  img.a.img['src']
        videoitem['href'] = img.a['href']
        videos.append(videoitem)
    return videos

#clicli.me
def get_cliclime_categories():
    return [{'name':'编辑推荐','link':'https://api.clicli.us/posts?status=public&sort=&tag=%E6%8E%A8%E8%8D%90&uid=&page=1&pageSize=10'},
            {'name':'新番表','link':'https://api.clicli.us/posts?status=nowait&sort=%E6%96%B0%E7%95%AA&tag=&uid=&page=1&pageSize=100'},
            {'name':'排行','link':'https://api.clicli.us/rank'},
            {'name':'最近更新','link':'https://api.clicli.us/posts?status=public&sort=bgm&tag=&uid=&page=1&pageSize=30'}]

def get_cliclime_videos(url,page):
    #爬视频列表的
    videos = []
    html = get_html(url)
    try:
        j = json.loads(html)
        for index in range(len(j['posts'])):
            con = j['posts'][index]['content']
            img = re.search('!\\[[^\\]]+\\]\\([^\\)]+\\)', con)
            videoitem = {}
            videoitem['name'] = j['posts'][index]['title']
            videoitem['href'] = j['posts'][index]['id']
            videoitem['thumb'] = img.group()[7:-1]
            text = j['posts'][index]['content']
            text = re.sub('\!\[.*?\)','',text) #处理markdown图片
            text = re.sub('[#]+[\s]+','',text) #正则h1 - h4
            text = re.sub('[?<=\*\*](.*?)[?=\*\*]',r'\1',text)
            text = re.sub('>[\s]+','',text)
            text = re.sub('<.*?>.*?</.*?>','',text)
            text = re.sub('\[(\S+?)\]\(\S+\)',r'[COLOR green]\1[/COLOR]\n',text)
            videoitem['info'] = {'plot':text,'cast':[(j['posts'][index]['uname'],j['posts'][index]['uqq'])],'genre':j['posts'][index]['tag'].strip().split(u' ')}
            videos.append(videoitem)  
    except ValueError:
        pass
    return videos

def get_cliclime_source(url):
    videos = []
    html = get_html('https://api.clicli.us/videos?pid=' + str(url) +'&page=1&pageSize=150')
    
    sclist = []
    try:
        duopdict = {}
        j = json.loads(html)
        pnum = 1
        for index in range(len(j['videos'])):
            #pp = pp.encode('utf-8')
            if j['videos'][index]['title'] != '':
                duopdict['P ' + str(j['videos'][index]['oid']) + '  ' + j['videos'][index]['title']] = j['videos'][index]['content']
            else:
                duopdict['P ' + str(j['videos'][index]['oid'])] = j['videos'][index]['content']
            pnum += 1  
        sclist.append(duopdict)
        videoitem = {}
        videoitem['name'] = '播放线路1'
        videoitem['href'] = str(sclist[0])
        videos.append(videoitem)

        tmp['bghtml'] = str(url)
        
    except IndexError:
        pass
    except TypeError:
        html = get_html('https://api.clicli.us/post/' + str(url))
        j = json.loads(html)
        text = j['result']['content']
        text = re.sub('\!\[.*?\)',u'【图片】',text)
        text = re.sub('#+([\s\S]*?)\n',r'[COLOR red]\1[/COLOR]\n',text)
        text = re.sub('>+([\s\S]*?)\n',r'[COLOR pink]\1[/COLOR]\n',text)
        text = re.sub('\*\*([\s\S]*?)\*\*',r'[COLOR yellow]\1[/COLOR]\n',text)
        text = re.sub('\[[A-Za-z0-9\.]+?\]([\s\S]*?)\([A-Za-z0-9\.]+?\)',r'[COLOR green]\1[/COLOR]\n',text)
        dialog = xbmcgui.Dialog()
        dialog.textviewer(j['result']['title'], text)
    return videos
    
def get_cliclime_mp4info(url):
    infodict={}
    url = tmp['bghtml']
    html = get_html('https://api.clicli.us/post/' + url)
    j = json.loads(html)
    text = j['result']['content']
    text = re.sub('\!\[.*?\)','',text)
    text = re.sub('#+ ','',text)
    text = re.sub('> ','',text)
    text = re.sub('\[(\S+?)\]\(\S+\)',r'[COLOR green]\1[/COLOR]\n',text)
    
    infodict['plot'] = text
    infodict['title'] = j['result']['title']
    infodict['genre'] = j['result']['tag'].strip().split(u' ')
    return infodict

def get_cliclime_mp4(url):
    if url[:4] != 'http':
        url = 'https://jx.clicli.us/jx?url=' + url
        html = get_html(url)
        try:
            j = json.loads(html)
            mp4 = j['url'] 
        except ValueError:
            pass
    else:
        mp4 = url
    return mp4

def get_cliclime_search(keyword,page):
    #爬视频列表的
    videos = []
    html = get_html('https://api.clicli.us/search/posts?key=' + keyword)
    try:
        j = json.loads(html)
        for index in range(len(j['posts'])):
            con = j['posts'][index]['content']
            img = re.search('!\\[[^\\]]+\\]\\([^\\)]+\\)', con)
            videoitem = {}
            videoitem['name'] = j['posts'][index]['title']
            videoitem['href'] = j['posts'][index]['id']
            videoitem['thumb'] = img.group()[7:-1]
            text = j['posts'][index]['content']
            text = re.sub('\!\[.*?\)','',text) #处理markdown图片
            text = re.sub('[#]+[\s]+','',text) #正则h1 - h4
            text = re.sub('[?<=\*\*](.*?)[?=\*\*]',r'\1',text)
            text = re.sub('>[\s]+','',text)
            text = re.sub('<.*?>.*?</.*?>','',text)
            text = re.sub('\[(\S+?)\]\(\S+\)',r'[COLOR green]\1[/COLOR]\n',text)
            videoitem['info'] = {'plot':text,'cast':[(j['posts'][index]['uname'],j['posts'][index]['uqq'])],'genre':j['posts'][index]['tag'].strip().split(u' ')}
            videos.append(videoitem)  
    except ValueError:
        pass
    return videos
#5dm.tv
def get_5dmtv_categories():
    return [{'name':'新番时间表','link':'https://www.5dm.tv/timeline'},
            {'name':'连载新番','link':'https://www.5dm.tv/video/bangumi'},
            {'name':'完结番组','link':'https://www.5dm.tv/video/end'},
            {'name':'剧场•OVA','link':'https://www.5dm.tv/video/bgm/ova'}]

def get_5dmtv_videos(url,page):
    #爬视频列表的
    videos = []
    if int(page) != 1:
        url = url + '/page/' +str(page)
    html = get_html(url,cf=1)
    soup = BeautifulSoup(html, 'html.parser')
    vids = soup.find_all('div',class_='item-thumbnail')

    tips = soup.find_all('div',class_='qv_tooltip')
    
    for index in range(len(vids)):
        videoitem = {}
        title = vids[index].a.img['alt']

        videoitem['info'] = {'plot':re.sub('<.*?>','',tips[index]['title'].replace(title,''))}
        if vids[index].span:
            title += u' - ' + vids[index].span.text
        videoitem['name'] = title
        videoitem['href'] = vids[index].a['href']
        videoitem['thumb'] = 'https://www.5dm.tv' + vids[index].a.img['data-original']
        
        videos.append(videoitem)  
    return videos

def get_5dmtv_source(url):
    videos = []
    html = get_html(url,cf=1)
    soup = BeautifulSoup(html, 'html.parser')
    #sclist = []
    duopdict = {}
    if soup.find('iframe',id='player'):
        sourcelist = soup.find_all('tr')
        for index in range(len(sourcelist)):
            duopname = sourcelist[index].find('td',class_='multilink-title')
            duoplist = sourcelist[index].find_all('a',class_='multilink-btn')
            for index in range(len(duoplist)):
                duopdict[duoplist[index].text] = duoplist[index]['href']
            #sclist.append(duopdict)
    
            videoitem = {}
            videoitem['name'] = duopname.text
            videoitem['href'] = str(duopdict)
            videos.append(videoitem)

        tmp['bghtml'] = html
    else:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('错误提示', '视频不存在！404！AWSL！')
    return videos

def get_5dmtv_mp4info(url):
    rtext = tmp['bghtml']
    soup = BeautifulSoup(rtext, 'html.parser')
    infodict={}

    tag = soup.find('div',class_='item-tax-list')
    tags = tag.find_all('a')
    genres = []
    for index in range(len(tags)):
        genres.append(tags[index].text)
    infodict['genre'] = genres

    plot = soup.find('div',class_='item-content toggled')
    ptext = plot.p.text
    if plot.p.span:
        pspan = plot.p.span.text
        ptext = ptext.replace(pspan,'')
    infodict['plot'] = ptext

    return infodict

def get_5dmtv_mp4(url):
    html = get_html(url,cf=1)
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find('iframe',id='player'):
        apiurl = soup.find('iframe',id='player')
        mp4api = apiurl['src']
        html1 = get_html(mp4api,cf=1)
        mp4 = re.search('https?:\/\/..+\.mp4',html1).group()
        r = requests.head(mp4,stream=True)
        mp4 = r.headers['Location']
        # mp4 = get_html(mp4,mode='url')
        
        # str1 = html1.find('srcUrl={')
        # str2 = html1.find('window.cid=')
        # mp4 = html1[str1+15:str2-4]
        # dialog = xbmcgui.Dialog()
        # ok = dialog.ok('错误提示', mp4)
    else:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('错误提示', '视频不存在！404！AWSL！')
    return mp4

#clicli.co
def get_cliclico_categories():
    return [{'name':'番剧','link':'https://clicli.co/anime/'},
            {'name':'电影','link':'https://clicli.co/pd/2'},
            {'name':'美剧','link':'https://clicli.co/pd/3'},
            {'name':'国漫','link':'https://clicli.co/pd/4'}]

def get_cliclico_videos(url,page):
    #爬视频列表的
    videos = []
    html = get_html(url)
    soup = BeautifulSoup(html,'html.parser')
    
    ullist = soup.find('div',class_='anime-list')
    videolist = ullist.find_all('a')
    for index in range(len(videolist)):
        videoitem = {}
        videoitem['name'] =  videolist[index].li.p.text
        videoitem['thumb'] =  videolist[index].li.img['data-echo']
        videoitem['href'] = 'https://clicli.co' + videolist[index]['href']
        videos.append(videoitem)
    return videos

def get_cliclico_source(url):
    videos = []
    av = re.search('av\d+',url).group()
    data = str({'av':av,'uas':'no'})
    html = post_html('https://api.clicli.co/anime/index',data)
    # dialog = xbmcgui.Dialog()
    # dialog.textviewer('错误提示', str(av) + '\n' + str(html.encode('utf-8')))
    sclist = []

    j = json.loads(html)
    try:
        duopdict = {}
        for index in range(len(j['epi'])):
            title = j['epi'][index]['title']
            if j['epi'][index]['name'] != '':
                title += ' - '+j['epi'][index]['name']
            duopdict[title] = 'https://clicli.co/player/anime.php?av=' + av + '&num=' + str(j['epi'][index]['num'])
        sclist.append(duopdict)
    except IndexError:
        pass
    
    videoitem = {}
    videoitem['name'] = '播放线路1'
    videoitem['href'] = str(sclist[0])
    videos.append(videoitem)

    tmp['bghtml'] = html
    return videos

def get_cliclico_mp4(url):
    r = get_html(url)
    soup = BeautifulSoup(r,'html.parser')
    mp4 = soup.find('e-player')
    return mp4['src']

def get_cliclico_search(keyword,page):
    videos = []
    url = 'https://clicli.co/search?key=' +keyword
    html = get_html(url)
    soup = BeautifulSoup(html,'html.parser')
    
    ullist = soup.find('div',class_='cards')
    videolist = ullist.find_all('a')
    for index in range(len(videolist)):
        videoitem = {}
        videoitem['name'] =  videolist[index].li.p.text
        videoitem['thumb'] =  videolist[index].li.img['data-echo']
        videoitem['href'] = 'https://clicli.co' + videolist[index]['href']
        videos.append(videoitem)
    return videos

#zzzfun
def zzzfun_fuckddos(url):
    r = get_html(url)
    if re.search('(?<=location.href = ).*?(?=;)',r.encode('utf-8')):
        purl = re.search('(?<=location\.href = ).*?(?=;)',r.encode('utf-8')).group()
        # dialog = xbmcgui.Dialog()
        # dialog.textviewer('错误提示', str(purl))
        try:
            purl = eval(purl)
            r = get_html('http://www.zzzfun.com' + purl)
        except:
            pass
    return r

def get_zzzfun_categories():
    return [{'name':'本季新番','link':'http://www.zzzfun.com/vod-type-id-42'},
            {'name':'日本动漫','link':'http://www.zzzfun.com/vod-type-id-1'},
            {'name':'剧场版','link':'http://www.zzzfun.com/vod-type-id-3'},
            {'name':'影视剧','link':'http://www.zzzfun.com/vod-type-id-4'}]

def get_zzzfun_videos(url,page):
    #爬视频列表的
    videos = []
    if int(page) != 1:
        url += '-page-' + str(page)
    url += '.html'
    html = zzzfun_fuckddos(url)

    soup = BeautifulSoup(html,'html.parser')
    
    ullist = soup.find('ul',class_='search-result')
    videolist = ullist.find_all('a')
    for index in range(len(videolist)):
        videoitem = {}
        videoitem['name'] =  videolist[index].find('div',class_='title-big').text
        videoitem['thumb'] =  videolist[index].find('img')['src']
        videoitem['href'] = 'http://www.zzzfun.com' + videolist[index]['href']
        videoitem['info'] = {'plot':videolist[index].find('div',class_='d-descr').text}
        videos.append(videoitem)
    return videos

def get_zzzfun_source(url):
    videos = []
    html = zzzfun_fuckddos(url)
    soup = BeautifulSoup(html,'html.parser')
    
    duoplist = soup.find('div',class_='tag-slider').find_all('ul')
    eplist = soup.find('div',class_='episode-wrap').find_all('ul')
    # dialog = xbmcgui.Dialog()
    # dialog.textviewer('错误提示', str(av) + '\n' + str(html.encode('utf-8')))
    sclist = []
    
    for index in range(len(duoplist)):
        duopdict = {}
        epli = eplist[index].find_all('li')
        for i in range(len(epli)):
            duopdict[epli[i].a.span.text] = 'http://www.zzzfun.com' + epli[i].a['href']
        sclist.append(duopdict)

        videoitem = {}
        videoitem['name'] = duoplist[index].li.span.text
        videoitem['href'] = str(sclist[index])
        videos.append(videoitem)
    tmp['bghtml'] = html
    return videos

def get_zzzfun_mp4info(url):
    infodict={}
    html = tmp['bghtml']
    soup = BeautifulSoup(html,'html.parser')
    base = soup.find('div',class_='info-content')
    title = base.find('div',class_='content-head').h1.text
    infodict['title'] = title
    info = base.find('div',class_='info-descr')
    infodict['plot'] = info.text

    text = base.find('div',class_='content-count').find_all('span',class_='count-item')
    for index in range(len(text)):
        span = text[index].text.split(u':')
        if span[0].strip() == u'语言':
            infodict['country'] = span[1]
        if span[0].strip() == u'状态':
            infodict['status'] = span[1]
        if span[0].strip() == u'CV':
            cast = text[index].find_all('a')
            casts = []
            for i in range(len(cast)):
                casts.append((cast[i].text,u'CV'))

            infodict['cast'] = casts
    return infodict

def get_zzzfun_mp4(url):
    r = zzzfun_fuckddos(url)
    js = re.search(u'(?<=var player_data=).*?(?=</script>)',r.encode('utf-8')).group()
    j = json.loads(js)
    deco = base64.b64decode(j['url'])
    # dialog = xbmcgui.Dialog()
    # ok = dialog.ok('错误提示', deco)
    
    html = zzzfun_fuckddos('http://www.zzzfun.com/static/danmu/zone.php?' + unescape(deco))
    soup = BeautifulSoup(html,'html.parser')
    # dialog = xbmcgui.Dialog()
    # dialog.textviewer('错误提示',html.encode('utf-8'))
    mp4 = soup.find('source')['src']
    return mp4

def get_zzzfun_search(keyword,page):
    #爬视频列表的
    videos = []
    
    if int(page) == 1:
        url = 'http://www.zzzfun.com/vod-search.html?wd=' + keyword
    else:
        url = 'http://www.zzzfun.com/vod-search-page-' + str(page) + '-wd-' + keyword + '.html'
    html = zzzfun_fuckddos(url)

    soup = BeautifulSoup(html,'html.parser')
    
    ullist = soup.find('ul',class_='show-list')
    videolist = ullist.find_all('li')
    for index in range(len(videolist)):
        videoitem = {}
        videoitem['name'] =  videolist[index].find('h2').text
        videoitem['thumb'] =  videolist[index].find('img')['src']
        videoitem['href'] = 'http://www.zzzfun.com' + videolist[index].a['href']
        videoitem['info'] = {'plot':videolist[index].find('dd',class_='juqing').p.text}
        videos.append(videoitem)
    return videos

#dmd8
def dmd8_fuckddos(url,data=''):
    if data == '':
        r = get_html(url)
    else:
        r = post_html(url,data)
    # dialog = xbmcgui.Dialog()
    # dialog.textviewer('错误提示', str(r.encode('utf-8')))
    if re.search('(?<=location.href = ).*?(?=;)',r.encode('utf-8')):
        purl = re.search('(?<=location\.href = ).*?(?=;)',r.encode('utf-8')).group()
        # dialog = xbmcgui.Dialog()
        # dialog.textviewer('错误提示', str(purl))
        try:
            purl = eval(purl)
            r = get_html('http://www.dmd8.com' + purl)
        except:
            pass
    return r

def get_dmd8_categories():
    return [{'name':'新番连载','link':'http://www.dmd8.com/type/1-'},
            {'name':'完结日漫','link':'http://www.dmd8.com/type/3-'},
            {'name':'热门国漫','link':'http://www.dmd8.com/type/4-'},
            {'name':'剧场动漫','link':'http://www.dmd8.com/type/16-'}]

def get_dmd8_videos(url,page):
    #爬视频列表的
    videos = []
    url += str(page) + '.html'
    html = dmd8_fuckddos(url)
    

    soup = BeautifulSoup(html,'html.parser')
    
    
    videolist = soup.find_all('div',class_='cn_box2')
    for index in range(len(videolist)):
        videoitem = {}
        videoitem['name'] =  videolist[index].find('a',class_='B font_16').text
        videoitem['thumb'] =  videolist[index].find('img')['src']
        videoitem['href'] = 'http://www.dmd8.com' + videolist[index].find('a',class_='B font_16')['href']
        videos.append(videoitem)
    return videos

def get_dmd8_source(url):
    videos = []
    html = dmd8_fuckddos(url)
    soup = BeautifulSoup(html,'html.parser')

    eplist = soup.find_all('ul',class_='mn_list_li_movie')
    # dialog = xbmcgui.Dialog()
    # dialog.textviewer('错误提示', str(av) + '\n' + str(html.encode('utf-8')))
    sclist = []
    
    for index in range(len(eplist)):
        duopdict = {}
        epli = eplist[index].find_all('li')
        for i in range(len(epli)):
            duopdict[epli[i].a.text] = 'http://www.dmd8.com' + epli[i].a['href']
        sclist.append(duopdict)

        videoitem = {}
        videoitem['name'] = '线路'+str(index+1)
        videoitem['href'] = str(sclist[index])
        videos.append(videoitem)
    tmp['bghtml'] = html
    return videos

# def get_dmd8_mp4info(url):
#     infodict={}
#     html = tmp['bghtml']
#     soup = BeautifulSoup(html,'html.parser')
#     base = soup.find('div',class_='info-content')
#     title = base.find('div',class_='content-head').h1.text
#     infodict['title'] = title
#     info = base.find('div',class_='info-descr')
#     infodict['plot'] = info.text

#     text = base.find('div',class_='content-count').find_all('span',class_='count-item')
#     for index in range(len(text)):
#         span = text[index].text.split(u':')
#         if span[0].strip() == u'语言':
#             infodict['country'] = span[1]
#         if span[0].strip() == u'状态':
#             infodict['status'] = span[1]
#         if span[0].strip() == u'CV':
#             cast = text[index].find_all('a')
#             casts = []
#             for i in range(len(cast)):
#                 casts.append((cast[i].text,u'CV'))

#             infodict['cast'] = casts
#     return infodict

def get_dmd8_mp4(url):
    r = dmd8_fuckddos(url)
    maccms = unescape(re.search(u'(?<=mac_url\=unescape\(\').*?(?=\'\);)',r.encode('utf-8')).group())
    rmac = re.search('(?<=-)([0-9]+)-([0-9]+)(?=.html)',url)
    duopnum = int(rmac.group(1))
    pnum = int(rmac.group(2))
    if re.search('$$$',maccms):
        duopall=maccms.split('$$$')
        duop = duopall[duopnum-1]
        duop = duop.split('#')
    else:
        duop = maccms.split('#')

    mp4 = duop[pnum-1].split('$')[1]
    if mp4[:4] != 'http':
        mp4 = re.search('[0-9]{4}_[0-9a-z]+',mp4).group()
        r = dmd8_fuckddos('http://www.dmd8.com/kongjian/?url=' + mp4)
        mp4 = re.search('(?<=var url = \').*?(?=\';)',r).group()
    #     dialog = xbmcgui.Dialog()
    #     ok = dialog.textviewer('错误提示', mp4)
    
    # dialog = xbmcgui.Dialog()
    # ok = dialog.textviewer('错误提示', mp4)
    return mp4

def get_dmd8_search(keyword,page):
    #爬视频列表的
    videos = []
    
    if int(page) == 1:
        url = 'http://www.dmd8.com/index.php?m=vod-search'
        html = dmd8_fuckddos(url,str({'wd':keyword}))
    else:
        url = 'http://www.dmd8.com/search-pg-' + str(page) + '-wd-'+ keyword + '.html'
        html = dmd8_fuckddos(url)
    dialog = xbmcgui.Dialog()
    ok = dialog.textviewer('错误提示', html)
    soup = BeautifulSoup(html,'html.parser')
    
    
    videolist = soup.find_all('div',class_='cn_box2')
    for index in range(len(videolist)):
        videoitem = {}
        videoitem['name'] =  videolist[index].find('a',class_='B font_16').text
        videoitem['thumb'] =  videolist[index].find('img')['src']
        videoitem['href'] = 'http://www.dmd8.com' + videolist[index].find('a',class_='B font_16')['href']
        videos.append(videoitem)
    return videos
##########################################################
###以下是核心代码区，看不懂的请勿修改
##########################################################

@plugin.route('/play/<name>/<url>/<mode>/')
def play(name,url,mode):
    items = []
    mp4 = get_mp4_mode(url,mode)
    #head = '|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
    try:
        mp4info = get_mp4info_mode(url,mode)
        mp4info['mediatype'] = 'video'
        item = {'label': name,'path':mp4,'is_playable': True,'info':mp4info,'info_type':'video','thumbnail': tmp['bgimg'],'icon': tmp['bgimg']}
    except NameError:
        item = {'label': name,'path':mp4,'is_playable': True,'info_type':'video','thumbnail': tmp['bgimg'],'icon': tmp['bgimg']}
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
                if get_categories()[index]['link'] in damakulist:
                    vlist['name'] = '[COLOR pink]' + get_categories()[index]['name'] + '[/COLOR]'
                else:
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
                if get_categories()[index]['link'] in damakulist:
                    vlist['name'] = '[COLOR pink]' + get_categories()[index]['name'] + '[/COLOR]'
                else:
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
    # items.append({
    #     'label': '繁体模式 - 开启可能会造成弹幕插件自动搜索失效 (状态:'+chushihua('jf',0) +')',
    #     'path': plugin.url_for('switch',key='jf'),
    # })
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
