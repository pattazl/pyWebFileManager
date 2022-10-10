import os, sys
from security import security

code_path = os.path.abspath(os.path.dirname(sys.argv[0])) # code path
root_path = code_path  # os.path.abspath("E:\\Code")  # can set root path  
app_dir = '/filemanager'
security.accounts = {"test": "test", "test2": "test2"}
security.admins = ["test2"]
exclude = []
log_debug = True
max_num_search = 1000  
host = '127.0.0.1'
port = 8083
maxFileSize = 20*1024*1024  #  the max size(Byte) of file which will be read,suggest between 200K and 50M, avoid Out Of Memory