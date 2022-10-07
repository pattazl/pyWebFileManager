# -*- coding: utf-8 -*-
import sys   #reload()之前必须要引入模块
reload(sys)
sys.setdefaultencoding('utf-8')
syscode = sys.getfilesystemencoding()  # gbk
from bottle import post, route, request, response, redirect, static_file
from config import config
from security import security
from utils import utils
import os

"""Handle basic actions."""

@post(config.app_dir+'/login')
def login():
    """Process login : set cookie when credentials are valid."""
    login = request.forms.get('login')
    password = request.forms.get('password')
    if not login or not password:
        redirect(config.app_dir+"/?error=empty")
    if security.can_login(login, password):
        response.set_cookie("login", login)
        response.set_cookie("password", security.encrypt_password(password))
        redirect(config.app_dir+"/")
    else:
        # don't indicate if that's a valid user or anything
        redirect(config.app_dir+"/?error=badpass")
    return ""


@route(config.app_dir+'/logout')
def logout():
    """Process logout : remove cookies."""
    response.set_cookie('login', '', expires=0)
    response.set_cookie('password', '', expires=0)
    redirect(config.app_dir+"/")


@route(config.app_dir+'/upload', method='POST')
def do_upload():
    """Upload files : only the admin can do this."""
    if not security.is_authenticated_admin(request.get_cookie("login"), request.get_cookie("password")):
        return None
    uploadFileName = request.forms.get('uploadFileName')
    #print str(name.decode('utf-8').encode("gbk"))
    path = request.forms.get('filePath')
    #data = request.files.get('file')
    data = request.files.get('myFile')
    #print data
    # name, ext = os.path.splitext(data.filename) 
    serverPath = config.full_path + path + os.altsep + uploadFileName
    #return serverPath
    if (os.path.exists(serverPath)):
        return "Server File: '"+serverPath+"' is exist"
    #new_file = open(serverPath, "w+")
    #new_file.write(data.file.read())
    data.save(serverPath.encode(syscode))
    redirect(config.app_dir+"/?path=" + path.decode('utf-8').encode(syscode))


@route(config.app_dir+'/rename')
def rename():
    """Rename a file/directory : only the admin can do this."""
    if not security.is_authenticated_admin(request.get_cookie("login"), request.get_cookie("password")):
        return None
    srcPath = config.full_path+'/'+request.GET.get('srcPath').decode('utf-8').encode(syscode)
    dstPath = config.full_path+'/'+request.GET.get('dstPath').decode('utf-8').encode(syscode)
    itemId = request.GET.get('itemId');

    if srcPath == dstPath:
        return None
    if config.log_debug:
        print("user wants to rename '"+repr(srcPath)+"' to '"+repr(dstPath))
    try:
        os.rename(srcPath, dstPath)
    except Exception, e:
        if config.log_debug:
            print("Can't rename file")
            print(repr(e))
    return '{"itemId": "'+itemId+'", "filetype": "'+utils.get_icon(
        config.full_path, request.GET.get('path'), dstPath)+'"}'


@route(config.app_dir+'/download')
def download():
    """Download a file : only the admin can do this."""
    if not security.is_authenticated_admin(request.get_cookie("login"), request.get_cookie("password")):
        return None
    filename = request.GET.get('path')
    return static_file(filename, root=config.full_path, download=filename)


@route(config.app_dir+'/delete')
def delete():
    """Delete a file : only the admin can do this."""
    if not security.is_authenticated_admin(request.get_cookie("login"), request.get_cookie("password")):
        return None
    filePath = config.full_path + request.GET.get('path')
    if config.log_debug:
        print("deleted file : "+filePath)
    try:
        os.unlink(filePath)
    except:
        if config.log_debug:
            print("File doesn't exists")
    return None
