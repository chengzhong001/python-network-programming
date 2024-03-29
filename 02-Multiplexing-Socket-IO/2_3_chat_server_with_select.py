import argparse
import pickle
import select
import signal
import socket
import struct
import sys

SERVER_HOST = "localhost"
CHAT_SERVER_NAME = "server"


def send(channel: socket.socket, *args):
    buffer = pickle.dumps(args)
    value = socket.htonl(len(buffer))
    size = struct.pack("L", value)
    channel.send(size)
    channel.send(buffer)


def receive(channel: socket.socket):
    size = struct.calcsize("L")
    size = channel.recv(size)
    try:
        size = socket.ntohl(struct.unpack("L", size)[0])
    except struct.error as e:
        return ""
    buf = ""
    while len(buf) < size:
        buf = channel.recv(size - len(buf))
    return pickle.loads(buf)[0]


class ChatServer:
    def __init__(self, port, backlog=5) -> None:
        self.clients = 0
        self.clientmap = {}
        self.outputs = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((SERVER_HOST, port))
        print(f"Server listen to port: {port}")
        self.server.listen(backlog)
        signal.signal(signal.SIGINT, self.sighandler)

    def sighandler(self, signum, frame):
        print(" shutting down server...")
        for output in self.outputs:
            output.close()
        self.server.close()

    def get_client_name(self, client):
        info = self.clientmap[client]
        host, name = info[0][0], info[1]
        return "@".join((name, host))

    def run(self):
        inputs = [self.server, sys.stdin]
        self.outputs = []
        running = True
        while running:
            try:
                readable, writeable, exceptional = select.select(inputs, self.outputs, [])
                
            except select.error as e:
                break

            for sock in readable:
                if sock == self.server:
                    client, address = self.server.accept()
                    print(f"Chat server: got connection {client.fileno()} from {address}")
                    cname = receive(client).split("NAME: ")[1]
                    self.clients += 1
                    send(client, "CLIENT: " + str(address[0]))
                    inputs.append(client)
                    self.clientmap[client] = (address, cname)
                    msg = f"\n(Connected: New client ({self.clients} from {self.get_client_name(client)}))"
                    for output in self.outputs:
                        send(output, msg)
                    self.outputs.append(client)

                elif sock == sys.stdin:
                    junk = sys.stdin.readline()
                    running = False
                else:
                    try:
                        data = receive(sock)
                        if data:
                            msg = "\n#[" + self.get_client_name(sock) + "]>>" + data
                            for output in self.outputs:
                                if output != sock:
                                    send(output, msg)
                        else:
                            print(f"Chat server: {sock.fileno()} hung up")
                            self.clients -= 1
                            sock.close()
                            inputs.remove(sock)
                            self.outputs.remove(sock)

                            msg = f"\n(Now hung up: Client from {self.get_client_name(sock)})"
                            for output in self.outputs:
                                send(output, msg)
                    except socket.error as e:
                        inputs.remove(sock)
                        self.outputs.remove(sock)

        self.server.close()


class ChatClient:
    def __init__(self, name, port, host=SERVER_HOST) -> None:
        self.name = name
        self.connected = False
        self.host = host
        self.port = port
        self.prompt = "[" + "@".join((name, socket.gethostname().split(".")[0])) + "]> "

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, self.port))
            print(f"Now connected to char server@port{self.port}")
            self.connected = True
            send(self.sock, "NAME: " + self.name)
            data = receive(self.sock)
            # addr = data.split("CLIENT: ")[1]
            addr = data.split('CLIENT: ')[1]
            self.prompt = "[" + "@".join((self.name, addr)) + "]> "
        except socket.error as e:
            print(f"Failed to connect to chat server@port {self.port}")
            sys.exit(1)

    def run(self):
        while self.connected:
            try:
                sys.stdout.write(self.prompt)
                sys.stdout.flush()
                readable, writeable, exceptional = select.select([0, self.sock], [], [])
                for sock in readable:
                    if sock == 0:
                        data = sys.stdin.readline().strip()
                        if data:
                            send(self.sock, data)
                    elif sock == self.sock:
                        data = receive(self.sock)
                        if not data:
                            print("Client shutting down")
                            self.connected = False 
                            break
                        else:
                            sys.stdout.write(data + "\n")
                            sys.stdout.flush()

            except KeyboardInterrupt:
                print(" Client interrupted")
                self.sock.close()
                break

                


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Socket Server Example with Select")
    parser.add_argument("--name", action="store", dest="name", required=True)
    parser.add_argument("--port", action="store", dest="port", type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    name = given_args.name

    if name == CHAT_SERVER_NAME:
        server = ChatServer(port)
        server.run()
    else:
        client = ChatClient(name=name, port=port)
        client.run()
