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
def get_html(url,ua='pc',cf='',mode='html'):
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
        r.encoding = 'utf-8'
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
        r.encoding = 'utf-8'
        if mode == 'url':
            html = r.url
        else:
            html = r.text
    return html

@plugin.cached(TTL=2)
def post_html(url,data,ua='pc',cf=''):
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
        r.encoding = 'utf-8'
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

##########################################################
###主入口
##########################################################

def get_categories():
    return [{'id':1,'name':'喜欢看影视(138vcd.com)','link':'138vcd','author':'zhengfan2014','upload':'2020-5-7','videos':48}]

##########################################################
###以下是模块，网站模块请粘贴在这里面
##########################################################

#138vcd
def get_138vcd_categories():
    return [{"name": "电影", "link": "https://www.138vcd.com/vodshow/id/20"},
          {"name": "连续剧", "link": "https://www.138vcd.com/vodshow/id/21"}, 
          {"name": "综艺", "link": "https://www.138vcd.com/vodshow/id/22"}, 
          {"name": "动漫", "link": "https://www.138vcd.com/vodshow/id/23"},
          {"name": "纪录片", "link": "https://www.138vcd.com/vodshow/id/24"}]

def get_138vcd_videos(url,page):
    videos = []
    if page == 1:
        r = get_html(url + '/')
    else:
        r = get_html(url + '/page/' +str(page) +'.html')
    soup = BeautifulSoup(r, "html5lib")
    linelist = soup.find('ul',class_='myui-vodlist clearfix')
    alist = linelist.find_all('a',class_='myui-vodlist__thumb lazyload')
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
    str1 = r.find('var player_data=')
    cut = r[str1:]
    mp4 = re.search('https?:..+\.mp4',cut).group()
    mp4 = mp4.replace('\\','')
    #dialog = xbmcgui.Dialog()
    #ok = dialog.ok('错误提示', mp4)
    return mp4

def get_138vcd_search(keyword,page):
    videos = []
    
    if page == 1:
        r = get_html('https://www.138vcd.com/vodsearch.html?wd='+keyword+'&submit=')
    else:
        r = get_html('https://www.138vcd.com/vodsearch/page/'+str(page)+'/wd/'+keyword+'.html')
    soup = BeautifulSoup(r, "html5lib")
    linelist = soup.find('ul',id='searchList')
    alist = linelist.find_all('a',class_='myui-vodlist__thumb img-lg-150 img-md-150 img-sm-150 img-xs-100 lazyload')
    for i in range(len(alist)):
        videoitem = {}
        videoitem['name'] =  alist[i]['title'] 
        videoitem['href'] =  'https://www.138vcd.com/' + alist[i]['href']
        videoitem['thumb'] = alist[i]['data-original']
        videos.append(videoitem)
    return videos



##########################################################
###以下是核心代码区，看不懂的请勿修改
##########################################################

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

if __name__ == '__main__':
    plugin.run()
