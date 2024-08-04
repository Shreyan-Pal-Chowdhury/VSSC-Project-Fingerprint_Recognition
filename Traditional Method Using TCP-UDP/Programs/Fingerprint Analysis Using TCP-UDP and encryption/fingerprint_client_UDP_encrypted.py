import socket
import cv2
import pickle
import bz2
import sys
import rsa

ID = 1002

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

publicKey = pickle.load(open(r'E:\ISRO\VSSC\Fingerprint_analysis\fingerprint using client server\publicKey.pkl', 'rb'))

ID_encrypt = rsa.encrypt(str(ID).encode(), publicKey)
client.sendto(ID_encrypt, ('localhost', 12345))


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
# with bz2.BZ2File('compressed_keypoints_UDP.pkl.bz2', 'wb', compresslevel=9) as f:
#     pickle.dump(keypoints_data, f)
# with bz2.BZ2File('compressed_descriptor_UDP.pkl.bz2', 'wb', compresslevel=9) as f:
#     pickle.dump(descriptor_data, f)
compressed_keypoints = bz2.compress(keypoints_data)
compressed_descriptors = bz2.compress(descriptor_data)

#Sending Keypoints data
size = sys.getsizeof(compressed_keypoints)
client.sendto(size.to_bytes(4, 'big'), ('localhost', 12345))
client.sendto(compressed_keypoints, ('localhost', 12345))


#Sending descriptor data
size = sys.getsizeof(compressed_descriptors)
client.sendto(size.to_bytes(8, 'big'), ('localhost', 12345))
if size<65506:
    client.sendto(b'0', ('localhost', 12345))
    client.sendto(compressed_descriptors, ('localhost', 12345))
else:
    print("The data supplied is to big to send at a time! sending by data chuncks")
    client.sendto(b'1', ('localhost', 12345))
    with bz2.BZ2File('compressed_descriptor_UDP.pkl.bz2', 'wb', compresslevel=9) as f:
        pickle.dump(descriptor_data, f)
    file = open(r'E:\ISRO\VSSC\Fingerprint_analysis\fingerprint using client server\compressed_descriptor_UDP.pkl.bz2', 'rb')
    descriptor_data = file.read(2048)
    while descriptor_data:
        client.sendto(descriptor_data, ('localhost', 12345))
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
