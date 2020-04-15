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

useragent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
tmp = plugin.get_storage('tmp')


def get_categories_mode(mode):
    if mode == 'bimibimi':
        item = get_bimibimi_categories()
    if mode == 'yhdm':
        item = get_yhdm_categories()
    if mode == 'age':
        item = get_age_categories()
    if mode == 'qm':
        item = get_qm_categories()
    if mode == 'nm':
        item = get_nm_categories()
    if mode == 'sili':
        item = get_sili_categories()
    if mode == '8':
        item = get_8_categories()
    if mode == 'srsg':
        item = get_srsg_categories()
    return item

def get_videos_mode(url,mode):
    if mode == 'bimibimi':
        item = get_bimibimi_videos(url)
    if mode == 'yhdm':
        item = get_yhdm_videos(url)
    if mode == 'age':
        item = get_age_videos(url)
    if mode == 'qm':
        item = get_qm_videos(url)
    if mode == 'nm':
        item = get_nm_videos(url)
    if mode == 'sili':
        item = get_sili_videos(url)
    if mode == '8':
        item = get_8_videos(url)
    if mode == 'srsg':
        item = get_srsg_videos(url)
    return item
def get_source_mode(url,mode):
    if mode == 'bimibimi':
        item = get_bimibimi_source(url)
    if mode == 'yhdm':
        item = get_yhdm_source(url)
    if mode == 'age':
        item = get_age_source(url)
    if mode == 'qm':
        item = get_qm_source(url)
    if mode == 'nm':
        item = get_nm_source(url)
    if mode == 'sili':
        item = get_sili_source(url)
    if mode == '8':
        item = get_8_source(url)
    if mode == 'srsg':
        item = get_srsg_source(url)
    return item
def get_mp4info_mode(mode):
    if mode == 'bimibimi':
        item = get_bimibimi_mp4info()                                  
    if mode == 'yhdm':
        item = get_yhdm_mp4info()
    if mode == 'age':
        item = get_age_mp4info()
    if mode == 'qm':
        item = get_qm_mp4info()
    if mode == 'nm':
        item = get_nm_mp4info()
    if mode == 'sili':
        item = get_sili_mp4info()
    if mode == '8':
        item = get_8_mp4info()
    if mode == 'srsg':
        item = get_srsg_mp4info()
    return item
def get_mp4_mode(url,mode):
    if mode == 'bimibimi':
        item = get_bimibimi_mp4(url)
    if mode == 'yhdm':
        item = get_yhdm_mp4(url)
    if mode == 'age':
        item = get_age_mp4(url)
    if mode == 'qm':
        item = get_qm_mp4(url)
    if mode == 'nm':
        item = get_nm_mp4(url)
    if mode == 'sili':
        item = get_sili_mp4(url)
    if mode == '8':
        item = get_8_mp4(url)
    if mode == 'srsg':
        item = get_srsg_mp4(url)
    return item


def get_categories():
    return [{'name':'哔咪哔咪(bimibimi.tv)','link':'bimibimi'},
            {'name':'樱花动漫(yhdm.tv)','link':'yhdm'},
            {'name':'Age动漫(agefans.tw)','link':'age'},
            {'name':'嘶哩嘶哩(silisili.me)','link':'sili'},
            {'name':'八重樱动漫(iafuns.com.com)','link':'8'},
            {'name':'番組計劃(anime.srsg.moe)','link':'srsg'},
            {'name':'Qinmei(qinmei.video)','link':'qm'},
            {'name':'柠萌瞬间(ningmoe.com)','link':'nm'}]

#bimibimi
def get_bimibimi_categories():
    return [{'name':'新番放送','link':'http://www.bimibimi.me/type/riman/'},
            {'name':'国产动漫','link':'http://www.bimibimi.me/type/guoman/'},
            {'name':'番组计划','link':'http://www.bimibimi.me/type/fanzu/'},
            {'name':'剧场动画','link':'http://www.bimibimi.me/type/juchang/'},
            {'name':'影视','link':'http://www.bimibimi.me/type/move/'}]

