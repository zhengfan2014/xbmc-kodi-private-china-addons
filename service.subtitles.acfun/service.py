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
import random
import string



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

ZIMUZU_BASE = 'https://www.acfun.cn/rest/pc-direct'


UserAgent  = 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)'

def log(module, msg):
    xbmc.log((u"%s::%s - %s" % (__scriptname__,module,msg,)).encode('utf-8'),level=xbmc.LOGDEBUG )

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
    url = ZIMUZU_BASE + '/search/bgm?keyword=%s' % (urllib.quote(search_string))
    data = GetHttpData(url)
    try:
        j = json.loads(data)
    except:
        return
    
    #番剧
    if 'bgmList' in j:
        bgm = j['bgmList']
        for index in range(len(bgm)):
            subtitles_list.append({"language_name":"Chinese", "filename":'[COLOR pink][' + bgm[index]['episodeInfo'] + '] ' + bgm[index]['bgmTitle'] + '[/COLOR]', "link":'https://www.acfun.cn/bangumi/aa' + str(bgm[index]['id']), "language_flag":'zh', "rating":"0"})
    
    url = ZIMUZU_BASE + '/search/video?keyword=%s' % (urllib.quote(search_string))
    data = GetHttpData(url)
    try:
        j = json.loads(data)
    except:
        return
    #视频
    if 'videoList' in j:
        k = j['videoList']
        for index in range(len(k)):
            subtitles_list.append({"language_name":"Chinese", "filename":k[index]['title'], "link":'https://www.acfun.cn/v/ac' + str(k[index]['id']), "language_flag":'zh', "rating":"0"})
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
    b = 1
    if b == 1:
        #data = GetHttpData(url)
        if re.match('https://',url) == None:
            if re.match('http://',url) != None:
                url = 'https://'+url[7:]
            else:
                dialog = xbmcgui.Dialog()
                ok = dialog.ok('错误提示', '非法url')

        ifbangumiurl = re.match('https://www.acfun.cn/bangumi/aa',url)
        ifvideourl = re.match('https://www.acfun.cn/v/ac',url)
        if ifbangumiurl or ifvideourl != None:
            if ifbangumiurl != None:
                r = GetHttpData(url)
                str1 = r.find('window.bangumiList = ')
                str2 = r.find('window.abtestConfig =')
                cutjson = r[str1+21:str2]
                cutjson = cutjson.split(';')[0]
                dialog = xbmcgui.Dialog()
                dialog.textviewer('错误提示', str(cutjson))
                j = json.loads(cutjson)
        
                titles = []
                cids = []
                for p in range(len(j['items'])):
                    titles.append(u'正片 - ' + j['items'][p]['episodeName'])
                    cids.append(j['items'][p]['videoId'])

            if ifvideourl != None:
                r = GetHttpData(url)
                str1 = r.find('window.pageInfo = window.videoInfo = ')
                str2 = r.find('window.videoResource =')
                cutjson = r[str1+37:str2]
                cutjson = cutjson.split(';')[0]
                dialog = xbmcgui.Dialog()
                dialog.textviewer('错误提示', str(cutjson))
                j = json.loads(cutjson)
                #bvid = j['data']['pages'][0]['bvid']
                titles = []
                cids = []
                for p in range(len(j['videoList'])):
                    titles.append(j['videoList'][p]['title'])
                    cids.append(j['videoList'][p]['id'])
            if len(titles) > 1:
                sel = xbmcgui.Dialog().select('请选择分集的字幕', titles)
                if sel == -1:
                    sel = 0
            else:
                sel = 0
        apiheaders = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
      'cookie':'_did=web_471136585E37DE05; uuid=00ac251daba2fd89f2cef9937df1662b; analytics=GA1.2.979500629.1590051501; ac__avi=101092823893b8e326abdc90e6850ae2886d0cde88b81067851cf6c2c6febafe3a364146315ef65213; Hm_lvt_2af69bc2b378fb58ae04ed2a04257ed1=1589465669,1590051312,1590243605,1590284267; sign_remind=1; csrfToken=oUoc3WbPlM29zqGXhVNsi7Vb; session_id=4045767301B5686B; webp_supported=%7B%22lossy%22%3Atrue%2C%22lossless%22%3Atrue%2C%22alpha%22%3Atrue%2C%22animation%22%3Atrue%7D; lsv_js_player_v1_main=f2c6e6; lsv_js_player_v2_main=9fa1b0; clientlanguage=zh_CN; safety_id=AAJHfMhNHgUr-jBjMz48azvJ; cur_req_id=5488657659848AC3_self_93a47343167a440b05e5119c339296db; cur_group_id=5488657659848AC3_self_93a47343167a440b05e5119c339296db_0'}
        apidata = {'videoId':cids[sel],'lastFetchTime':0}
        r = requests.post('https://www.acfun.cn/rest/pc-direct/new-danmaku/poll',apidata,headers=apiheaders)
        r.encoding = 'utf-8'
        r = r.text
        j = json.loads(r)

        data = '<?xml version=\"1.0\" encoding=\"UTF-8\"?><i><chatserver>chat.bilibili.com</chatserver><chatid>72540443</chatid><mission>0</mission><maxlimit>%d</maxlimit><state>0</state><real_name>0</real_name><source>e-r</source>' % (len(j['added']))
        # str1 = r.find('\"added\":[')
        # str2 = r.find('],\"host-name\"')
        # data = '{' + r[str1+8:str2] + ']}'
        for i in range(len(j['added'])):
            data += '<d p=\"' + str(float(j['added'][i]['position'])/float(1000)) #弹幕开始显示时间
            if re.search('.\d+,',data):
                if len(re.search('.\d+,',data).group()[1:-1]) < 5:
                    data += '0'*(5 - len(re.search('.\d+,',data).group()[1:-1]))
                
            data += ','
            data += str(j['added'][i]['mode']) + ',' #模式
            data += str(j['added'][i]['size']) + ',' #字体
            data += str(j['added'][i]['color']) + ',' #颜色
            data += str(int(float(j['added'][i]['createTime'])/1000)) + ',' #时间戳 acfun 13位-> b站 10位
            data += '0' + ',' #弹幕池 b站特有
            data += hex(j['added'][i]['userId'])[2:] + ',' #发送者id b站特有
            data += str(j['added'][i]['danmakuId']) #弹幕在数据库的rowid,b站特有
            data += '\">' + j['added'][i]['body'] + '</d>'
        data += '</i>'

        dialog = xbmcgui.Dialog()
        dialog.textviewer('错误提示', str(data.encode('utf-8')))
        #data = r
        # if data['info'] != 'OK':
        #     return []
        # url = data['data']['info']['file']
        # data = GetHttpData(url)
    #except:
        #return []
    if len(data) < 1024:
        return []
    # t = time.time()
    
    # ts = time.strftime("%Y%m%d%H%M%S",time.localtime(t)) + str(int((t - int(t)) * 1000))
    tmpfile = os.path.join(__temp__, "cid%s%s.ass" % (str(cids[sel]), os.path.splitext(url)[1])).replace('\\','/')
    dialog = xbmcgui.Dialog()
    dialog.textviewer('错误提示', str(tmpfile))
    with open(tmpfile, "wb") as subFile:
        subFile.write(data.encode('utf-8'))

    xbmc.sleep(500)
    xml2ass.Danmaku2ASS(tmpfile,tmpfile,960,540,duration_marquee=10.0)

    # archive = urllib.quote_plus(tmpfile)
    # if data[:4] == 'Rar!':
    #     path = 'rar://%s' % (archive)
    # else:
    #     path = 'zip://%s' % (archive)
    # dirs, files = xbmcvfs.listdir(path)
    # if ('__MACOSX') in dirs:
    #     dirs.remove('__MACOSX')
    # if len(dirs) > 0:
    #     path = path + '/' + dirs[0].decode('utf-8')
    #     dirs, files = xbmcvfs.listdir(path)
    # list = []
    # for subfile in files:
    #     if (os.path.splitext( subfile )[1] in exts):
    #         list.append(subfile.decode('utf-8'))
    # if len(list) == 1:
    #     subtitle_list.append(path + '/' + list[0])
    # elif len(list) > 1:
    #     sel = xbmcgui.Dialog().select('请选择压缩包中的字幕', list)
    #     if sel == -1:
    #         sel = 0
    #     subtitle_list.append(path + '/' + list[sel])
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
