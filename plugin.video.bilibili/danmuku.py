#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import xml2ass
import os
import io
import shutil

def Danmuku(cid):
#############在这里改路径####################

#####PC端路径示例############################
  # path = 'D:/ass'
#####coreelec端路径示例############################
    path = '/storage/videos/ass'
#############################################
    if os.path.exists(path):
        shutil.rmtree(path)
        os.makedirs(path)
    else:
        os.makedirs(path)
    
    headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
    danmuku = requests.get('https://comment.bilibili.com/' + str(cid) + '.xml',headers = headers)
    danmuku.encoding = 'utf-8'
        # print(type(danmuku.text))
    with io.open(path+'/'+str(cid)+'.xml', 'w',encoding = 'utf-8') as file:
        file.write(danmuku.text)
    file.close()
    xml2ass.Danmaku2ASS(path+'/'+str(cid)+'.xml',path+'/'+str(cid)+'.ass',1920,540)
    os.remove(path+'/'+str(cid)+'.xml')
