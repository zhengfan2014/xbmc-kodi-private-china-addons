# -*- coding: utf-8 -*-

import urllib2
import sys
import urlparse
import urllib
import os
import unicodedata
import xbmcgui
import xbmcplugin
import xbmc
import xbmcaddon
import xbmcvfs

ADDON = xbmcaddon.Addon()
SCRIPT_ID = ADDON.getAddonInfo('id')
PROFILE = xbmc.translatePath(ADDON.getAddonInfo('profile'))
TEMP = os.path.join(PROFILE, 'temp', '')
HANDLE = int(sys.argv[1])

# 创建一个文件夹，用于存储下载的字幕
if not xbmcvfs.exists(TEMP):
    xbmcvfs.mkdirs(TEMP)

# 检索传递的参数的函数，返回字典
def get_params():
    if len(sys.argv) > 2:
        return dict(urlparse.parse_qsl(sys.argv[2].lstrip('?')))
    return {}

def normalize_string(str):
    return unicodedata.normalize(
        'NFKD', unicode(unicode(str, 'utf-8'))
    ).encode('ascii', 'ignore')

# 收集播放项目中所有可用的信息，
# 有助于确定要列出的字幕
def get_info():
    item = {}
    item['temp'] = False
    item['rar'] = False
    # 尝试获得Year
    item['year'] = xbmc.getInfoLabel("VideoPlayer.Year")
    # 尝试获得Season
    item['season'] = str(xbmc.getInfoLabel("VideoPlayer.Season"))
    # 尝试获得Episode
    item['episode'] = str(xbmc.getInfoLabel("VideoPlayer.Episode"))
    # 尝试获得Show title
    item['tvshow'] = normalize_string(
        xbmc.getInfoLabel("VideoPlayer.TVshowtitle"))
    # 尝试获得原始标题 (original title)
    item['title'] = normalize_string(
        xbmc.getInfoLabel("VideoPlayer.OriginalTitle"))
    # 播放文件的完整路径
    item['file_original_path'] = urllib.unquote(
        xbmc.Player().getPlayingFile().decode('utf-8'))

    if item['title'] == "":
        # 没有原始标题，仅获得标题
        item['title'] = normalize_string(xbmc.getInfoLabel("VideoPlayer.Title"))

    # 检查季节是否为"Special"
    if item['episode'].lower().find("s") > -1:
        item['season'] = "0"
        item['episode'] = item['episode'][-1:]

    # 检查路径是否不是本地路径
    if (item['file_original_path'].find("http") > -1):
        item['temp'] = True

    # 检查路径是否为rar文件
    elif (item['file_original_path'].find("rar://") > -1):
        item['rar'] = True
        item['file_original_path'] = os.path.dirname(
            item['file_original_path'][6:])

    # 检查路径是否是文件堆栈的一部分
    elif (item['file_original_path'].find("stack://") > -1):
        stackPath = item['file_original_path'].split(" , ")
        item['file_original_path'] = stackPath[0][8:]

    # Filename
    item['filename'] = os.path.splitext(
        os.path.basename(item['file_original_path']))[0]
    return item

# 获取用户想要搜索的语言（3个字母的格式）
def get_languages(params):
    langs = []  # ['scc','eng']
    for lang in urllib.unquote(params['languages']).decode('utf-8').split(","):
        langs.append(xbmc.convertLanguage(lang, xbmc.ISO_639_2))
    return langs

# 将字幕添加到要显示的字幕列表中
def append_subtitle(subname, lang_name, language, params, sync=False, h_impaired=False):
    listitem = xbmcgui.ListItem(
                                # 在lang徽标下显示的语言名称（例如英语）
                                label=lang_name,
                                # 字幕名称（例如“ Lost 1x01 720p”）
                                label2=subname,
                                # 语言2字母名称（例如en）
                                thumbnailImage=language)
                                #xbmc.convertLanguage(language, xbmc.ISO_639_1)

    # 字幕与视频同步
    listitem.setProperty("sync", 'true' if sync else 'false')
    # 听力障碍子项
    listitem.setProperty("hearing_imp", 'true' if h_impaired else 'false')

    # 创建将处理字幕下载的插件的网址
    url = "plugin://{url}/?{params}".format(
        url=SCRIPT_ID, params=urllib.urlencode(params))
    # 在列表中添加副标题
    xbmcplugin.addDirectoryItem(
        handle=HANDLE, url=url, listitem=listitem, isFolder=False)

# 使用get_info和get_languages收集的信息向列表中添加字幕。
def search(info, languages):
    append_subtitle(
        "Lost 1x01", "Chinese", "zh", {"action": "download", "id": 15}, sync=True)
    append_subtitle("Lost 1x01", "Chinese", "zh", {"action": "download", "id": 16})
    append_subtitle("Lost 1x01 720p", "Chinese", "zh", {"action": "download", "id": 17})

# 使用用户手动插入的字符串添加字幕到列表中。
def manual_search(search_str, languages):
    append_subtitle(
        "Lost 1x01", "Chinese", "zh", {"action": "download", "id": 15}, sync=True)
    append_subtitle("Lost 1x01", "Chinese", "zh", {"action": "download", "id": 16})
    append_subtitle("Lost 1x01 720p", "Chinese", "zh", {"action": "download", "id": 17})

# 下载用户选择的字幕
def download(params):
    id = params['id']
    # 下载所需文件
    url = "http://path.to/subtitle/{id}.srt".format(id=id)
    file = os.path.join(TEMP, "{id}.srt".format(id=id))

    response = urllib2.urlopen(url)
    with open(file, "w") as local_file:
        local_file.write(response.read())

    # 把文件交给kodi
    xbmcplugin.addDirectoryItem(
        handle=HANDLE, url=file, listitem=xbmcgui.ListItem(label=file), isFolder=False)

def run():
    # 收集请求信息
    params = get_params()

    if 'action' in params:
        if params['action'] == "search":
            # 如果动作是 "搜索"，则使用kodi提供的项目信息来搜索字幕。
            search(get_info(), get_languages(params))
        elif params['action'] == "manualsearch":
            # 如果操作是'manualsearch'，则使用用户手动插入的字符串来搜索字幕。
            manual_search(params['searchstring'], get_languages(params))
        elif params['action'] == "download":
            # 如果动作是 "下载"，则使用提供的信息下载字幕，并提供文件路径到kodi。
            download(params)

    xbmcplugin.endOfDirectory(HANDLE)