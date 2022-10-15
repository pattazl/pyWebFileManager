pyFileManager
=============

 Support python 2, fork from pyFileManager , add some functions :

1. support upload file , search file's name in folder, get size of folder
2. support different language code such as chinese
3. can set root_path in  `lib\config\config.py`

---

A simple web file manager in Python.

![screenshot](screenshot.png)

#### Usage:

1. install python 2.x
2. check config at `lib\config\config.py`
3. make cwd(current working directory) is this program , run `python ./server.py`
4. open the browser and go to the http://127.0.0.1:8083（default）

---

#### FEATURES :
- english translation
- reverse-proxy support
- display chmod
- download, rename and delete files
- support upload file , search file's name in folder, get size of folder
- support different language code such as chinese



#### HOW TO USE WITH NGINX :
- change "app_dir" to desired directory
- use this location configuration with NGiNX :
```
location /directory {
    proxy_pass http://127.0.0.1:8083;
}
```
