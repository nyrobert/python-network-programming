"""
- On macOS you will need the SCTP NKE (Kernel Extensions).
- On Linux systems, you need an SCTP-aware kernel (most are) and install the following packages: apt install libsctp-dev libsctp1 lksctp-tools
"""


import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_SCTP)

server_address = ("127.0.0.1", 12345)
server_socket.bind(server_address)

server_socket.listen(5)
print("Waiting for connections...")

client_socket, client_address = server_socket.accept()
print(f"Connected: {client_address}")

data = client_socket.recv(1024)
print(f"Message: {data.decode()}")

client_socket.send(b"Hello, client!")

client_socket.close()
server_socket.close()
