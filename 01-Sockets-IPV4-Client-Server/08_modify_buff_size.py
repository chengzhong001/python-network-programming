#!/usr/bin/env python3
# coding:utf-8
'''
Description: 修改套接字发送和接收的缓冲区大小
Author: zhengchengzhong
Date: 2021-02-13 10:35:18
'''
import socket

SEND_BUF_SIZE = 4096
RECV_BUF_SIZE = 4096


def modify_buff_size():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    buffsize = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    print(f"Buffer size [Before]: {buffsize}")

    sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, SEND_BUF_SIZE)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, RECV_BUF_SIZE)

    buffsize = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    print(buffsize)


if __name__ == "__main__":
    modify_buff_size()
