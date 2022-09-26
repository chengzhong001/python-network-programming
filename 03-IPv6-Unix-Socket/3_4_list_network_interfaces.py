import array
import fcntl
import socket
import struct
import sys

SIOGIFCONF = 0x8912
STUCT_SIZE_32 = 32
STUCT_SIZE_64 = 40
PLATFORM_32_MAX_NUMBER = 2**32
DEFAULT_INTERFACES = 8


def list_interfaces():
    interfaces = []
    max_interfaces = DEFAULT_INTERFACES
    is_64bits = sys.maxsize > PLATFORM_32_MAX_NUMBER
    struct_size = STUCT_SIZE_64 if is_64bits else STUCT_SIZE_32
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        bytes = max_interfaces * struct_size
        interface_names = array.array('B', b"\0" * bytes)
        sock_info = fcntl.ioctl(
            sock.fileno(),
            SIOGIFCONF,
            struct.pack("iL", bytes, interface_names.buffer_info()[0])
        )
        outbytes = struct.unpack("iL", sock_info)[0]
        if outbytes == bytes:
            max_interfaces *= 2
        else:
            break

    namestr = interface_names.tobytes()
    for i in range(0, outbytes, struct_size):
        interfaces.append(
            (namestr[i : i + 16].split(b"\0", 1)[0]).decode("ascii", "ignore")
        )
    return interfaces


if __name__ == "__main__":
    interfaces = list_interfaces()
    print("This machine has %s network interfaces: %s." % (len(interfaces), interfaces))