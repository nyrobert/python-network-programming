import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ("127.0.0.1", 12345)
server_socket.bind(server_address)

print("Waiting for connections...")

data, client_address = server_socket.recvfrom(4096)
print(f"Connected: {client_address}")
print(f"Message: {data.decode()}")

server_socket.sendto(b"Hello, client!", client_address)
