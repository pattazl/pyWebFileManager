# -*- coding: utf-8 -*-
import sys   #reload()之前必须要引入模块
reload(sys)
sys.setdefaultencoding('utf-8')
from bottle import route, view, request, redirect
from config import config
from security import security
from utils import utils, chmod
import os, json, urllib,re

@route('/')
def redirect_home():
    """Main route : redirect to app home."""
    return redirect(config.app_dir+'/')

@route(config.app_dir+'/')
@view('main.stpl')
def list():
    """App home : is building the file listing job."""
    is_auth = security.is_authenticated_user(request.get_cookie("login"), request.get_cookie("password"))
    is_admin = (is_auth and security.is_admin(request.get_cookie("login")))
    path = request.GET.get('path')
    if not path:
        path = '/'
    if path != '/':
        array = path.split("/")
        toplevel = path.replace("/" + array[path.count("/")], "")
        if not toplevel:
            toplevel  = '/'
    else:
        toplevel = False
    current_dir = config.full_path + path
    all_files = os.listdir(current_dir)
    dir_list = [d for d in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, d))]
    f = current_dir + "/.settings"
    if os.path.exists(f):
        settings_file = open(f, "r+")
        settings_json = json.load(settings_file)
        settings_file.close()
    dir_list.sort(key=lambda d: d.lower())
    file_list = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]
    file_list.sort(key=lambda d: d.lower())
    all_files = dir_list + file_list
    fileList = []
    id = 1
    syscode = sys.getfilesystemencoding()
    for item in all_files:
        if item in config.exclude:
            pass
        else:
            if not toplevel:
                filepath = path + item
            else:
                filepath = path + "/" + item
            file = config.full_path + path + '/' + item
            fileList.append({"name": item.decode(syscode).encode("utf-8"), "path": urllib.quote(filepath), "filetype": utils.get_icon(config.full_path, request.GET.get('path'), item),
                "date": utils.date_file(config.full_path +filepath), "size": utils.get_file_size(config.full_path + filepath),
                "id": id, "chmod":chmod.get_pretty_chmod(file)})
            id = id + 1

    data = {"title": path.decode(syscode).encode("utf-8"), "full_path": config.full_path, "path": path, "list": all_files,
        "toplevel": toplevel, "fileList": fileList, "is_auth": is_auth,
        "is_admin": is_admin, "error": request.GET.get('error'), "app_dir": config.app_dir}
    return dict(data=data)

@route(config.app_dir+'/search')
def search():
#   arr = os.path.split(path)
#   path2  = os.altsep.join(arr) 
    path = request.GET.get('path')
    current_dir = config.full_path + path
    val = request.GET.get('key')
    fileList = []
    for d in os.walk(current_dir):  #parent,dirnames,filenames
        # case 2:  
        for filename in d[2]:
            path = os.path.join(d[0],filename)
            if re.search(val, path, re.IGNORECASE):
                fileList.append(path)
    return dict(data=fileList)

@route(config.app_dir+'/getFolderSize')
def getFolderSize():
#   arr = os.path.split(path)
#   path2  = os.altsep.join(arr) 
    path = request.GET.get('path')
    current_dir = config.full_path + path
    size = utils.size_format(get_dir_size(current_dir))
    return dict(data=size)

def get_dir_size(dir):
    '''
    :brief:获取该目录的大小
    :param dir: 文件夹目录
    :return:改文件夹的大小：MB
    '''
    size = 0
    #遍历该文件夹下的文件并计算大小
    for root, dirs, files in os.walk(dir):
        size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
    return size

