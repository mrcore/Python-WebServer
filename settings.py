# -*- coding: utf-8 -*-

from model.login import login
from model.login import result

# 地址
HOST = ''

# 端口
PORT = '80'

# 默认主页
# 以,分割 优先级从高到低
DEFAULT_PAGE = 'index.html,default.html'

# 默认404页面
DEFAULT_404 = '/home/webserver/404.html'

# 网页根目录
WWW_ROOT = '/home/webserver/wwwroot'

# 日志目录
LOG_PATH = '/home/webserver/log.txt'

# 301跳转 请求路径：跳转页面
MOVE301 = {'/move': 'https://www.baidu.com',
           '/a': 'https://www.baidu.com'}

# 302跳转 请求路径：跳转页面
MOVE302 = {'/b': 'https://www.hao123.com'}

# MVC结构路由信息，得先在文件顶部导入函数
ROUTES = {'/login': login, '/login.html': login,
          '/result': result, '/result.html': result, }
