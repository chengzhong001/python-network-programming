import argparse
import asyncore
import socket

LOCAL_SERVER_HOST = "localhost"
REMOTE_SERVER_HOST = "www.baidu.com"
BUFSIZE = 4096


class PortForwarder(asyncore.dispatcher):
    def __init__(self, ip, port, remote_ip, remote_port, backlog=5) -> None:
        asyncore.dispatcher.__init__(self)
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((ip, port))
        self.listen(backlog)

    def handle_accept(self) -> None:
        conn, addr = self.accept()
        print("Connected to:", addr)
        Sender(Receiver(conn), self.remote_ip, self.remote_port)


class Receiver(asyncore.dispatcher):
    def __init__(self, conn) -> None:
        super().__init__(self, conn)
        self.from_remote_buffer = ""
        self.to_remote_buffer = ""
        self.sender = None

    def handle_connect(self) -> None:
        pass

    def handle_read(self) -> None:
        read = self.recv(BUFSIZE)
        self.from_remote_buffer += read

    def writable(self):
        return len(self.to_remote_buffer) > 0

    def handle_write(self) -> None:
        sent = self.send(self.to_remote_buffer)
        self.to_remote_buffer = self.to_remote_buffer[sent:]

    def handle_close(self):
        self.close()
        if self.sender:
            self.sender.close()


class Sender(asyncore.dispatcher):
    def __init__(self, receiver: Receiver, remote_addr, remote_port) -> None:
        super.__init__(self)
        self.reveiver = receiver
        receiver.sender = self
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((remote_addr, remote_port))

    def handle_connect(self) -> None:
        pass

    def handle_read(self):
        read = self.recv(BUFSIZE)
        self.reveiver.to_remote_buffer += read

    def writable(self):
        return len(self.receiver.from_remote_buffer) > 0

    def handle_write(self) -> None:
        sent = self.send(self.receiver.from_remote_buffer)
        self.receiver.from_remote_buffer = self.receiver.from_remote_buffer[sent:]

    def handle_close(self) -> None:
        self.close()
        self.receiver.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stackless Socket Server Example")
    parser.add_argument(
        "--local-host", action="store", dest="local_host", default=LOCAL_SERVER_HOST
    )
    parser.add_argument(
        "--local-port", action="store", dest="local_port", type=int, required=True
    )
    parser.add_argument(
        "--remote-host", action="store", dest="remote_host", default=REMOTE_SERVER_HOST
    )
    parser.add_argument(
        "--remote-port", action="store", dest="remote_port", type=int, default=80
    )

    given_args = parser.parse_args()
    local_host, remote_host = given_args.local_host, given_args.remote_host
    local_port, remote_port = given_args.local_port, given_args.remote_port
    print(
        f"Starting port forwarding local {local_host}:{local_port} => remote {remote_host}:{remote_port}"
    )
    PortForwarder(local_host, local_port, remote_host, remote_port)
    asyncore.loop()
