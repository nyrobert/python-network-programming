import os
import socket
import struct
import time
import select
import argparse

ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0

def checksum(source_string):
    sum = 0
    count_to = (len(source_string) // 2) * 2
    count = 0

    while count < count_to:
        this_val = source_string[count + 1] * 256 + source_string[count]
        sum = sum + this_val
        sum = sum & 0xffffffff
        count = count + 2

    if count_to < len(source_string):
        sum = sum + source_string[len(source_string) - 1]
        sum = sum & 0xffffffff

    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def create_packet(id):
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, 0, id, 1)
    data = struct.pack("d", time.time())
    my_checksum = checksum(header + data)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), id, 1)
    return header + data

def do_one_ping(dest_addr, timeout):
    icmp = socket.getprotobyname("icmp")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    except PermissionError as e:
        print("Operation not permitted: ICMP messages can only be sent from processes running as root.")
        return

    my_id = os.getpid() & 0xFFFF
    packet = create_packet(my_id)
    while packet:
        sent = sock.sendto(packet, (dest_addr, 1))
        packet = packet[sent:]

    delay = receive_one_ping(sock, my_id, timeout)
    sock.close()
    return delay

def receive_one_ping(sock, my_id, timeout):
    time_left = timeout / 1000
    while True:
        started_select = time.time()
        ready = select.select([sock], [], [], time_left)
        how_long_in_select = (time.time() - started_select)
        if ready[0] == []:  # Timeout
            return None

        time_received = time.time()
        rec_packet, addr = sock.recvfrom(1024)
        icmp_header = rec_packet[20:28]
        type, code, checksum, packet_id, sequence = struct.unpack("bbHHh", icmp_header)
        if packet_id == my_id:
            bytes_in_double = struct.calcsize("d")
            time_sent = struct.unpack("d", rec_packet[28:28 + bytes_in_double])[0]
            return time_received - time_sent

        time_left = time_left - how_long_in_select
        if time_left <= 0:
            return None

def ping(dest_addr, timeout=1000, count=4):
    for i in range(count):
        print(f"Pinging {dest_addr}...")
        delay = do_one_ping(dest_addr, timeout)
        if delay is None:
            print(f"Request timed out.")
        else:
            delay = delay * 1000
            print(f"Reply from {dest_addr}: time={delay:.2f}ms")
        time.sleep(1)

def main():
    parser = argparse.ArgumentParser(description="A simple ping script in Python")
    parser.add_argument("destination", help="The destination IP address or hostname to ping")
    parser.add_argument("-t", "--timeout", type=int, default=1000, help="Timeout in milliseconds to wait for each reply")
    parser.add_argument("-c", "--count", type=int, default=4, help="Number of echo requests to send")

    args = parser.parse_args()
    dest_addr = socket.gethostbyname(args.destination)

    print(f"Pinging {dest_addr} with {args.count} packets:")
    ping(dest_addr, args.timeout, args.count)

if __name__ == "__main__":
    main()
