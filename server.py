# -*- coding: utf-8 -*-

from util import move301, move302, log, get_src
from socket import *
from request import Request
from settings import *
import thread


# 处理请求并返回相应的信息
def process_request(conn, addr):
    req = conn.recv(1024)
    # 防止浏览器发送空请求导致崩溃
    if len(req.split()) < 2:
        return
    src = get_src(req)

    if src in MOVE301.keys():
        conn.sendall(move301(src))
    elif src in MOVE302.keys():
        conn.sendall(move302(src))
    else:
        request = Request(req)
        print(request.method + ' > ' + str(request.src))
        response = request.response

        if request.src in ROUTES:
            response = ROUTES[request.src](request)

        conn.sendall(response)

    conn.close()
    # 结束连接


# 监听请求并为每个请求分配一个线程
def run(host, port):
    s = socket(AF_INET, SOCK_STREAM)
    # AF_INET 指用IPv4协议 ，SOCK_STREAM指用TCP协议连接
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # 保证程序重启后使用原有端口
    s.bind((host, port))
    # 绑定host和端口
    s.listen(5)
    # 监听请求
    print('Web Server start > listen ' + HOST + ':' + PORT + '\n')
    log('Web Server start > listen ' + HOST + ':' + PORT + '\n')
    while True:
        conn, addr = s.accept()
        thread.start_new_thread(process_request, (conn, addr))
        # 为每个请求建立一个线程


if __name__ == '__main__':
    run(HOST, int(PORT))
