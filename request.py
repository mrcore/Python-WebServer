# -*- coding: utf-8 -*-

import os
import re
import time
from settings import *
from util import log, get_url, get_404


class Request(object):
    def __init__(self, req):
        # 整个请求头信息
        self.request = req
        # 请求方法
        self.method = req.decode().split(' ')[0]
        # 整个URL包括get请求参数
        self.url = str(get_url(self.request.decode().split(' ')[1])).lower()
        # POST请求内容
        self.body = req.split('\r\n\r\n', 1)[1]
        # 只是请求文件，不包括参数
        self.src = self.get_src()
        # # 定位网页的根目录
        self.path = self.get_path()
        # 请求的附加GET或者POST参数
        self.data = self.get_data()
        # 请求cookie信息
        self.cookies = self.get_cookies()
        # 返回头信息
        self.response_head = self.get_response_head()
        # 返回状态码信息
        self.response_status = self.get_response_status()
        # 返回信息
        self.response = self.get_response()

        log('\nMethod: ' + self.method + '\nURL: ' + self.url + '\nPath :' + self.path +
            '\n Response Status' + self.response_status + '\n\n')

    # 获取请求文件的本地路径
    def get_path(self):
        path = self.get_wwwroot() + self.src
        if path[-1] == b'/':
            path += str(self.get_default())
        return path

    # 获取Cookies
    def get_cookies(self):
        try:
            cookies = {}
            cookies_data = re.findall('Cookie:\ (.*?)\r\n', self.request)[0]
            if ';' in cookies_data:
                cookies_list = re.split(';', cookies_data)
                for d in cookies_list:
                    dic = re.split('=', d)
                    cookies[dic[0]] = dic[1]
            else:
                dic = re.split('=', cookies_data)
                cookies[dic[0]] = dic[1]
        except IndexError:
            cookies = {}
        return cookies

    # 获取GET请求或者POST请求数据
    def get_data(self):
        data = {}
        if self.method == 'GET':
            if '?' in self.url:
                data_url = re.split('\?', self.url)[1]
                if '&' in data_url:
                    data_list = re.split('&', data_url)
                    for d in data_list:
                        dic = re.split('=', d)
                        data[dic[0]] = dic[1]
                else:
                    dic = re.split('=', data_url)
                    data[dic[0]] = dic[1]
        elif self.method == 'POST':
            if '=' in self.body:
                if '&' in self.body:
                    data_list = re.split('&', self.body)
                    for d in data_list:
                        dic = re.split('=', d)
                        data[dic[0]] = dic[1]
                else:
                    dic = re.split('=', self.body)
                    data[dic[0]] = dic[1]

        return data

    # 处理Server字段
    def get_server(self):
        return b'Server: Leo'

    # 处理Date字段
    def get_date(self):
        date = time.strftime("%a, %b %d %H:%M:%S %Y", time.localtime())
        date = str(b'Date: ' + date + ' GMT')
        return str.encode(date)

    # 处理Content-Type字段
    def get_type(self):
        dic = {'html': b'text/html', 'xhtml': b'text/html', 'xml': b'text/xml', 'css': b'text/css', 'js': b'application/javascript',
               'gif': b'image/gif', 'jpg': b'image/jpeg', 'jpeg': b'image/jpeg', 'png': b'image/png', 'ico': b'image/x-icon',
               'mp3': b'audio/mp3', 'pdf': b'application/pdf', 'json': b'application/json', 'woff2': b'font/woff2',
               'svg': b'image/svg+xml'
               }
        request_type = re.split('\.', self.path)[-1]
        if request_type in dic.keys():
            txt = str.encode(str(b'Content-Type: ' + dic[request_type]))
            return txt
        else:
            return ''

    # 处理Content-Length字段
    def get_length(self):
        html_file = open(self.path, 'rb')
        length = len(html_file.read())
        length = str(b'Content-Length: ' + str(length))
        return str.encode(length)

    # 获取网页src
    def get_src(self):
        try:
            return str(re.split('\?', self.url)[0])
        except IndexError:
            return self.url

    # 处理默认首页类型
    def get_default(self):
        if ',' in DEFAULT_PAGE:
            default = re.split(',', DEFAULT_PAGE)
            for i in range(len(default)):
                if os.path.exists(self.get_wwwroot() + '/' + default[i]):
                    return default[i]
        else:
            return DEFAULT_PAGE

    # 处理网页根目录
    def get_wwwroot(self):
        if WWW_ROOT[-1] == '/':

            return WWW_ROOT[:-1]
        else:
            return WWW_ROOT

    # 返回Response状态码信息
    def get_response_status(self):
        if os.path.exists(self.path):
            return b'200 OK'
        else:
            return b'404 Not Found'

    # 返回Response头信息
    def get_response_head(self):
        head = b''
        if os.path.exists(self.path):
            head += b'HTTP/1.1 200 OK\r\n'
            head += self.get_server() + b'\r\n'
            head += self.get_type() + b'\r\n'
            head += self.get_date()
            return head + '\r\n\r\n'
        else:
            return get_404()

    # 返回整个Response信息
    def get_response(self):
        response = self.get_response_head()
        if os.path.exists(self.path):
            f = open(self.path, 'rb')
            response += f.read()
        return response
