import argparse
from scapy.all import *

def ping(destination, timeout=1, count=4):
    for seq in range(count):
        packet = IP(dst=destination) / ICMP(seq=seq)
        start_time = time.time()
        reply = sr1(packet, timeout=timeout, verbose=0)
        end_time = time.time()

        if reply is None:
            print(f"Request timed out.")
        else:
            rtt = (end_time - start_time) * 1000
            print(f"Reply from {reply.src}: time={rtt:.2f}ms")

        time.sleep(1)

def main():
    parser = argparse.ArgumentParser(description="A simple ping script using Python and Scapy")
    parser.add_argument("destination", help="The destination IP address or hostname to ping")
    parser.add_argument("-t", "--timeout", type=int, default=1, help="Timeout in seconds to wait for each reply")
    parser.add_argument("-c", "--count", type=int, default=4, help="Number of echo requests to send")

    args = parser.parse_args()
    destination = args.destination
    timeout = args.timeout
    count = args.count

    print(f"Pinging {destination} with {count} packets:")
    ping(destination, timeout, count)

if __name__ == "__main__":
    main()
