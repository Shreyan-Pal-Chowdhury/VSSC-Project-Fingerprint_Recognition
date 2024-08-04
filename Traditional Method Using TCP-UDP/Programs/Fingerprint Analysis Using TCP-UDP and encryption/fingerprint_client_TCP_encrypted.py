import socket
import cv2
import pickle
import bz2
import sys
import rsa

ID = 10124

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 12345))

publicKey = pickle.load(open(r'E:\ISRO\VSSC\Fingerprint_analysis\fingerprint using client server\publicKey.pkl', 'rb'))

ID_encrypt = rsa.encrypt(str(ID).encode(), publicKey)
client.send(ID_encrypt)

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
client.send(size.to_bytes(4, 'big'))
client.send(compressed_keypoints)


#Sending descriptor data
size = sys.getsizeof(compressed_descriptors)
client.send(size.to_bytes(8, 'big'))

try:
    client.send(compressed_descriptors)
except Exception:
    print("Connection Closed by Server!!")
    exit()

try:
    data = client.recv(1024)
except Exception:
    print("Connection Closed by Server!!")
    exit()
print("massege received")
print(data.decode())

client.close()