@plugin.cached(TTL=60)
def get_bimibimi_videos(url):
    #爬视频列表的
    videos = []
    r = requests.get(url,headers=headers)
    r.encoding = 'utf-8'
    #print(r.text)
    soup = BeautifulSoup(r.text, 'html.parser')
    linelist = soup.find('ul',class_='drama-module clearfix tab-cont')
    #print(len(linelist))
    alist = linelist.find_all('a',class_='img')
    plist = linelist.find_all('span',class_='fl')
    for i in range(len(alist)):
        videoitem = {}
        videoitem['name'] =  alist[i]['title'] + '[' + plist[i].text + ']' 
        videoitem['href'] =  'http://www.bimibimi.me' + alist[i]['href']
        videoitem['thumb'] = alist[i].img['data-original']
        videos.append(videoitem)
    return videos

@plugin.cached(TTL=60)
def get_bimibimi_source(url):
    #爬视频列表的
    videos = []
    r = requests.get(url,headers=headers)
    #print(r.text)
    soup = BeautifulSoup(r.text, 'html.parser')
    linelist = soup.find_all('div',class_='play_box')
    #print(len(linelist))

    sourcelist = []
    for index in range(len(linelist)):
        alist = linelist[index].find_all('a')
        duopdict = {}
        for i in range(len(alist)):
            duopdict[alist[i].text] = 'http://www.bimibimi.me/' + alist[i]['href']
        #print('------------'*30)
        sourcelist.append(duopdict)

    for index in range(len(sourcelist)):
        videoitem = {}
        videoitem['name'] = '播放线路' + str(index+1)
        videoitem['href'] = str(sourcelist[index])
        videos.append(videoitem)
    tmp['bghtml'] = r.text
    return videos

def get_bimibimi_mp4info():
    rtext = tmp['bghtml']
    soup = BeautifulSoup(rtext, 'html.parser')
    li = soup.find_all('li',class_='clearfix')
    infodict={}
    for index in range(len(li)):
        emtext = li[index].em.text
        emtext = emtext.encode('utf-8')
        emtext = emtext.replace('：','')
        print(emtext)
        if li[index].find_all('a'):
            a = li[index].find_all('a')
            if len(a) == 1:
                atex = a[0].text
                atex = atex.encode('utf-8')
                atext = atex
            else:
                atext = []
                for index in range(len(a)):
                    if a[index].text != '':
                        atex = a[index].text
                        atex = atex.encode('utf-8')
                        atext.append(atex)
        else:
            atex = li[index].text
            atex = atex.encode('utf-8')
            atex = atex.replace('：','')
            atex = atex.replace(emtext,'')
            atext = atex.strip()
        emtext = emtext.replace('提醒','status')
        emtext = emtext.replace('声优','cast')
        emtext = emtext.replace('类型','genre')
        emtext = emtext.replace('导演','writer')
        emtext = emtext.replace('开播','premiered')
        emtext = emtext.replace('年份','year')
        emtext = emtext.replace('地区','country')
        emtext = emtext.replace('更新','dateadded')
        emtext = emtext.replace('简介','plot')
        if atext != '':
            infodict[emtext] = atext

        

 
    return infodict

@plugin.cached(TTL=60)
def get_bimibimi_mp4(url):
    r = requests.get(url,headers=headers)
    rtext = r.text
    soup = BeautifulSoup(rtext, 'html.parser')
    #title = soup.find('title')
    str1 = rtext.find('var player_data=')
    str2 = rtext.find('</script><script type="text/javascript"')
    cutjson = rtext[str1+16:str2]
    #print(cutjson)
    j = json.loads(cutjson)
    #向接口发送请求
    if j['from']:
        if j['from'] == 'niux':
            apiurl = 'http://182.254.167.161/danmu/niux.php?id=' + j['url']
        else:
            apiurl = 'http://182.254.167.161/danmu/play.php?url=' + j['url']
        r = requests.get(apiurl,headers=headers)
        rtext = r.text
        #print(rtext)
        soup = BeautifulSoup(r.text, 'html.parser')
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

@plugin.cached(TTL=60)
def get_yhdm_videos(url):
    #爬视频列表的
    videos = []
    r = requests.get(url,headers=headers)
    r.encoding = 'utf-8'
    #print(r.text)
    soup = BeautifulSoup(r.text, 'html.parser')
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
        videos.append(videoitem)
    return videos

