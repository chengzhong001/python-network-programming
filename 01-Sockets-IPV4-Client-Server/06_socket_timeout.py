#!/usr/bin/env python3
# coding:utf-8
'''
Description: 设定并获取默认的套接字超时时间
Author: zhengchengzhong
Date: 2021-02-13 10:22:48
'''
import socket


def test_socket_timeout():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Default socket timeout: {s.gettimeout()}")
    s.settimeout(100)
    print(f"Current socket timeout: {s.gettimeout()}")


if __name__ == "__main__":
    test_socket_timeout()
