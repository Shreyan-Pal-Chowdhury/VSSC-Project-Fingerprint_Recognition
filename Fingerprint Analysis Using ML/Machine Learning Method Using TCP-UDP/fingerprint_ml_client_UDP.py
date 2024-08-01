import bz2
import pickle
import sys
import numpy as np
from sklearn.model_selection import train_test_split
from imgaug import augmenters as iaa
import socket


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

image = int(input("Enter the image: "))

x_real = np.load(r'E:\ISRO\VSSC\Fingerprint using ml\fingerprint analysis using ML and TCP UDP\x_real.npz')['data']
y_real = np.load(r'E:\ISRO\VSSC\Fingerprint using ml\fingerprint analysis using ML and TCP UDP\y_real.npy')
x_easy = np.load(r'E:\ISRO\VSSC\Fingerprint using ml\fingerprint analysis using ML and TCP UDP\x_easy.npz')['data']
y_easy = np.load(r'E:\ISRO\VSSC\Fingerprint using ml\fingerprint analysis using ML and TCP UDP\y_easy.npy')
x_medium = np.load(r'E:\ISRO\VSSC\Fingerprint using ml\fingerprint analysis using ML and TCP UDP\x_medium.npz')['data']
y_medium = np.load(r'E:\ISRO\VSSC\Fingerprint using ml\fingerprint analysis using ML and TCP UDP\y_medium.npy')
x_hard = np.load(r'E:\ISRO\VSSC\Fingerprint using ml\fingerprint analysis using ML and TCP UDP\x_hard.npz')['data']
y_hard = np.load(r'E:\ISRO\VSSC\Fingerprint using ml\fingerprint analysis using ML and TCP UDP\y_hard.npy')

print(x_real.shape, y_real.shape)

x_data = np.concatenate([x_easy, x_medium, x_hard], axis=0)
label_data = np.concatenate([y_easy, y_medium, y_hard], axis=0)

x_train, x_val, label_train, label_val = train_test_split(x_data, label_data, test_size=0.1)

print(x_data.shape, label_data.shape)
print(x_train.shape, label_train.shape)
print(x_val.shape, label_val.shape)

label_real_dict = {}

for i, y in enumerate(y_real):
    key = y.astype(str)
    key = ''.join(key).zfill(6)

    label_real_dict[key] = i


request_img = x_val[image]
request_label = label_val[image]

seq = iaa.Sequential([
    iaa.GaussianBlur(sigma=(0, 0.5)),
    iaa.Affine(
        scale={"x": (0.9, 1.1), "y": (0.9, 1.1)},
        translate_percent={"x": (-0.1, 0.1), "y": (-0.1, 0.1)},
        rotate=(-30, 30),
        order=[0, 1],
        cval=255
    )
], random_order=True)

request_img = seq.augment_image(request_img).reshape((1, 90, 90, 1)).astype(np.float32) / 255.

#Sending the image for matching
request_img_pkl = pickle.dump(request_img)
request_img_compressed = bz2.compress(request_img_pkl)
size = sys.getsizeof(request_img_compressed)
client.sendto(size.to_bytes(4, 'big'), ('localhost', 12345))
client.sendto(request_img_compressed, ('localhost', 12345))


print(client.recvfrom(1024).decode())

client.close()