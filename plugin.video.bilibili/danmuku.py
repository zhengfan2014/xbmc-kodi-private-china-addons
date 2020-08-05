#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import xml2ass
import os
import io
import shutil

#获取文件后缀名
def suffix(fileName, *suffixName):
    array = map(fileName.endswith, suffixName)
    if True in array :
        return True
    else :
        return False
    
#删除目录下扩展名为.ass的文件
def deleteFile(path):
    target_dir = path
    for root, dir_names, file_names in os.walk(target_dir):
        for file in file_names:
            target_file = os.path.join(root, file)
            if suffix(file, '.ass','.xml'):
                os.remove(target_file)
            # 文件夹名字
            if file == 'a':
                shutil.rmtree(os.path.join(root, dir_names))

def Danmuku(cid,path):
    path = path.replace('\\','/')
#############在这里改路径####################

#####PC端路径示例############################
  # path = 'D:/ass'
#####coreelec端路径示例############################
    # path = '/storage/videos/ass'
#############################################

    if os.path.exists(path):
        # shutil.rmtree(path)
        # os.makedirs(path)
        deleteFile(path)
    else:
        os.makedirs(path)
    headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
    danmuku = requests.get('https://comment.bilibili.com/' + str(cid) + '.xml',headers = headers)
    danmuku.encoding = 'utf-8'
        # print(type(danmuku.text))
    with io.open(path + '/' + str(cid)+'.xml', 'w',encoding = 'utf-8') as file:
        file.write(danmuku.text)
    file.close()
    xml2ass.Danmaku2ASS(path+'/'+str(cid)+'.xml',path+'/'+str(cid)+'.ass',1920,540)
    os.remove(path+'/'+str(cid)+'.xml')

