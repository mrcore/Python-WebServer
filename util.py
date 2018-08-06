# -*- coding: utf-8 -*-

from settings import DEFAULT_404, MOVE301, MOVE302, LOG_PATH
import urllib
import time
import sys
import re

reload(sys)
sys.setdefaultencoding('utf8')


def get_404():
    head = 'HTTP/1.1 404 Not Found\r\nServer: Leo Server\r\n\r\n'
    html_file = open(DEFAULT_404, 'rb')
    head += html_file.read()
    html_file.close()
    return head


def move301(src):
    move_url = MOVE301[src]
    print('GET > ' + src + ' >  301 Moved Permanently  >  ' + move_url)
    log('GET > ' + src + ' >  301 Moved Permanently  >  ' + move_url)
    response = b'HTTP/1.1 301 Moved Permanently\r\nLocation: ' + move_url + '\r\n\r\n'
    return response


def move302(src):
    move_url = MOVE302[src]
    print('GET > ' + src + ' >  302 Move temporarily  >  ' + move_url)
    log('GET > ' + src + ' >  302 Move temporarily  >  ' + move_url)
    response = b'HTTP/1.1 302 Move temporarily\r\nLocation: ' + move_url + '\r\n\r\n'
    return response


def log(txt):
    format_time = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format_time, value)
    with open(LOG_PATH, 'a') as f:
        f.write('%s : %s\n' % (dt, txt))


def get_url(url):
    url = url.encode('ascii')
    url = urllib.unquote(url)
    return url


def get_src(request):
    url = get_url(request.split(' ')[1])
    url = get_url(url)
    try:
        return str(re.split('\?', url)[0])
    except IndexError:
        return url
