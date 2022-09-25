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
        max_count = (len(source_string) // 2) * 2
        count = 0
        while count < max_count:
            val = ord(source_string[count + 1] * 256 + ord(source_string[count]))
            sum = sum + val
            sum = sum & 0xFFFFFFFF
            count = count + 2

        if max_count < len(source_string):
            sum = sum + ord(source_string)
            sum = sum & 0xFFFFFFFF

        sum = (sum >> 16) + (sum & 0xFFFF)
        sum = sum + (sum >> 16)
        answer = answer & 0xFFFF
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

    