import argparse
import fcntl
import socket
import struct

import nmap

SAMPLE_PORT = "21-23"


def get_interface_status(ifname):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip_address = socket.inet_ntoa(
        fcntl.ioctl(
            sock.fileno(), 0x8915, struct.pack(b"256s", bytes(ifname[:15], "utf-8"))
        )[20:24]
    )
    nm = nmap.PortScanner()
    nm.scan(ip_address, SAMPLE_PORT)
    return nm[ip_address].state()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python networking utils")
    parser.add_argument("--ifname", action="store", dest="ifname", required=True)
    given_args = parser.parse_args()
    ifname = given_args.ifname
    print(f"Interface {ifname} is : {get_interface_status(ifname)}")
