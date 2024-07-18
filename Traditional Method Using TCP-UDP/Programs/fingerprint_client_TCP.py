import os
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 12345))

path = input("Enter your image: ")
file = open(path, 'rb')
size = os.path.getsize(path)

image_data = file.read(size)
client.send(size.to_bytes(4, 'big'))

client.send(image_data)

file.close()

data = client.recv(1024)
print(data.decode())

client.close()
