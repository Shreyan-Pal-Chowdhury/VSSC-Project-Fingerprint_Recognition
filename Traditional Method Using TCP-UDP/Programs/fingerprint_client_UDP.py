import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

path = input("Enter your image: ")
file = open(path, 'rb')
image_data = file.read(2048)

while image_data:
    client.sendto(image_data, ('localhost', 12345))
    image_data = file.read(2048)

client.sendto(b'0', ('localhost',12345))

data, add = client.recvfrom(2048)
print(data.decode())

file.close()
client.close()