@plugin.cached(TTL=60)
def get_yhdm_source(url):
    #爬视频列表的
    videos = []
    r = requests.get(url,headers=headers)
    r.encoding = 'utf-8'
    #print(r.text)
    soup = BeautifulSoup(r.text, 'html.parser')
    linelist = soup.find('div',class_='main0')
    #print(len(linelist))
    li = linelist.find_all('li')

    sourcelist = []
    duopdict = {}
    for index in range(len(li)):
        duopdict[li[index].a.text] = 'http://www.yhdm.tv/' + li[index].a['href']
    #print('------------'*30)
    sourcelist.append(duopdict)

    
    videoitem = {}
    videoitem['name'] = '播放线路1'
    videoitem['href'] = str(sourcelist[0])
    videos.append(videoitem)
    tmp['bghtml'] = r.text
    return videos

def get_yhdm_mp4info():
    rtext = tmp['bghtml']
    soup = BeautifulSoup(rtext, 'html.parser')

    sinfo = soup.find('div',class_='sinfo')
    span = sinfo.find_all('span')
    info = soup.find('div',class_='info')
    infodict={}
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

@plugin.cached(TTL=60)
def get_yhdm_mp4(url):
    r = requests.get(url,headers=headers)
    rtext = r.text
    soup = BeautifulSoup(rtext, 'html.parser')
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
    else:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('错误提示','不受支持的播放链接')
    return rt

#agefan.tw
def get_age_categories():
    return [{'name':'每日推荐','link':'https://agefans.tw/recommend'},
            {'name':'最近更新','link':'https://agefans.tw/update'}]

@plugin.cached(TTL=60)
def get_age_videos(url):
    #爬视频列表的
    videos = []
    scraper = cfscrape.create_scraper()
    html = scraper.get(url).content
    soup = BeautifulSoup(html,'html.parser')
    #print(r.text)
    base = soup.find('ul')
    li = base.find_all('li')
    for index in range(len(li)):
        videoitem = {}
        videoitem['name'] =  li[index].a.img['alt']
        videoitem['thumb'] =  'http:' + li[index].a.img['src']
        videoitem['href'] = 'https://agefans.tw' + li[index].a['href']
        videos.append(videoitem)
    return videos

@plugin.cached(TTL=60)
def get_age_source(url):
    #爬视频列表的
    videos = []
    bak = url
    url = url.replace('detail','play')
    aid = re.search('[0-9]+',url).group()
    scraper = cfscrape.create_scraper()
    html = scraper.get(url).content
    #print(r.text)
    soup = BeautifulSoup(html, 'html.parser')
    base = soup.find('div',class_='baseblock2')
    sourcelist = base.find_all('div',class_='blockcontent')
    #print(len(sourcelist))
    sclist = []
    for index in range(len(sourcelist)):
        alist = sourcelist[index].find_all('a',class_='episode')
        #print('在線播放'+str(alist[0]['routeidx']))
        duopdict = {}
        for index in range(len(alist)):
            uri = 'https://agefans.tw/_getplay_2?animeid='+ str(aid)+ '&routeidx='+ str(alist[index]['routeidx'])+ '&episodeidx='+ str(alist[index]['episodeidx'])+ '&lhf='+ str(alist[index]['lhf'])+ '&sign='+ alist[index]['sign']+ '&num='+ str(random.random())
            duopdict[alist[index].text] = uri
        sclist.append(duopdict)
    #print('------------'*30)
    

    
    for index in range(len(sclist)):
        videoitem = {}
        videoitem['name'] = '播放线路' + str(index+1)
        videoitem['href'] = str(sclist[index])
        videos.append(videoitem)
    tmp['bghtml'] = html
    return videos

def get_age_mp4info():
    rtext = tmp['bghtml']
    infodict={}
    
    soup = BeautifulSoup(rtext, 'html.parser')
    table = soup.find('table')
    li = table.find_all('li')

    for index in range(len(li)):
        text = li[index].find('span',class_='play_imform_tag').text.strip() + li[index].find('span',class_='play_imform_val').text.strip()
        text = text.encode('utf-8')
        text = text.split('：')
        text[0] = text[0].replace('地區','country')
        text[0] = text[0].replace('標簽','tag')
        text[0] = text[0].replace('原版名稱','originaltitle')
        text[0] = text[0].replace('原作','writer')
        text[0] = text[0].replace('制作公司','studio')
        text[0] = text[0].replace('首播時間','premiered')
        text[0] = text[0].replace('播放狀態','status')
        text[0] = text[0].replace('劇情類型','genre')
        text[0] = text[0].replace('官方網站','showlink')
        if text[1]:
            if text[1].find(',') != -1:
                text[1] = text[1].split(',')
            infodict[text[0]] = text[1]
    pinfo = soup.find('div',class_='play_desc')
    infodict['plot'] =pinfo.p.text.strip()
    #dialog = xbmcgui.Dialog()
    #dialog.textviewer('错误提示',str(infodict))
    return infodict

