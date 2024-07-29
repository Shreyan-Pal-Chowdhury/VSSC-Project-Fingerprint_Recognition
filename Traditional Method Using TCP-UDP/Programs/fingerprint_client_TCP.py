import os
import socket
import cv2
import pickle
import bz2


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 12345))

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
with bz2.BZ2File('compressed_keypoints.pkl.bz2', 'wb', compresslevel=9) as f:
    pickle.dump(keypoints_data, f)
with bz2.BZ2File('compressed_descriptor.pkl.bz2', 'wb', compresslevel=9) as f:
    pickle.dump(descriptor_data, f)

#Sending keypoints data
size = os.path.getsize(r'E:\ISRO\VSSC\Fingerprint_analysis\fingerprint using client server\compressed_keypoints.pkl.bz2')
client.send(size.to_bytes(4, 'big'))
file = open(r'E:\ISRO\VSSC\Fingerprint_analysis\fingerprint using client server\compressed_keypoints.pkl.bz2', 'rb')
keypoints_data = file.read(size)
client.send(keypoints_data)
file.close()

#Sending descriptor data
size = os.path.getsize(r'E:\ISRO\VSSC\Fingerprint_analysis\fingerprint using client server\compressed_descriptor.pkl.bz2')
print(size)
client.send(size.to_bytes(4, 'big'))
file = open(r'E:\ISRO\VSSC\Fingerprint_analysis\fingerprint using client server\compressed_descriptor.pkl.bz2', 'rb')
descriptor_data = file.read(size)
try:
    client.send(descriptor_data)
    file.close()
except ConnectionResetError:
    print("Connection Closed by Server!!")
    exit()

try:
    data = client.recv(1024)
except ConnectionAbortedError:
    print("Connection Closed by Server!!")
    exit()
print("massege received")
print(data.decode())

client.close()
