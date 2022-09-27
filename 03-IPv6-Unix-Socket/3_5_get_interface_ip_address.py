import argparse
import fcntl
import socket
import struct


def get_ip_address(ifname):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return socket.inet_ntoa(
        fcntl.ioctl(
            sock.fileno(), 0x8915, struct.pack(b"256s", ifname[:15].encode("utf-8"))
        )[20:24]
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python networking utils")
    parser.add_argument("--ifname", action="store", dest="ifname", required=True)
    given_args = parser.parse_args()
    ifname = given_args.ifname
    _ifname = get_ip_address(ifname)
    print(f"Interface {ifname}-->IP: {_ifname}")
