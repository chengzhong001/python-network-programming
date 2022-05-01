#!/usr/bin/env python3
# coding:utf-8
'''
Description: 把套接字改成阻塞或非阻塞模式
Author: zhengchengzhong
Date: 2021-02-13 10:41:11
'''
import socket

def test_socket_modes():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setblocking(True) # Blocking mode
    s.settimeout(0.5)
    s.bind(("127.0.0.1", 0))
    
    socket_address = s.getsockname()
    print(f"Trivial Server launched on socket: {socket_address}")

    while True:
        s.listen(1)
        

if __name__ == "__main__":
    test_socket_modes()