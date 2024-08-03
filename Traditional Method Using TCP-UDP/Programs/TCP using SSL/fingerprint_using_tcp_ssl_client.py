import socket
import ssl
import cv2
import pickle
import bz2
import sys

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations('E:\ISRO\VSSC\Fingerprint_analysis\server.crt')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_client = context.wrap_socket(client, server_hostname='localhost')
ssl_client.connect(('localhost', 12345))

path = input("Enter the image path: ")

try:
    file = open(path)
    sample = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
except OSError:
    print("Unable to read file!")
    exit()

sift = cv2.SIFT_create()

try:
    keypoints, descriptor = sift.detectAndCompute(sample, None)
except cv2.error:
    print("Wrong File format!")
    exit()

keypoints_as_tuples = [(kp.pt, kp.size, kp.angle, kp.response, kp.octave, kp.class_id) for kp in keypoints]
keypoints_data = pickle.dumps(keypoints_as_tuples)
descriptor_data = pickle.dumps(descriptor)

#Compression using Bz2
compressed_keypoints = bz2.compress(keypoints_data)
compressed_descriptors = bz2.compress(descriptor_data)

#Sending keypoints data
size = sys.getsizeof(compressed_keypoints)
ssl_client.send(size.to_bytes(4, 'big'))
ssl_client.send(compressed_keypoints)
print(size)
print(compressed_keypoints)


#Sending descriptor data
size = sys.getsizeof(compressed_descriptors)
ssl_client.send(size.to_bytes(8, 'big'))

try:
    ssl_client.send(compressed_descriptors)
except Exception:
    print("Connection Closed by Server!!")
    exit()

try:
    data = ssl_client.recv(1024)
except Exception:
    print("Connection Closed by Server!!")
    exit()

print("massege received")
print(data.decode())

client.close()