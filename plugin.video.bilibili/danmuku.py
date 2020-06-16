#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import xml2ass
import os
import io
import shutil

def Danmuku(cid):
    path = 'D:/ass'
    if os.path.exists(path):
        shutil.rmtree(path)
        os.makedirs(path)
    else:
        os.makedirs(path)
    # 链接格式：https://www.bilibili.com/video/BV******* (后面不能有/)
    # url = input('输入视频链接：')
    # bv = url[len('https://www.bilibili.com/video/'):]
    headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
    # a = requests.get('http://api.bilibili.com/x/web-interface/archive/stat?bvid='+ bv, headers = headers)
    # dict_aid = eval(a.text)
    # aid = dict_aid['data']['aid']
    # # print(aid)
    # r = requests.get("https://www.bilibili.com/widget/getPageList?aid=" + str(aid),headers = headers)
    # # print(eval(r.text))
    # cid = []
    # for i in eval(r.text):
    #     dict = i
    #     every_cid = dict['cid']
    #     cid.append(every_cid)
    # print(len(cid))

    # *******多P视频分P下载弹幕************
    # for j in range(len(cid)):
    #     p_cid = cid[j]
    #     # print(p_cid)
    danmuku = requests.get('https://comment.bilibili.com/' + str(cid) + '.xml',headers = headers)
    danmuku.encoding = 'utf-8'
        # print(type(danmuku.text))
    with io.open('D:/ass/'+str(cid)+'.xml', 'w',encoding = 'utf-8') as file:
        file.write(danmuku.text)
    file.close()
    xml2ass.Danmaku2ASS('D:/ass/'+str(cid)+'.xml','D:/ass/'+str(cid)+'.ass',1920,540)
    os.remove('D:/ass/'+str(cid)+'.xml')

