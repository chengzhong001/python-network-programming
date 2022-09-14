#!/usr/bin/env python3
# coding:utf-8
'''
Description: 从网络时间服务器获取并打印当前时间
Author: zhengchengzhong
Date: 2021-02-13 11:10:47
'''
from time import ctime

import ntplib


def print_time():
    ntp_client = ntplib.NTPClient()
    response = ntp_client.request('pool.ntp.org')
    print(ctime(response.tx_time))


if __name__ == '__main__':
    print_time()
