import os
import re
import xml.etree.cElementTree as et
import zipfile
import shutil


workpath = '/config/workspace/kodi/xbmc-kodi-private-china-addons'


# 匹配所有需要处理的kodi插件
for pluginname in os.listdir(workpath):
    if re.search('\[停止更新\]',pluginname):
        # 跳过停止更新的项目
        pass
    elif re.search('metadata.*',pluginname) or re.search('plugin.*',pluginname) or re.search('service.*',pluginname):
        # 读取xml获取版本
        parser = et.parse(workpath + "/" + pluginname + "/addon.xml")
        root = parser.getroot()
        version = root.attrib['version']
        # 压缩
        zippath = workpath + '/latest/' + str(pluginname) + '-' + version +  '.zip'
        f = zipfile.ZipFile(zippath,'w',zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(workpath + '/' + pluginname):
            fpath = dirpath.replace(workpath + '/','') #这一句很重要，不replace的话，就从根目录开始复制
            fpath = fpath and fpath + os.sep or ''#这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
            for filename in filenames:
                f.write(os.path.join(dirpath, filename),fpath+filename)
        print (pluginname + '压缩成功')
        f.close()
        # 拷贝zip到对应repo
        basepath = workpath + "/repo/" + pluginname + '/'
        if not os.path.exists(basepath):
            os.makedirs(basepath)
        shutil.copy(zippath, basepath + pluginname + '-' + version +  '.zip')
        # 拷贝icon

        # 合并xml