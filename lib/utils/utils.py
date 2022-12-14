import os, time
import sys 
from bottle import static_file,HTTPError
from config import config

"""Utils here."""


def get_icon(full_path, path, filename):
    """Get icon, based on file name."""
    if not path:
        path = '/'
    TEXT_TYPE = ['doc', 'docx', 'txt', 'rtf', 'odf', 'text', 'nfo']
    LANGUAGE_TYPE = ['js', 'html', 'htm', 'xhtml', 'jsp', 'asp', 'aspx', 'php', 'xml', 'css', 'py', 'bat', 'sh', 'rb', 'java']
    AUDIO_TYPE = ['aac', 'mp3', 'wav', 'wma', 'm4p', 'flac', 'ac3']
    IMAGE_TYPE = ['bmp', 'gif', 'jpg', 'jpeg', 'png','svg', 'eps', 'ico', 'psd', 'psp', 'raw', 'tga', 'tif', 'tiff', 'svg']
    VIDEO_TYPE = ['mv4', 'bup', 'mkv', 'ifo', 'flv', 'vob', '3g2', 'bik', 'xvid', 'divx', 'wmv', 'avi', '3gp', 'mp4', 'mov', '3gpp', '3gp2', 'swf', 'mpg', 'mpeg']
    ARCHIVE_TYPE = ['7z', 'dmg', 'rar', 'sit', 'zip', 'bzip', 'gz', 'tar', 'bz2', 'ace']

    if os.path.isdir(full_path + path + "/" + filename):
        return 'folder-o'
    else:
        extension = os.path.splitext(filename)[1][1:].lower()
        if extension in AUDIO_TYPE:
            return 'music'
        elif extension in TEXT_TYPE or extension in LANGUAGE_TYPE:
            return 'file-text-o'
        elif extension in IMAGE_TYPE:
            return 'file-image-o'
        elif extension == 'mp4':
            return 'file-movie-o'
        elif extension in VIDEO_TYPE:
            return 'film'
        elif extension in ARCHIVE_TYPE:
            return 'file-archive-o'
        elif extension == 'pdf':
            return 'file-pdf-o'
        return 'file-o'


def date_file(path):
    """Get date with proper format."""
    mtime = time.gmtime(os.path.getmtime(path))
    return time.strftime("%d/%m/%Y %H:%M", mtime)

def get_file_size(path):
    bytes = float(os.path.getsize(path))
    return bytes

# str sys -> utf8 , if flag = false is utf8->sys
syscode = sys.getfilesystemencoding()
def toUTF8(myStr,flag=True):
    global syscode
    if myStr is None:
        myStr='' 
    if syscode.lower()=='utf-8':
        return myStr
    else:
        try:
            if flag:
                resStr = myStr.decode(syscode).encode("utf-8")
            else:
                resStr = myStr.decode("utf-8").encode(syscode)
        except Exception as e:
            resStr = myStr
            #syscode = 'utf-8'
        return resStr

# use the max size of file which will read
def my_static_file(filename, root,
                mimetype=True,
                download=False,
                charset='UTF-8',
                etag=None):
    myRoot = os.path.join(os.path.abspath(root), '')
    myFilename = os.path.abspath(os.path.join(myRoot, filename.strip('/\\')))
    stats = os.stat(myFilename)
    if stats.st_size > config.maxFileSize:
        return HTTPError(413, "File Size["+str(stats.st_size)+"]byte out of Max["+str(config.maxFileSize)+"]byte")
    return static_file(filename, root,
                mimetype,
                download,
                charset,
                etag)