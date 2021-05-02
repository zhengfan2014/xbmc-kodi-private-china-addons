#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import re
import xml.etree.cElementTree as et
import zipfile
import shutil
import hashlib


workpath = '/workdir/python2/'

addons_xml = et.Element('addons')

# 匹配所有需要处理的kodi插件
for pluginname in os.listdir(workpath):
    if re.search('\[停止更新\]|video.vid|bangumi|cine|reallive', pluginname):
        # 跳过停止更新的项目
        pass
    elif re.search('metadata.*', pluginname) or re.search('plugin.*', pluginname) or re.search('service.*', pluginname):
        # 读取xml获取版本
        parser = et.parse(workpath + "/" + pluginname + "/addon.xml")
        root = parser.getroot()
        version = root.attrib['version']
        # 压缩
        zippath = workpath + '/latest/' + \
            str(pluginname) + '-' + version + '.zip'
        f = zipfile.ZipFile(zippath, 'w', zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(workpath + '/' + pluginname):
            # 这一句很重要，不replace的话，就从根目录开始复制
            fpath = dirpath.replace(workpath + '/', '')
            fpath = fpath and fpath + os.sep or ''  # 这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
            for filename in filenames:
                f.write(os.path.join(dirpath, filename), fpath+filename)
        print(pluginname + '压缩成功')
        f.close()
        # 拷贝zip到对应repo
        basepath = workpath + "/repo/" + pluginname + '/'
        if not os.path.exists(basepath):
            os.makedirs(basepath)
        shutil.copy(zippath, basepath + pluginname + '-' + version + '.zip')
        # 拷贝icon
        shutil.copy(workpath + '/' + str(pluginname) +
                    '/icon.png', basepath + 'icon.png')
        # 合并xml
        addons_xml.append(root)
# 输出addons.xml
tree = et.ElementTree(addons_xml)
tree.write(workpath + '/addons.xml', "UTF-8",xml_declaration=True)
# 生成addons.xml.md5
f = open(workpath + '/addons.xml')
m2 = hashlib.md5()
text = f.read()
m2.update(text)
f.close()
with open(workpath + '/addons.xml.md5','w') as f: # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
    f.write(m2.hexdigest())
    f.close()
