import os
import socket
import cv2
import sys
import pickle
import bz2


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 12345))

path = input("Enter the image path: ")

sample = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

sift = cv2.SIFT_create()
keypoints, descriptor = sift.detectAndCompute(sample, None)
print(keypoints)

keypoints_as_tuples = [(kp.pt, kp.size, kp.angle, kp.response, kp.octave, kp.class_id) for kp in keypoints]
keypoints_data = pickle.dumps(keypoints_as_tuples)
descriptor_data = pickle.dumps(descriptor)
print(keypoints_data)

#Compression using Bz2
with bz2.BZ2File('compressed_keypoints.pkl.bz2', 'wb', compresslevel=9) as f:
    pickle.dump(keypoints_data, f)
with bz2.BZ2File('compressed_descriptor.pkl.bz2', 'wb', compresslevel=9) as f:
    pickle.dump(descriptor_data, f)

size = os.path.getsize(r'E:\ISRO\VSSC\Fingerprint_analysis\fingerprint using client server\compressed_keypoints.pkl.bz2')
client.send(size.to_bytes(4, 'big'))
file = open(r'E:\ISRO\VSSC\Fingerprint_analysis\fingerprint using client server\compressed_keypoints.pkl.bz2', 'rb')
keypoints_data = file.read(size)
client.send(keypoints_data)
file.close()

keypoints_decompossed = open(r'E:\ISRO\VSSC\Fingerprint_analysis\fingerprint using client server\normal.pkl')
data = keypoints_decompossed.read(keypoints_decompossed)
decompress=bz2.decompress(data)
loaded=pickle.loads(decompress)
print(pickle.loads(loaded))
# keypoints_unpickled = pickle.loads(keypoints_decompossed)
# print(keypoints_decompossed)

data = client.recv(1024)
print(data.decode())

client.close()