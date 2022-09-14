#!/usr/bin/env python3
# coding:utf-8
'''
Description: 优雅地处理套接字错误
Author: zhengchengzhong
Date: 2021-02-13 10:28:14
'''
import argparse
import socket
import sys


def main():
    parser = argparse.ArgumentParser(description="Socket error example")
    parser.add_argument("--host", action="store", dest="host", required=False)
    parser.add_argument("--port", action="store",
                        dest="port", type=int, required=False)
    parser.add_argument("--file", action="store", dest="file", required=False)
    given_args = parser.parse_args()
    host = given_args.host
    port = given_args.port
    filename = given_args.file
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    except socket.error as e:
        print(f"Error creating socket: {e}")
        sys.exit(1)

    try:
        s.connect((host, port))

    except socket.gaierror as e:
        print(f"Address-related error connecting to server: {e}")
        sys.exit(1)
    except socket.error as e:
        print(f"Connection error: {e}")
        sys.exit(1)
    try:
        s.sendall(f"GET {filename}s HTTP/1.0\r\n\r\n".encode())

    except socket.error as e:
        print(f"Error sending data: {e}")
        sys.exit(1)
    while True:
        try:
            buf = s.recv(1024)

        except socket.error as e:
            print(f"Error receiving data: {e}")
            sys.exit(1)
        if not len(buf):
            break
        sys.stdout.write(buf.decode())


if __name__ == "__main__":
    main()
