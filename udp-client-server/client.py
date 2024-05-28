import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ("127.0.0.1", 12345)

client_socket.sendto(b"Hello, server!", server_address)

data, server = client_socket.recvfrom(4096)
print(f"Message: {data.decode()}")

client_socket.close()
