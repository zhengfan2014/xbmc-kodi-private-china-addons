#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import sys
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

from lib.tmdbscraper.tmdb import TMDBMovieScraper
from lib.tmdbscraper.fanarttv import get_details as get_fanarttv_artwork
from lib.tmdbscraper.imdbratings import get_details as get_imdb_details
from lib.tmdbscraper.traktratings import get_trakt_ratinginfo
from scraper_datahelper import combine_scraped_details_info_and_ratings, \
    combine_scraped_details_available_artwork, find_uniqueids_in_text, get_params
from scraper_config import configure_scraped_details, PathSpecificSettings, \
    configure_tmdb_artwork, is_fanarttv_configured

from xbmcswift2 import Plugin
import requests
from bs4 import BeautifulSoup
import re
from requests.adapters import HTTPAdapter

ADDON_SETTINGS = xbmcaddon.Addon('metadata.douban.com.python')
ID = ADDON_SETTINGS.getAddonInfo('id')


def log(msg, level=xbmc.LOGDEBUG):
    xbmc.log(msg='[{addon}]: {msg}'.format(addon=ID, msg=msg), level=level)


headers = {
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'Cache-Control': 'max-age=0',
    # 'Connection': 'keep-alive',
    # 'Sec-Fetch-User': '?1',
    # 'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
}
plugin = Plugin()


# @plugin.cached(TTL=2)
def get_html(url, ua='pc', cookie='', mode='html', encode='utf-8'):
    #ConnectionError
    cloudflare = ADDON_SETTINGS.getSetting('cloudflareproxy')
    cloudflareurl = ADDON_SETTINGS.getSetting('cloudflareproxyurl')
    # dialog = xbmcgui.Dialog()
    # dialog.textviewer('错误提示', str(cloudflare))
    # dialog = xbmcgui.Dialog()
    # dialog.textviewer('错误提示', str(cloudflareurl))

    if cloudflare == 'true':
        if cloudflareurl[-1:] == '/':
            url = cloudflareurl + '-----' + url
        else:
            url = cloudflareurl + '/-----' + url
    else:
        dialog = xbmcgui.Dialog()
        dialog.notification('警告', '未设置代理Url可能使你的IP被豆瓣封禁',
                            xbmcgui.NOTIFICATION_WARNING, 5000, False)

    if cookie != '':
        cookie = eval(cookie)
    else:
        cookie = {}
    # UA相关
    head = headers
    # 超时重试3次
    # s0 = requests.Session()
    with requests.Session() as s0:
        s0.mount('http://', HTTPAdapter(max_retries=3))
        s0.mount('https://', HTTPAdapter(max_retries=3))

        # 获取网页源代码
        if mode == 'html':
            r = s0.get(url, headers=head, cookies=cookie, timeout=15)

            # 编码相关
            if encode == 'utf-8':
                r.encoding = 'utf-8'
            if encode == 'gbk':
                r.encoding = 'gbk'
            html = r.text

        # 用于获取302跳转网页的真实url
        if mode == 'url':
            head['Connection'] = 'close'
            r = s0.get(url, headers=head, timeout=5,
                       stream=True, cookies=cookie)
            html = r.url
        # dialog = xbmcgui.Dialog()
        # dialog.textviewer('错误提示', str(url))
        # dialog = xbmcgui.Dialog()
        # dialog.textviewer('错误提示', str(html.encode('utf-8')))
        return html

#获取视频真实url
def get_douban_videourl(url):
    r = get_html(url)
    soup = BeautifulSoup(r, 'html.parser')
    video = False
    counter = 1
    while soup.find('source', type="video/mp4") == False:
        r = get_html(url)
        soup = BeautifulSoup(r, 'html.parser')
        counter += 1
        if counter > 3:
            break
        if soup.find('source', type="video/mp4"):
            video = soup.find('source', type="video/mp4")['src']
            break
    return video


def get_douban_imglist(url):
    r = get_html(url)
    soup = BeautifulSoup(r, 'html.parser')
    ul = soup.find('ul', class_='poster-col3')
    li = ul.find_all('li')
    returnlist = []
    for index in range(len(li)):
        imgdict = {}
        img = li[index].find('img')['src']
        imgdict['preview'] = img
        img = re.sub('photo\/m', 'photo/r', img)
        imgdict['url'] = img
        returnlist.append(imgdict)
    return returnlist

# 构造仿tmdb的json
# [{
#         "poster_path": "https://1.jpg",
#         "title": "标题",
#         "release_date": "2019-06-19",
#         "id": 568160
#     }]


