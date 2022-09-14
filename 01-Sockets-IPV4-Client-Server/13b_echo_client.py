#!/usr/bin/env python3
import argparse
import socket

host = "localhost"


def echo_client(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    print(f"Connectiong to {port} {server_address}")
    sock.connect(server_address)

    try:
        message = "Test message. This will be echoed".encode()
        print(f"Sending {message}")
        sock.sendall(message)
        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print(f"Received: {data.decode()}")

    except socket.errno as e:
        print(f"Socket error: {e}")
    except Exception as e:
        print(f"Other exception: {e}")
    finally:
        print("Closing connection to the server")
        sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Socket Server Examle")
    parser.add_argument("--port", action="store", dest="port", type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    echo_client(port)