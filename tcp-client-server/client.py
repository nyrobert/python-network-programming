import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("127.0.0.1", 12345)
client_socket.connect(server_address)

client_socket.send(b"Hello, server!")

data = client_socket.recv(1024)
print(f"Message: {data.decode()}")

client_socket.close()