# def get_douban_search(title, year):
#     #r = get_html("https://search.douban.com/movie/subject_search?cat=1002&search_text=" + title)
#     r = get_html("https://www.douban.com/search?cat=1002&q=" + title)
#     #print(r.encode('utf-8'))
#     dialog = xbmcgui.Dialog()
#     dialog.textviewer('search', str(r.encode('utf-8')))
#     soup = BeautifulSoup(r, 'html.parser')
#     result = soup.find("div", class_="result-list")
#     resultlist = result.find_all('div', class_='result')
#     returnlist = []
#     for index in range(len(resultlist)):
#         returndict = {}
#         returndict['title'] = resultlist[index].find(
#             'div', class_="title").a.text
#         returndict['poster_path'] = resultlist[index].find(
#             'div', class_="pic").a.img['src']
#         returndict['release_date'] = re.search(
#             '(?<=/ )[\d]{4}$', resultlist[index].find('span', class_="subject-cast").text).group()
#         returndict['id'] = re.search(
#             '(?<=sid: )[\d]+', resultlist[index].find('div', class_="pic").a['onclick']).group()
#         returnlist.append(returndict)
#     return returnlist
def get_douban_search(title, year):
    r = get_html('https://movie.douban.com/j/subject_suggest?q=' + title)
    j = json.loads(r)
    returnlist = []
    for index in range(len(j)):
        returndict = {}
        returndict['title'] = j[index]['sub_title']
        returndict['poster_path'] = j[index]['img'].replace(
            's_ratio_poster', 'r')
        returndict['release_date'] = j[index]['year'] + '-01-01'
        returndict['id'] = j[index]['id']
        returnlist.append(returndict)

    return returnlist

# 用douban的数据，构造仿tmdb的json


def get_douban_details(input_uniqueids):
    doubanjson = {
        "info": {
            "mpaa": "PG-13",
            "studio": ["豆瓣电影"],
            "tag": [],
            "trailer":""
        },
        "ratings": {
            "themoviedb": {}
        },
        "available_art": {
            "set.landscape": [],
            "set.fanart": [],
            "set.poster": [],
            "fanart": [],
            "poster": [],
            "landscape": []
        },
        "uniqueids": {},
        "cast": [],
        "_info": {
            "set_tmdbid": None
        }}
    #传入input_uniqueids = {'tmdb':'123456'}
    doubanid = int(input_uniqueids['tmdb'])
    doubanjson['uniqueids']['tmdb'] = doubanid
    doubanurl = 'http://movie.douban.com/subject/' + str(doubanid) + '/'
    r = get_html(doubanurl)
    print(r.encode('utf-8'))
    soup = BeautifulSoup(r, 'html.parser')

    # 国家
    countrys = []
    info = soup.find('div',id='info')
    country = re.search(r'(?<=制片国家/地区:</span>).*?(?=<br/>)',str(info)).group()
    # country = '日本'
    if re.search('/', country):
        country = country.split('/')
        for i in range(len(country)):
            countrys.append(country[i].strip())
    else:
        countrys.append(country.strip())
    doubanjson['info']['country'] = countrys

    # 标题&年
    doubanjson['info']['title'] = soup.find(
        'span', property="v:itemreviewed").text
    #year = soup.find('span',class_="year").text.replace('(','').replace(')','')

    # 豆瓣评分&人数
    doubanjson['ratings']['themoviedb']['rating'] = float(
        soup.find('strong', class_="ll rating_num").text)
    doubanjson['ratings']['themoviedb']['votes'] = int(
        soup.find('span', property="v:votes").text)

    # 简介
    doubanjson['info']['plot'] = soup.find(
        'span', property="v:summary").text.strip()

    # 预告片
    if get_douban_videourl(soup.find('a', title="预告片")['href']):
        trailer = get_douban_videourl(soup.find('a', title="预告片")['href']) + '|referer=' + doubanurl
        doubanjson['info']['trailer'] = trailer

    # 类型
    genre = soup.find_all('span', property="v:genre")
    genres = []
    for i in range(len(genre)):
        genres.append(genre[i].text)
    doubanjson['info']['genre'] = genres

    # 时长
    doubanjson['info']['duration'] = int(
        soup.find('span', property="v:runtime")['content'])*60

    # 日期
    doubanjson['info']['premiered'] = re.search(
        '[\d]{4}-[\d]{2}-[\d]{2}', soup.find('span', property="v:initialReleaseDate")['content']).group()

    

    # 标签
    taglist = []
    tag = soup.find('div', class_='tags-body')
    tags = tag.find_all('a')
    for i in range(len(tags)):
        taglist.append(tags[i].text)
    doubanjson['info']['tag'] = taglist

    # 剧照
    doubanjson['available_art']['fanart'] = get_douban_imglist('https://movie.douban.com/subject/' + str(doubanid) + '/photos?type=S')

    # 海报
    doubanjson['available_art']['poster'] = get_douban_imglist('https://movie.douban.com/subject/' + str(doubanid) + '/photos?type=R')

    # 导演&编剧&演员
    r = get_html("https://movie.douban.com/subject/" +
                 str(doubanid) + "/celebrities")
    soup = BeautifulSoup(r, 'html.parser')

    director = []
    credit = []
    cast = []
    celebrities = soup.find('div', id='celebrities').find_all(
        'div', class_='list-wrapper')
    for index in range(len(celebrities)):
        if celebrities[index].h2.text == u'导演 Director':
            li = celebrities[index].find_all('li')
            for i in range(len(li)):
                director.append(li[i].a['title'])
        if celebrities[index].h2.text == u'编剧 Writer':
            li = celebrities[index].find_all('li')
            for i in range(len(li)):
                credit.append(li[i].a['title'])
        if celebrities[index].h2.text == u'演员 Cast':
            li = celebrities[index].find_all('li')
            for i in range(len(li)):
                castdict = {}
                castdict['order'] = i
                castdict['role'] = li[i].find('span', class_='role')['title']
                castdict['name'] = li[i].a['title']
                castdict['thumbnail'] = li[i].a.div['style'].replace(
                    'background-image: url(', '').replace(')', '').replace('s_ratio_celebrity', 'r')
                cast.append(castdict)
    doubanjson['info']['director'] = director
    doubanjson['info']['credits'] = credit
    doubanjson['cast'] = cast
    return doubanjson


