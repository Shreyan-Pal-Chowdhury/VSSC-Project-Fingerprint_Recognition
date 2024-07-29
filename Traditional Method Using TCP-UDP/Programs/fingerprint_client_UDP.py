import socket
import cv2
import pickle
import bz2

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

path = input("Enter your image: ")
sample = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

sift = cv2.SIFT_create()
keypoints, descriptor = sift.detectAndCompute(sample, None)

keypoints_as_tuples = [(kp.pt, kp.size, kp.angle, kp.response, kp.octave, kp.class_id) for kp in keypoints]
keypoints_data = pickle.dumps(keypoints_as_tuples)
descriptor_data = pickle.dumps(descriptor)
print(keypoints)
print(descriptor)

#Compression Using Bz2
with bz2.BZ2File('compressed_keypoints_UDP.pkl.bz2', 'wb', compresslevel=9) as f:
    pickle.dump(keypoints_data, f)
with bz2.BZ2File('compressed_descriptor_UDP.pkl.bz2', 'wb', compresslevel=9) as f:
    pickle.dump(descriptor_data, f)

#Sending Keypoints data
file = open(r'E:\ISRO\VSSC\Fingerprint_analysis\fingerprint using client server\compressed_keypoints_UDP.pkl.bz2', 'rb')
keypoints_data = file.read(2048)

while keypoints_data:
    client.sendto(keypoints_data, ('localhost', 12345))
    keypoints_data = file.read(2048)

file.close()

client.sendto(b'0', ('localhost',12345))

#Sending descriptor data
file = open(r'E:\ISRO\VSSC\Fingerprint_analysis\fingerprint using client server\compressed_descriptor_UDP.pkl.bz2', 'rb')
descriptor_data = file.read(2048)

while descriptor_data:
    client.sendto(descriptor_data, ('localhost', 12345))
    descriptor_data = file.read(2048)

file.close()

client.sendto(b'0', ('localhost', 12345))


data, add = client.recvfrom(2048)
print(data.decode())

file.close()
client.close()
