#!/usr/bin/env python3
# coding:utf-8
'''
Description: 主机字节序和网络字节序之间相互转换
Author: zhengchengzhong
Date: 2021-02-13 10:14:48
'''
import socket


def convert_integer():
    data = 1234
    print(
        f"Original: {data} => Long host byte order: {socket.ntohl(data)}, Network byte order: {socket.htonl(data)}")
    print(
        f"Original: {data} => Long host byte order: {socket.ntohs(data)}, Network byte order: {socket.htons(data)}")


if __name__ == "__main__":
    convert_integer()
