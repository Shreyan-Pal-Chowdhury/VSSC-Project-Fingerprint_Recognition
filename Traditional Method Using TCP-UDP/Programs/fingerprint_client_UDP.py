import socket
import cv2
import pickle
import bz2

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

path = input("Enter your image: ")

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
    try:
        client.sendto(descriptor_data, ('localhost', 12345))
    except ConnectionResetError:
        print("Connection Closed by Server!!")
        exit()
    descriptor_data = file.read(2048)

file.close()

client.sendto(b'0', ('localhost', 12345))

try:
    data, add = client.recvfrom(2048)
except ConnectionAbortedError:
    print("Connection Closed by Server!!")
    exit()

print(data.decode())

file.close()
client.close()
