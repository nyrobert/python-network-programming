"""
- On macOS you will need the SCTP NKE (Kernel Extensions).
- On Linux systems, you need an SCTP-aware kernel (most are) and install the following packages: apt install libsctp-dev libsctp1 lksctp-tools
"""


import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_SCTP)

server_address = ("127.0.0.1", 12345)
client_socket.connect(server_address)

client_socket.send(b"Hello, server!")

data = client_socket.recv(1024)
print(f"Message: {data.decode()}")

client_socket.close()
