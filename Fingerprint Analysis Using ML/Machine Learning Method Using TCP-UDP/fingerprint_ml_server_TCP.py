import bz2
import numpy as np
import pickle
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
print("Server binded")

server.listen()
print("Now Listening")
client_socket, client_address = server.accept()

#Receiving the image
size = client_socket.recv(4)
request_img_compressed = client_socket.recv(int.from_bytes(size, 'big'))
request_img_pkl = bz2.decompress(request_img_compressed)
request_img = pickle.load(request_img_pkl)

x_real = np.load(r'E:\ISRO\VSSC\Fingerprint using ml\fingerprint analysis using ML and TCP UDP\x_real.npz')['data']
y_real = np.load(r'E:\ISRO\VSSC\Fingerprint using ml\fingerprint analysis using ML and TCP UDP\y_real.npy')


label_real_dict = {}

for i, y in enumerate(y_real):
    key = y.astype(str)
    key = ''.join(key).zfill(6)

    label_real_dict[key] = i


model = pickle.load(open(r'E:\ISRO\VSSC\Fingerprint using ml\fingerprint analysis using ML and TCP UDP\model_saved', 'rb'))

max_score = 0

for match_key in label_real_dict:
  rx = x_real[label_real_dict[match_key]].reshape((1, 90, 90, 1)).astype(np.float32) / 255.
  ry = y_real[label_real_dict[match_key]]

  pred_rx = model.predict([request_img, rx])

  if pred_rx > max_score:
    max_score = pred_rx
    best_match = rx
    best_label = ry


if best_match is not None:
    client_socket.send(b'Access Granted')

else:
    client_socket.send(b'Access Denied')

server.close()