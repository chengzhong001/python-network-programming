#!/usr/bin/env python3
# coding:utf-8
'''
Description: 通过指定的端口和协议找到服务名
Author: zhengchengzhong
Date: 2021-02-13 10:11:54
'''
import socket

def find_service_name():
    protocolname = "tcp"
    for port in [80, 25, 443]:
        print(f"port: {port} => service name: {socket.getservbyport(port, protocolname)}" )
    print(f"port: {53} => service name: {socket.getservbyport(53, 'udp')}" )

if __name__ == "__main__":
    find_service_name()