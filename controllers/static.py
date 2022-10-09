from bottle import route, static_file, request
from config import config

"""Handle static ressources."""
@route(config.app_dir+'/img/:filename')
def img_static(filename):
    return static_file(filename, root=config.code_path+'/views/static/img/')

@route(config.app_dir+'/img/view')
def view_img_static():
    filename = request.GET.get('path')
    return static_file(filename, root=config.root_path)

@route(config.app_dir+'/movie/view')
def view_img_static():
    filename = request.GET.get('path')
    return static_file(filename, root=config.root_path)

@route(config.app_dir+'/img/fancybox/:filename')
def fancybox_static(filename):
    return static_file(filename, root=config.code_path+'/views/static/img/fancybox/')

@route(config.app_dir+'/js/:filename')
def js_static(filename):
    return static_file(filename, root=config.code_path+'/views/static/js/')

@route(config.app_dir+'/css/:filename')
def css_static(filename):
    return static_file(filename, root=config.code_path+'/views/static/css/')

@route(config.app_dir+'/fonts/:filename')
def css_static(filename):
    return static_file(filename, root=config.code_path+'/views/static/fonts/')
