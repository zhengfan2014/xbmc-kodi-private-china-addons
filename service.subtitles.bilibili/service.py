# -*- coding: utf-8 -*-

import os
import sys
import xbmc
import urllib
import urllib2
import json
import xbmcvfs
import requests
import xbmcaddon
import xbmcgui,xbmcplugin
import re
from bs4 import BeautifulSoup
import time



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
import xml2ass

ZIMUZU_BASE = 'https://api.bilibili.com'

ZIMUZU_API = ZIMUZU_BASE + '/x/web-interface/search/all/v2?keyword=%s'
UserAgent  = 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)'

def log(module, msg):
    pass
    # xbmc.log((u"%s::%s - %s" % (__scriptname__,module,msg,)).decode('utf-8'),level=xbmc.LOGDEBUG )

def GetHttpData(url, data=''):
    log(sys._getframe().f_code.co_name, "url [%s]" % (url))
    if data:
        req = urllib2.Request(url, data)
    else:
        req = urllib2.Request(url)
    req.add_header('User-Agent', UserAgent)
    try:
        response = urllib2.urlopen(req)
        httpdata = response.read()
        response.close()
    except:
        log(sys._getframe().f_code.co_name, "Error (%d) [%s]" % (
               sys.exc_info()[2].tb_lineno,
               sys.exc_info()[1]
               ))
        return ''
    return httpdata

def Search( item ):
    subtitles_list = []

    log(sys._getframe().f_code.co_name, "Search for [%s] by name" % (os.path.basename( item['file_original_path'] )))
    if item['mansearch']:
        search_string = item['mansearchstr']
    elif len(item['tvshow']) > 0:
        search_string = "%s S%.2dE%.2d" % (item['tvshow'],
                                           int(item['season']),
                                           int(item['episode']),)
    else:
        search_string = item['title']
    #search_string = search_string.replace(' ','')
    # dialog = xbmcgui.Dialog()
    # dialog.textviewer('错误提示', search_string)
    if search_string.find('%') != -1:
        url = ZIMUZU_API % search_string
    else:
        url = ZIMUZU_API % urllib.quote(search_string)
    data = GetHttpData(url)
    try:
        j = json.loads(data)
    except:
        return
    
    #番剧
    bgm = j['data']['result'][3]['data']
    for index in range(len(bgm)):
        subtitles_list.append({"language_name":"Chinese", "filename":'[COLOR pink][' + bgm[index]['season_type_name'] + '] ' + bgm[index]['title'].replace('<em class="keyword">','').replace('</em>','') + '[/COLOR]', "link":'https://www.bilibili.com/bangumi/play/ss' + str(bgm[index]['season_id']), "language_flag":'zh', "rating":"0"})
    #影视
    mov = j['data']['result'][4]['data']
    for index in range(len(mov)):
        subtitles_list.append({"language_name":"Chinese", "filename":'[COLOR pink][' + mov[index]['season_type_name'] + '] ' +  mov[index]['title'].replace('<em class="keyword">','').replace('</em>','') + '[/COLOR]', "link":'https://www.bilibili.com/bangumi/play/ss' + str(mov[index]['season_id']), "language_flag":'zh', "rating":"0"})
    #视频
    k = j['data']['result'][8]['data']
    for index in range(len(k)):
        subtitles_list.append({"language_name":"Chinese", "filename":'[' + k[index]['typename'] + ']' + k[index]['title'].replace('<em class="keyword">','').replace('</em>',''), "link":'http://www.bilibili.com/video/' + k[index]['bvid'], "language_flag":'zh', "rating":"0"})
    # results = j['data']['result']
    # for it in results:
    #     link = ZIMUZU_BASE + it.find("div", class_="fl-info").a.get('href').encode('utf-8')
    #     title = it.find("strong", class_="list_title").text.encode('utf-8')
    #     subtitles_list.append({"language_name":"Chinese", "filename":title, "link":link, "language_flag":'zh', "rating":"0"})

    if subtitles_list:
        for it in subtitles_list:
            listitem = xbmcgui.ListItem(label=it["language_name"],
                                  label2=it["filename"],
                                  iconImage=it["rating"],
                                  thumbnailImage=it["language_flag"])
            listitem.setProperty( "sync", "false" )
            listitem.setProperty( "hearing_imp", "false" )

            url = "plugin://%s/?action=download&link=%s" % (__scriptid__,
                                                            it["link"]
                                                            )
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=listitem,isFolder=False)

