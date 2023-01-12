import os, sys
from security import security

code_path = os.path.abspath(os.path.dirname(sys.argv[0])) # code path
# default Path,will be changed by user_paths
default_path = os.path.abspath("E:\\Code") 
root_path = default_path
app_dir = '/filemanager'
security.accounts = {"test": "test", "test2": "test2"}
security.admins = ["test2"]
user_paths = {"test":os.path.abspath("E:\\Code"),"test2":os.path.abspath("E:\\Doc")}  # user's own path
exclude = []
log_debug = True
max_num_search = 1000  
host = '127.0.0.1'
port = 8083
maxFileSize = 20*1024*1024  #  the max size(Byte) of file which will be read,suggest between 200K and 50M, avoid Out Of Memory

# maybe change root_path by user
def changeRoot(login):
    if login is None:
        return
    user_root = user_paths.get(login)
    global root_path
    if user_root is not None and os.path.exists(user_root):
        root_path = user_root
    else:
        root_path = default_path
    print 'inner changeRoot '+root_path