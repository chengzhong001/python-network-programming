import argparse
import os
import select
import socket
import struct
import time

ICMP_ECHO_REQUEST = 8
DEFAULT_TIME = 2
DEFAULT_COUNT = 4


class Pinger:
    def __init__(self, target_host, count=DEFAULT_COUNT, timeout=DEFAULT_TIME) -> None:
        self.target_host = target_host
        self.count = count
        self.timeout = timeout

    def do_checksum(self, source_string):
        sum = 0
        max_count = (len(source_string) / 2) * 2
        count = 0
        while count < max_count:
            val = source_string[count + 1] * 256 + source_string[count]
            sum += val
            sum &= 0xFFFFFFFF
            count += 2

        if max_count < len(source_string):
            sum += ord(source_string[len(source_string) - 1])
            sum &= 0xFFFFFFFF

        sum = (sum >> 16) + (sum & 0xFFFF)
        sum += sum >> 16
        answer = ~sum
        answer &= 0xFFFF
        answer = answer >> 8 | (answer << 8 & 0xFF00)
        return answer

    def receive_pong(self, sock: socket.socket, ID, timeout):
        time_remaining = timeout

        while True:
            start_time = time.time()
            readable = select.select([sock], [], [], time_remaining)
            time_spent = time.time() - start_time
            if readable[0] == []:
                return
            time_received = time.time()
            recv_packet, addr = sock.recvfrom(1024)
            icmp_header = recv_packet[20:28]
            type, code, checksum, packet_id, sequence = struct.unpack(
                "bbHHh", icmp_header
            )

            if packet_id == ID:
                bytes_in_double = struct.calcsize("d")
                time_sent = struct.unpack("d", recv_packet[28 : 28 + bytes_in_double])[
                    0
                ]
                return time_received - time_sent
            time_remaining = time_remaining - time_spent
            if time_remaining <= 0:
                return

    def send_ping(self, sock: socket.socket, ID):
        target_addr = socket.gethostbyname(self.target_host)
        my_checksum = 0
        header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
        bytes_in_double = struct.calcsize("d")
        data = (192 - bytes_in_double) * "Q"
        data = struct.pack("d", time.time()) + bytes(data.encode("utf-8"))
        my_checksum = self.do_checksum(header + data)
        header = struct.pack(
            "bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), ID, 1
        )
        packet = header + data
        sock.sendto(packet, (target_addr, 1))

    def ping_once(self):
        icmp = socket.getprotobyname("icmp")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)

        except socket.error as e:
            if e.errno == 1:
                e.msg = "ICMP messages can only be sent from root user processes"
                raise socket.error(e.msg)
        except Exception as e:
            print("Exception:", e)

        my_ID = os.getpid() & 0xFFFF
        self.send_ping(sock, my_ID)
        delay = self.receive_pong(sock, my_ID, self.timeout)
        sock.close
        return delay

    def ping(self):
        for i in range(self.count):
            print(f"Ping to {self.target_host}...")
            try:
                delay = self.ping_once()
            except socket.gaierror as e:
                print(f"Ping failed. (socket error: {e[1]})")

            if delay == None:
                print(f"Ping failed. (timeout within {self.timeout}sec.)")
            else:
                delay = delay * 1000
                print("Got pong in {:.4f} ms".format(delay))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python ping")
    parser.add_argument(
        "--target-host", action="store", dest="target_host", required=True
    )
    given_args = parser.parse_args()
    target_host = given_args.target_host
    pinger = Pinger(target_host=target_host)
    pinger.ping()