def Download(url):
    if not xbmcvfs.exists(__temp__.replace('\\','/')):
        xbmcvfs.mkdirs(__temp__)
    dirs, files = xbmcvfs.listdir(__temp__)
    
    for file in files:
        xbmcvfs.delete(os.path.join(__temp__, file.decode("utf-8")))
    
    subtitle_list = []
    try:
        #data = GetHttpData(url)
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
                ssid = re.search(r'ss[0-9]+', url)
                ssid = ssid.group()
                ssid = ssid[2:]
                r = GetHttpData('http://api.bilibili.com/pgc/web/season/section?season_id=' + ssid)
                j = json.loads(r)
        
                titles = []
                cids = []
                for p in range(len(j['result']['main_section']['episodes'])):
                    titles.append(u'正片 - ' + j['result']['main_section']['episodes'][p]['title'])
                    cids.append(j['result']['main_section']['episodes'][p]['cid'])
                for index in range(len(j['result']['section'])):
                    duopname = j['result']['section'][index]['title']
                    for i in range(len(j['result']['section'][index]['episodes'])):
                        titles.append(duopname + u' - ' + j['result']['section'][index]['episodes'][i]['title'])
                        cids.append(j['result']['section'][index]['episodes'][i]['cid'])

            if ifvideourl != None:
                bvid = ''
                aid = ''
                if re.search(r'[Bb]{1}[Vv]{1}[a-zA-Z0-9]+', url):
                    bvid = re.search(r'[Bb]{1}[Vv]{1}[a-zA-Z0-9]+', url)
                    bvid = bvid.group()
                    vurl = 'https://api.bilibili.com/x/web-interface/view?bvid='+bvid
                if re.search('[aA]{1}[vV]{1}[0-9]+', url):
                    aid = re.search(r'[aA]{1}[vV]{1}[0-9]+', url)
                    aid = aid.group()
                    aid = aid[2:]
                    vurl = 'https://api.bilibili.com/x/web-interface/view?aid='+aid
                r = GetHttpData(vurl)
                j = json.loads(r)
                #bvid = j['data']['pages'][0]['bvid']
                titles = []
                cids = []
                for p in range(len(j['data']['pages'])):
                    titles.append(j['data']['pages'][p]['part'])
                    cids.append(j['data']['pages'][p]['cid'])
            if len(titles) > 1:
                sel = xbmcgui.Dialog().select('请选择分集的弹幕', titles)
                if sel == -1:
                    sel = 0
            else:
                sel = 0
        r = requests.get('https://api.bilibili.com/x/v1/dm/list.so?oid=' + str(cids[sel]))
        r.encoding = 'utf-8'
        data = r.text
        pDialog = xbmcgui.DialogProgress()
        pDialog.create('获取弹幕', '初始化...')
        pDialog.update(50, '获取弹幕成功...')
        # dialog = xbmcgui.Dialog()
        # dialog.textviewer('错误提示', str(data.encode('utf-8')))
    except:
        return []
    if len(data) < 1024:
        return []
    tmpfile = os.path.join(__temp__, "cid%s%s.ass" % (str(cids[sel]), os.path.splitext(url)[1])).replace('\\','/')
    # dialog = xbmcgui.Dialog()
    # dialog.textviewer('错误提示', str(tmpfile))
    with open(tmpfile, "wb") as subFile:
        subFile.write(data.encode('utf-8'))
    pDialog.update(75, '写入xml成功...')
    xbmc.sleep(500)
    xml2ass.Danmaku2ASS(tmpfile,tmpfile,960,540,duration_marquee=10.0)
    pDialog.update(100, '转换ass成功...')
    pDialog.close()
    subtitle_list.append(tmpfile)
    return subtitle_list

def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=paramstring
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]

    return param

params = get_params()
if params['action'] == 'search' or params['action'] == 'manualsearch':
    item = {}
    item['temp']               = False
    item['rar']                = False
    item['mansearch']          = False
    item['year']               = xbmc.getInfoLabel("VideoPlayer.Year")                           # Year
    item['season']             = str(xbmc.getInfoLabel("VideoPlayer.Season"))                    # Season
    item['episode']            = str(xbmc.getInfoLabel("VideoPlayer.Episode"))                   # Episode
    item['tvshow']             = xbmc.getInfoLabel("VideoPlayer.TVshowtitle")                    # Show
    item['title']              = xbmc.getInfoLabel("VideoPlayer.OriginalTitle")                  # try to get original title
    item['file_original_path'] = urllib.unquote(xbmc.Player().getPlayingFile().decode('utf-8'))  # Full path of a playing file
    item['3let_language']      = []

    if 'searchstring' in params:
        item['mansearch'] = True
        item['mansearchstr'] = params['searchstring']

    for lang in urllib.unquote(params['languages']).decode('utf-8').split(","):
        item['3let_language'].append(xbmc.convertLanguage(lang,xbmc.ISO_639_2))

    if item['title'] == "":
        item['title']  = xbmc.getInfoLabel("VideoPlayer.Title")                       # no original title, get just Title
        if item['title'] == os.path.basename(xbmc.Player().getPlayingFile()):         # get movie title and year if is filename
            title, year = xbmc.getCleanMovieTitle(item['title'])
            item['title'] = title.replace('[','').replace(']','')
            item['year'] = year

    if item['episode'].lower().find("s") > -1:                                        # Check if season is "Special"
        item['season'] = "0"                                                          #
        item['episode'] = item['episode'][-1:]

    if ( item['file_original_path'].find("http") > -1 ):
        item['temp'] = True

    elif ( item['file_original_path'].find("rar://") > -1 ):
        item['rar']  = True
        item['file_original_path'] = os.path.dirname(item['file_original_path'][6:])

    elif ( item['file_original_path'].find("stack://") > -1 ):
        stackPath = item['file_original_path'].split(" , ")
        item['file_original_path'] = stackPath[0][8:]

    Search(item)

elif params['action'] == 'download':
    subs = Download(params["link"])
    for sub in subs:
        listitem = xbmcgui.ListItem(label=sub)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=sub,listitem=listitem,isFolder=False)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