@plugin.cached(TTL=60)
def get_age_mp4(url):
    scraper = cfscrape.create_scraper()
    html = scraper.get(url).content
    mp4 = unescape(html)
    if mp4[:2] == '//':
        mp4 = 'http:' + mp4
    if mp4.find('baidu.com') != -1:
        mp4 = re.search('https?:\/\/..+\.mp4',mp4).group()
    
    return mp4

#qinmei
def get_qm_categories():
    return [{'name':'新番','link':'https://qinmei.video/api/v2/animates?sortBy=updatedAt&sortOrder=-1&size=20&page=1'},
            {'name':'剧场版','link':'https://qinmei.video/api/v2/animates?sortBy=updatedAt&sortOrder=-1&size=20&page=1&kind=5e359428d1f1dc2e17f84fd4'},
            {'name':'战斗','link':'https://qinmei.video/api/v2/animates?sortBy=updatedAt&sortOrder=-1&size=20&page=1&kind=5e341fc1d1f1dc2e17f84fae'},
            {'name':'日常','link':'https://qinmei.video/api/v2/animates?sortBy=updatedAt&sortOrder=-1&size=20&page=1&kind=5e341fc8e7bc242e192d23cf'},
            {'name':'搞笑','link':'https://qinmei.video/api/v2/animates?sortBy=updatedAt&sortOrder=-1&size=20&page=1&kind=5e341fced1f1dc2e17f84faf'},
            {'name':'治愈','link':'https://qinmei.video/api/v2/animates?sortBy=updatedAt&sortOrder=-1&size=20&page=1&kind=5e341fd8e7bc242e192d23d0'},
            {'name':'致郁','link':'https://qinmei.video/api/v2/animates?sortBy=updatedAt&sortOrder=-1&size=20&page=1&kind=5e341fe7d1f1dc2e17f84fb0'},
            {'name':'异界','link':'https://qinmei.video/api/v2/animates?sortBy=updatedAt&sortOrder=-1&size=20&page=1&kind=5e341feed1f1dc2e17f84fb1'}]

@plugin.cached(TTL=60)
def get_qm_videos(url):
    #爬视频列表的
    videos = []
    r = requests.get(url,headers=headers)
    r.encoding = 'utf-8'
    #print(r.text)
    soup = BeautifulSoup(r.text, 'html.parser')

    j = json.loads(r.text)
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

@plugin.cached(TTL=60)
def get_qm_source(url):
    #爬视频列表的
    videos = []
    url = 'https://qinmei.video/api/v2/animates/' + url
    r = requests.get(url,headers=headers)
    r.encoding = 'utf-8'
    j = json.loads(r.text)
    sourcelist = []
    duopdict = {}
    for index in range(len(j['data']['eposides'])):
        duopdict[j['data']['eposides'][index]['title']] = j['data']['eposides'][index]['_id']
    sourcelist.append(duopdict)

    
    videoitem = {}
    videoitem['name'] = '播放线路1'
    videoitem['href'] = str(sourcelist[0])
    videos.append(videoitem)
    tmp['bghtml'] = r.text
    return videos

def get_qm_mp4info():
    rtext = tmp['bghtml']

    #t = json.dumps(r.text, ensure_ascii=False)  
    j = json.loads(rtext)
    infodict={}
#print(j['data']['status'])
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
            qqqq =1
    infodict['castandrole'] = actor
    infodict['premiered'] = str(j['data']['firstPlay'][:4]) + '-' +str(j['data']['firstPlay'][4:6]) + '-' +str(j['data']['firstPlay'][6:8])
    infodict['playcount'] = j['data']['countPlay']
    infodict['userrating'] = j['data']['rateStar']
    try:
        infodict['country'] = j['data']['area'][0]['name']
    except IndexError:
        qqqq =1
    try:
        infodict['year'] = j['data']['year'][0]['name']
    except IndexError:
        qqqq =1


    return infodict