def get_tmdb_scraper(settings):
    language = settings.getSettingString('language')
    certcountry = settings.getSettingString('tmdbcertcountry')
    # dialog = xbmcgui.Dialog()
    # #dialog.notification('提示', '已关闭', xbmcgui.NOTIFICATION_INFO, 5000)
    # dialog.textviewer('提示', str(TMDBMovieScraper(ADDON_SETTINGS, language, certcountry)))
    return TMDBMovieScraper(ADDON_SETTINGS, language, certcountry)


def search_for_movie(title, year, handle, settings):
    # 刮削&搜索
    log("Find movie with title '{title}' from year '{year}'".format(
        title=title, year=year), xbmc.LOGINFO)
    title = _strip_trailing_article(title)
    # 输出json结果
    search_results = get_douban_search(title, year)
    #search_results = get_tmdb_scraper(settings).search(title, year)
    #dialog = xbmcgui.Dialog()
    #dialog.textviewer('提示', str(get_tmdb_scraper(settings).search(title, year)))

    if not search_results:
        return
    # if 'error' in search_results:
    #     header = "The Movie Database Python error searching with web service TMDB"
    #     xbmcgui.Dialog().notification(header, search_results['error'], xbmcgui.NOTIFICATION_WARNING)
    #     log(header + ': ' + search_results['error'], xbmc.LOGWARNING)
    #     return

    for movie in search_results:
        listitem = _searchresult_to_listitem(movie)
        uniqueids = {'tmdb': str(movie['id'])}
        xbmcplugin.addDirectoryItem(handle=handle, url=build_lookup_string(uniqueids),
                                    listitem=listitem, isFolder=True)


_articles = [
    prefix + article for prefix in (', ', ' ') for article in ("the", "a", "an")]


def _strip_trailing_article(title):
    title = title.lower()
    for article in _articles:
        if title.endswith(article):
            return title[:-len(article)]
    return title


def _searchresult_to_listitem(movie):
    # 显示搜索结果  天气之子(2019)
    movie_info = {'title': movie['title']}
    movie_label = movie['title']

    movie_year = movie['release_date'].split(
        '-')[0] if movie.get('release_date') else None
    if movie_year:
        movie_label += ' ({})'.format(movie_year)
        movie_info['year'] = movie_year

    listitem = xbmcgui.ListItem(movie_label, offscreen=True)

    listitem.setInfo('video', movie_info)
    if movie['poster_path']:
        listitem.setArt({'thumb': movie['poster_path']})
    # dialog = xbmcgui.Dialog()
    # dialog.textviewer('提示111', str(movie_info))
    return listitem


# Low limit because a big list of artwork can cause trouble in some cases
# (a column can be too large for the MySQL integration),
# and how useful is a big list anyway? Not exactly rhetorical, this is an experiment.
IMAGE_LIMIT = 10


