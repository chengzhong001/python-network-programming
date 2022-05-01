#!/usr/bin/env python3
# coding:utf-8
'''
Description: 打印远程IP地址
Author: zhengchengzhong
Date: 2021-02-13 09:40:38
'''
import socket


def get_remote_machine_info():
    remote_host = "www.python.org"
    try:
        host_ip = socket.gethostbyname(remote_host)
        print(f"IP address: {host_ip}")
    except socket.error as error_msg:
        print(f"{remote_host}:{error_msg}")


if __name__ == "__main__":
    get_remote_machine_info()