@plugin.cached(TTL=60)
def get_qm_mp4(url):
    url = 'https://qinmei.video/api/v2/animates/' + url + '/play'
    r = requests.get(url,headers=headers)
    r.encoding = ('utf-8')
    rtext = r.text
    soup = BeautifulSoup(rtext, 'html.parser')
    j = json.loads(r.text)
    mp4 = j['data']['link'][0]['value']
    return mp4

#柠檬瞬间
def get_nm_categories():
    return [{'name':'本月热门','link':'https://www.ningmoe.com/api/get_hot_bangumi'}]

@plugin.cached(TTL=60)
def get_nm_videos(url):
    #爬视频列表的
    videos = []
    data = {'page': 1, 'limit': 50}
    r = requests.post(url,headers=headers,data=data)
    r.encoding = ('utf-8')
    j = json.loads(r.text)
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

@plugin.cached(TTL=60)
def get_nm_source(url):
    #爬视频列表的
    videos = []
    apiurl = 'https://www.ningmoe.com/api/get_bangumi'
    data = {'bangumi_id':url}
    r = requests.post(apiurl,headers=headers,data=data)
    r.encoding = ('utf-8')
    j = json.loads(r.text)
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
    tmp['bghtml'] = r.text
    return videos

def get_nm_mp4info():
    rtext = tmp['bghtml']
    infodict={}
    
    j = json.loads(rtext)
    vcount = j['data']['video_total_count']
    infodict['countPlay'] = int(vcount)
    vinfo = j['data']['bangumi']
    infodict['originaltitle'] = vinfo['en_name']
    infodict['plot'] = vinfo['description']
    infodict['premiered'] = vinfo['air_date']

    return infodict

@plugin.cached(TTL=60)
def get_nm_mp4(url):
    if url.find('kingsnug.cn') != -1:
        apiurl = 'https://www.ningmoe.com/api/get_real_yun_url'
        data = {'url':url}
        r = requests.post(apiurl,headers=headers,data=data)
        r.encoding = ('utf-8')
        j = json.loads(r.text)
        try:
            mp4 = j['data']['yun_url']
        except KeyError:
            dialog = xbmcgui.Dialog()
            ok = dialog.ok('错误提示','查询链接失败')
    else:
        mp4 = url
    return mp4

    #8chongying
def get_8_categories():
    return [{'name':'2020新番','link':'http://iafuns.com/catalog?year=2020'},
            {'name':'2019新番','link':'http://iafuns.com/catalog?year=2019'}]

@plugin.cached(TTL=60)
def get_8_videos(url):
    #爬视频列表的
    videos = []
    r = requests.get(url,headers=headers)
    r.encoding = ('utf-8')
    soup = BeautifulSoup(r.text, 'html.parser')
    li = soup.find_all('li',class_='col-lg-2 col-md-3 col-sm-3 col-4 st_col position-relative')
    for index in range(len(li)):
        videoitem = {}
        videoitem['name'] =  li[index].h6.text
        videoitem['href'] =  'http://iafuns.com' + li[index].a['href']
        videoitem['thumb'] = 'http:' + li[index].img['data-src']
        videos.append(videoitem)
    return videos

@plugin.cached(TTL=60)
def get_8_source(url):
    #爬视频列表的
    videos = []
    r = requests.get(url,headers=headers)
    r.encoding = ('utf-8')
    soup = BeautifulSoup(r.text, 'html.parser')
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
            duopdict[l[index]['ep_name']] = l[index]['play_cfg']+ ':' +l[index]['play_id']
        videoitem['href'] = str(duopdict)
        videos.append(videoitem)
  
    tmp['bghtml'] = r.text
    return videos

def get_8_mp4info():
    rtext = tmp['bghtml']
    infodict={}

    soup = BeautifulSoup(rtext, 'html.parser')
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
        if value.find(',') != -1:
            value = value.split(',')
        infodict[key] = value
    p = soup.find('span')
    infodict['plot'] = p.text

    return infodict

