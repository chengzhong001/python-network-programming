import argparse

import diesel


class EchoServer:
    def handler(self, remote_addr):
        host, port = remote_addr[0], remote_addr[1]
        print(f"Echo client connected {host}:{port}")
        while True:
            try:
                message = diesel.until_eol()
                your_message = ": ".join(["You said", message])
            except Exception as e:
                print("Exception: ", e)


def main(server_port):
    app = diesel.Application()
    server = EchoServer()
    app.add_service(diesel.Service(server.handler, server_port))
    app.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Echo server example with Diesel")
    parser.add_argument('--port', action="store", dest="port",type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    main(port)