def add_artworks(listitem, artworks):
    for arttype, artlist in artworks.items():
        if arttype == 'fanart':
            continue
        for image in artlist[:IMAGE_LIMIT]:
            listitem.addAvailableArtwork(image['url'], arttype)

    fanart_to_set = [{'image': image['url'], 'preview': image['preview']}
                     for image in artworks['fanart'][:IMAGE_LIMIT]]
    listitem.setAvailableFanart(fanart_to_set)


def get_details(input_uniqueids, handle, settings):
    # 解析详细信息
    if not input_uniqueids:
        return False

    #details = get_tmdb_scraper(settings).get_details(input_uniqueids)
    #传入input_uniqueids = {'tmdb':'123456'}
    details = get_douban_details(input_uniqueids)
    
    # dialog = xbmcgui.Dialog()
    # dialog.textviewer('details', str(input_uniqueids))
    if not details:
        return False
    # if 'error' in details:
    #     header = "The Movie Database Python error with web service TMDB"
    #     xbmcgui.Dialog().notification(header, details['error'], xbmcgui.NOTIFICATION_WARNING)
    #     log(header + ': ' + details['error'], xbmc.LOGWARNING)
    #     return False

    # details = configure_tmdb_artwork(details, settings)

    if settings.getSettingString('RatingS') == 'IMDb' or settings.getSettingBool('imdbanyway'):
        imdbinfo = get_imdb_details(details['uniqueids'])
        if 'error' in imdbinfo:
            header = "The Movie Database Python error with website IMDB"
            log(header + ': ' + imdbinfo['error'], xbmc.LOGWARNING)
        else:
            details = combine_scraped_details_info_and_ratings(
                details, imdbinfo)

    if settings.getSettingString('RatingS') == 'Trakt' or settings.getSettingBool('traktanyway'):
        traktinfo = get_trakt_ratinginfo(details['uniqueids'])
        details = combine_scraped_details_info_and_ratings(details, traktinfo)

    if is_fanarttv_configured(settings):
        fanarttv_info = get_fanarttv_artwork(details['uniqueids'],
                                             settings.getSettingString(
                                                 'fanarttv_clientkey'),
                                             settings.getSettingString(
                                                 'fanarttv_language'),
                                             details['_info']['set_tmdbid'])
        details = combine_scraped_details_available_artwork(
            details, fanarttv_info)

    details = configure_scraped_details(details, settings)

    listitem = xbmcgui.ListItem(details['info']['title'], offscreen=True)
    listitem.setInfo('video', details['info'])
    listitem.setCast(details['cast'])
    listitem.setUniqueIDs(details['uniqueids'], 'tmdb')
    add_artworks(listitem, details['available_art'])

    for rating_type, value in details['ratings'].items():
        if 'votes' in value:
            listitem.setRating(
                rating_type, value['rating'], value['votes'], value['default'])
        else:
            listitem.setRating(
                rating_type, value['rating'], defaultt=value['default'])

    xbmcplugin.setResolvedUrl(handle=handle, succeeded=True, listitem=listitem)
    return True


def find_uniqueids_in_nfo(nfo, handle):
    uniqueids = find_uniqueids_in_text(nfo)
    if uniqueids:
        listitem = xbmcgui.ListItem(offscreen=True)
        xbmcplugin.addDirectoryItem(
            handle=handle, url=build_lookup_string(uniqueids), listitem=listitem, isFolder=True)


def build_lookup_string(uniqueids):
    return json.dumps(uniqueids)


def parse_lookup_string(uniqueids):
    try:
        return json.loads(uniqueids)
    except ValueError:
        log("Can't parse this lookup string, is it from another add-on?\n" +
            uniqueids, xbmc.LOGWARNING)
        return None


def run():
    params = get_params(sys.argv[1:])
    enddir = True
    if 'action' in params:
        settings = ADDON_SETTINGS if not params.get('pathSettings') else \
            PathSpecificSettings(json.loads(
                params['pathSettings']), lambda msg: log(msg, xbmc.LOGWARNING))
        action = params["action"]
        if action == 'find' and 'title' in params:
            search_for_movie(params["title"], params.get(
                "year"), params['handle'], settings)
        elif action == 'getdetails' and 'url' in params:
            enddir = not get_details(parse_lookup_string(
                params["url"]), params['handle'], settings)
        elif action == 'NfoUrl' and 'nfo' in params:
            find_uniqueids_in_nfo(params["nfo"], params['handle'])
        else:
            log("unhandled action: " + action, xbmc.LOGWARNING)
    else:
        log("No action in 'params' to act on", xbmc.LOGWARNING)
    if enddir:
        xbmcplugin.endOfDirectory(params['handle'])


if __name__ == '__main__':
    run()
