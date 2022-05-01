#!/usr/bin/env python3
# coding:utf-8
'''
Description: 编写一个 SNTP 客户端
Author: zhengchengzhong
Date: 2021-02-13 11:18:26
'''
import socket
import struct
import sys
import time

NTP_SERVER = "0.uk.pool.ntp.org"
TIME1970 = 2208988800


def sntp_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = '\x1b' + 47 * '\0'
    print(data)
    t = struct.unpack('!12I', data.encode())
    print(t)
    client.sendto(data.encode(), (NTP_SERVER, 123))
    data, address = client.recvfrom(1024)
    print(data, address)
    if data:
        print("Response Received from:", address)
    t = struct.unpack('!12I', data)[10]
    print(t)
    t -= TIME1970
    print("Time={}".format(time.ctime(t)))


if __name__ == '__main__':
    sntp_client()
