import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("127.0.0.1", 12345)
server_socket.bind(server_address)

server_socket.listen(1)
print("Waiting for connections...")

client_socket, client_address = server_socket.accept()
print(f"Connected: {client_address}")

data = client_socket.recv(1024)
print(f"Message: {data.decode()}")

client_socket.send(b"Hello, client!")

client_socket.close()
server_socket.close()
