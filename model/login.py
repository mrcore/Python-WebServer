# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader

loader = FileSystemLoader('./templates')
env = Environment(loader=loader)

HEAD = 'HTTP/1.1 200 OK\r\nServer: Leo\r\nContent-Type: text/html\r\n\r\n'


def login(request):
    template = env.get_template('login.html')
    return HEAD + template.render(username='陌生人', result='未登陆')


def result(request):
    template = env.get_template('result.html')
    try:
        if request.data['username'] == 'lee' and request.data['password'] == '123':
            login_result = '登陆成功'
        else:
            login_result = '登陆失败'
        return HEAD + template.render(username=request.data['username'], password=request.data['password'], result=login_result)
    except KeyError:
        return HEAD + '<html><body><h1 style="text-align:center">Input is wrong!</h1></body></html>'