@plugin.cached(TTL=60)
def get_8_mp4(url):
    dialog = xbmcgui.Dialog()
    ok = dialog.ok('错误提示', url)
    url = url.split(':')
    if url[0][:2].find('qz') != -1:
        apiurl = 'http://iafuns.com/_get_e_i?url=' + url + '&quote=1'
    else:
        if url[0][:4].find('quan') != -1 or url[0][:3].find('mp4') != -1:
            apiurl = 'http://iafuns.com/_get_raw?id=' +url[1]
        else:
            dialog = xbmcgui.Dialog()
            ok = dialog.ok('错误提示', '不支持的视频格式，请向插件作者反馈 播放视频名字 和 播放线路')
    
    r = requests.get(apiurl,headers=headers)
    r.encoding = 'utf-8'

    if apiurl.find('_get_raw') != -1:
        if r.text[:2] == '//':
            mp4 = 'http:' + r.text
        mp4 = r.text
    if apiurl.find('_get_e_i') != -1:
        j = json.loads(r.text)
        mp4 = j['result']

    
    
    
    dialog = xbmcgui.Dialog()
    ok = dialog.ok('错误提示',mp4)
    return mp4

#斯利斯利
def get_sili_categories():
    return [{'name':'最新更新','link':'http://www.silisili.me/zxgx.html'},
            {'name':'日本动漫','link':'http://www.silisili.me/riyu/'},
            {'name':'国产动漫','link':'http://www.silisili.me/guoyu/'}]

@plugin.cached(TTL=60)
def get_sili_videos(url):
    #爬视频列表的
    videos = []
    r = requests.get(url,headers=headers)
    r.encoding = ('utf-8')
    soup = BeautifulSoup(r.text, 'html.parser')
    if url == 'http://www.silisili.me/zxgx.html':
        #
        li = soup.find_all('div',class_='ggwp')
        for index in range(len(li)):
            videoitem = {}
            videoitem['name'] =  li[index].a['title']
            videoitem['href'] =  'http://www.silisili.me'+li[index].a['href']
            videoitem['thumb'] = li[index].a.img['src']
            videos.append(videoitem)
    else:
        base = soup.find('div',class_='anime_list')
        li = base.find_all('dl')
        for index in range(len(li)):
            videoitem = {}
            videoitem['name'] =  li[index].dd.h3.text
            videoitem['href'] =  'http://www.silisili.me'+li[index].dt.a['href']
            videoitem['thumb'] = li[index].dt.a.img['src']
            videos.append(videoitem)
    
    return videos

@plugin.cached(TTL=60)
def get_sili_source(url):
    #爬视频列表的
    videos = []
    
    
    r = requests.get(url,headers=headers)
    r.encoding = ('utf-8')
    soup = BeautifulSoup(r.text, 'html.parser')
    base = soup.find('div',class_='swiper-slide')
    li = base.find_all('li')
    sourcelist = []
    duopdict = {}
    for index in range(len(li)):
        duopdict[li[index].a.em.span.text] = 'http://www.silisili.me' + li[index].a['href']

    sourcelist.append(duopdict)
    videoitem = {}
    videoitem['name'] = '播放线路1'
    videoitem['href'] = str(sourcelist[0])
    videos.append(videoitem)
    tmp['bghtml'] = r.text
    return videos

def get_sili_mp4info():
    rtext = tmp['bghtml']
    infodict={}
    soup = BeautifulSoup(rtext, 'html.parser')
    base = soup.find('div',class_='detail con24 clear')
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

@plugin.cached(TTL=60)
def get_sili_mp4(url):
    r = requests.get(url,headers=headers)
    r.encoding = ('utf-8')
    soup = BeautifulSoup(r.text, 'html.parser')
    mp4 = soup.find('iframe')
    mp4 = mp4['src'].split('?')
    return mp4[1]

#srsg
def get_srsg_categories():
    return [{'name':'每日推荐','link':'https://anime.srsg.moe/api/carousel'},
            {'name':'新番表(无图)','link':'https://anime.srsg.moe/api/timeline'}]

