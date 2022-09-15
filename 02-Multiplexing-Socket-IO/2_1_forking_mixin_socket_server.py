import os
import socket
import socketserver
import threading

SERVER_HOST = "localhost"
SERVER_PORT = 0  # tells the kernel to pick up a port dynamically
BUF_SIZE = 1024
ECHO_MSG = "Hello echo server!"


class ForkingClient:
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))

    def run(self):
        current_process_id = os.getpid()
        print(
            f"PID {current_process_id} Sending echo message to the server: {ECHO_MSG}"
        )
        send_data_length = self.sock.send(ECHO_MSG.encode())
        print(f"Sent: {send_data_length} characters, so far...")

        response = self.sock.recv(BUF_SIZE, 0)
        print(f"PID {current_process_id}s received: {response[5:]}")

    def shutdown(self):
        self.sock.close()


class ForkingServerRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(BUF_SIZE)
        current_process_id = os.getpid()
        response = f"{current_process_id}: {data}"
        print(f"Server sending response [current_process_id: data] = {response}")
        self.request.send(response.encode())
        return None


class ForkingServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


def main():
    server = ForkingServer((SERVER_HOST, SERVER_PORT), ForkingServerRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    # server_thread.setDaemon(True)  # don't hang on exit
    server_thread.daemon = True
    server_thread.start()
    print(f"Server loop running PID: {os.getpid()}")
    # Launch the client(s)
    client1 = ForkingClient(ip, port)
    client1.run()
    client2 = ForkingClient(ip, port)
    client2.run()
    # Clean them up
    server.shutdown()
    client1.shutdown()
    client2.shutdown()
    server.socket.close()


if __name__ == "__main__":
    main()
