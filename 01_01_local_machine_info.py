#!/usr/bin/env python3
# coding:utf-8
'''
Description: 打印本机设备名和 IPv4 地址
Author: zhengchengzhong
Date: 2021-02-13 09:39:10
'''
import socket


def print_machine_info():
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    print(f"Host name: {host_name}")
    print(f"IP address: {ip_address}")


if __name__ == '__main__':
    print_machine_info()
