#!/usr/bin/env python3
# coding:utf-8
'''
Description: 将 IPv4 地址转换成不同的格式
Author: zhengchengzhong
Date: 2021-02-13 10:06:27
'''
import socket
from binascii import hexlify


def conver_ip4_address():
    for ip_addr in ['127.0.0.1', '192.168.0.1']:
        packed_ip = socket.inet_aton(ip_addr)
        unpacked_ip = socket.inet_ntoa(packed_ip)
        print(
            f"IP Address: {ip_addr} => Packed: {hexlify(packed_ip)}, Unpacked: {unpacked_ip}")


if __name__ == "__main__":
    conver_ip4_address()
