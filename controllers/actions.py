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
    # serverPath = config.root_path + path + os.sep + uploadFileName
    serverPath = os.path.join(config.root_path + path ,uploadFileName)
    sysServerPath = utils.toUTF8(serverPath,False)
    if (os.path.exists(sysServerPath)):
        return "Server File: '"+serverPath+"' is exist"
    #new_file = open(serverPath, "w+")
    #new_file.write(data.file.read())
    try:
        data.save(sysServerPath)
    except Exception as e:
        return repr(e)
    redirect(config.app_dir+"/?path=" + utils.toUTF8(path,False))


@route(config.app_dir+'/rename')
def rename():
    """Rename a file/directory : only the admin can do this."""
    if not security.is_authenticated_admin(request.get_cookie("login"), request.get_cookie("password")):
        return None
    currPath = utils.toUTF8(request.GET.get('currPath'),False)
    srcPath = os.path.join(config.root_path+currPath , utils.toUTF8(request.GET.get('srcPath'),False))
    dstPath = os.path.join(config.root_path+currPath , utils.toUTF8(request.GET.get('dstPath'),False))
    itemId = request.GET.get('itemId');
    error = ''
    if srcPath == dstPath:
        return None
    if config.log_debug:
        print("user wants to rename '"+srcPath+"' to '"+dstPath)
    try:
        os.rename(srcPath, dstPath)
    except Exception as e:
        if config.log_debug:
            print("Can't rename file")
            error = repr(e)
    return dict({"itemId": itemId, "filetype":utils.get_icon(
        config.root_path, request.GET.get('path'), dstPath),"error":error})


@route(config.app_dir+'/download')
def download():
    """Download a file : only the admin can do this."""
    if not security.is_authenticated_admin(request.get_cookie("login"), request.get_cookie("password")):
        return None
    filename = request.GET.get('path')
    return static_file(filename, root=config.root_path, download=filename)


@route(config.app_dir+'/delete')
def delete():
    """Delete a file : only the admin can do this."""
    if not security.is_authenticated_admin(request.get_cookie("login"), request.get_cookie("password")):
        return None
    filePath = config.root_path + request.GET.get('path')
    if config.log_debug:
        print("deleted file : "+filePath)
    try:
        os.unlink(filePath)
    except:
        if config.log_debug:
            print("File doesn't exists")
    return None
