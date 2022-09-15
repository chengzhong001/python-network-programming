import socket
import socketserver
import threading

SERVER_HOST = "localhost"
SERVER_PORT = 0
BUF_SIZE = 1024


def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message.encode())
        response = sock.recv(BUF_SIZE)
        print(f"Client received: {response.decode()}")
    finally:
        sock.close()


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        current_thread = threading.current_thread()
        response = f"{current_thread}: {data}"
        self.request.sendall(response.encode())


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    server = ThreadedTCPServer((SERVER_HOST, SERVER_PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print(f"Server loop running on thread: {server_thread.name}")
    client(ip, port, "Hello from client1")
    client(ip, port, "Hello from client2")
    client(ip, port, "Hello from client3")

    server.shutdown()
