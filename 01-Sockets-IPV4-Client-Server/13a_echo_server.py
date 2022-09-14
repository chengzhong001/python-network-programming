#!/usr/bin/env python3

import argparse
import socket

host = "localhost"
data_playload = 2048
backlog = 5


def echo_server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    server_address = (host, port)
    sock.bind(server_address)
    sock.listen(backlog)
    while True:
        print("Waiting to receive message from client")
        client, address = sock.accept()
        data = client.recv(data_playload)
        if data:
            print(f"Data: {data.decode()}")
            client.send(data)
            print(f"sent {data.decode()} bytes back to {address}")
            client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Socket Server Example")
    parser.add_argument("--port", action="store", dest="port", type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    echo_server(port)