@plugin.cached(TTL=60)
def get_srsg_videos(url):
    #爬视频列表的
    videos = []
    scraper = cfscrape.create_scraper()
    html = scraper.get(url).content
    if url == 'https://anime.srsg.moe/api/timeline':
        j = json.loads(html)
        
        for index in range(len(j)):
            videoitem = {}
            videoitem['name'] = j[index]['title']
            videoitem['thumb'] = 'https://anime.srsg.moe/api/resource/'+j[index]['cover_h']
            videoitem['href'] = j[index]['bangumi_id']
            videos.append(videoitem)
    else:
        j = json.loads(html)
        for index in range(len(j['result'])):
            videoitem = {}
            videoitem['name'] = j['result'][index]['title']
            videoitem['thumb'] =  'https://tzz1ekxz.fantasy-love.top/'+j['result'][index]['cover_src']
            videoitem['href'] = re.search('\d+',j['result'][index]['link']).group()
            videos.append(videoitem)
        scraper = cfscrape.create_scraper()
        html = scraper.get('https://anime.srsg.moe/api/recommend?pageNo=1&pageSize=50').content
        j = json.loads(html)
        for index in range(len(j['result'])):
            videoitem = {}
            videoitem['name'] = j['result'][index]['title']
            videoitem['thumb'] =  'https://tzz1ekxz.fantasy-love.top/'+j['result'][index]['cover_v']
            videoitem['href'] = j['result'][index]['id']
            videos.append(videoitem)
    return videos

@plugin.cached(TTL=60)
def get_srsg_source(url):
    #爬视频列表的
    videos = []
    scraper = cfscrape.create_scraper()
    html = scraper.get('https://anime.srsg.moe/api/episodes/' +url).content


    j = json.loads(html)
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
    html = scraper.get('https://anime.srsg.moe/api/bangumi/' +url).content
    tmp['bghtml'] = html
    return videos

def get_srsg_mp4info():
    rtext = tmp['bghtml']
    infodict={}
    
    j = json.loads(rtext)
    infodict['title'] =j['title']
    infodict['plot'] =j['description']
    tmp['bgimg'] ='https://tzz1ekxz.fantasy-love.top/'+j['cover_v_src']
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

@plugin.cached(TTL=60)
def get_srsg_mp4(url):
    scraper = cfscrape.create_scraper()
    html = scraper.get('https://anime.srsg.moe/api/ep/' + url).content
    j = json.loads(html)
    mp4 = 'https://cdn-animetv-sgp.srsg.moe/' + j['parts'][0]['resources']['path'][:-3]+ 'm3u8'
    return mp4

@plugin.route('/play/<name>/<url>/<mode>/')
def play(name,url,mode):
        
        items = []
        #print(rec.text)
        mp4 = get_mp4_mode(url,mode)
        #json_string=json.dumps(get_mp4info_mode(mode))
        #mp4info = json.loads(json_string)
        mp4info = get_mp4info_mode(mode)
        mp4info['mediatype'] = 'video'
        mp4info['title'] = name

        #dialog = xbmcgui.Dialog()
        #ok = dialog.ok('错误提示',str(mp4info).encode('utf-8'))
        #print(mp4['src'])
        item = {'label': name,'path':mp4,'is_playable': True,'info':mp4info,'info_type':'video','thumbnail': tmp['bgimg'],'icon': tmp['bgimg']}
        items.append(item)
        return items

@plugin.route('/duop/<name>/<list>/<mode>/')
def duop(name,list,mode):
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', list)
    
    
    list = eval(list)
    #j = json.loads(list)
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', str(len(list)))
    kongge = ' - '
    kongge = kongge.encode('utf-8')
    items = []
    for k,i in list.items():
        item = {'label':k.encode('utf-8'),'path':plugin.url_for('play',name=k.encode('utf-8')+ kongge +name,url= i,mode=mode)}
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

@plugin.route('/category/<name>/<url>/<mode>/')
def category(name,url,mode):
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', url)
    
    videos = get_videos_mode(url,mode)
    
    items = [{
        'label': video['name'],
        'path': plugin.url_for('source', name=video['name'].encode('utf-8'),url=video['href'],img=video['thumb'], mode=mode),
	'thumbnail': video['thumb'],
        'icon': video['thumb'],
    } for video in videos]

    sorted_items = items
    #sorted_items = sorted(items, key=lambda item: item['label'])
    return sorted_items


@plugin.route('/home/<mode>/')
def home(mode):
    categories = get_categories_mode(mode)
    items = [{
        'label': category['name'],
        'path': plugin.url_for('category', name=category['name'] , url=category['link'],mode=mode),
    } for category in categories]

    
    return items

@plugin.route('/')
def index():
    categories = get_categories()
    items = [{
        'label': category['name'],
        'path': plugin.url_for('home',  mode=category['link']),
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
