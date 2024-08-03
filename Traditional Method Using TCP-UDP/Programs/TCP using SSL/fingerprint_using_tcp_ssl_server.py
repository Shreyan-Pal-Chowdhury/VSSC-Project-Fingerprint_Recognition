import pickle
import socket
import cv2
import os
import bz2
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile='E:\ISRO\VSSC\Fingerprint_analysis\server.crt', keyfile='E:\ISRO\VSSC\Fingerprint_analysis\server.key')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
print("Server binded")
count = 0
while True:
    if count==0:
        server.listen()
        print("Server listening")
    else:
        ssl_server.listen()

    if count==0:
        ssl_server = context.wrap_socket(server, server_side=True)

    count = count + 1
    client_socket, client_address = ssl_server.accept()

    size = client_socket.recv(2048)
    keypoints = client_socket.recv(int.from_bytes(size, 'big'))
    print(int.from_bytes(size, 'big'))
    print(keypoints)
    try:
        f = bz2.decompress(keypoints)
    except Exception as e:
        print(f"An exception occured {e}")
        client_socket.shutdown(socket.SHUT_RDWR)
        exit()

    try:
        keypoints_unpickled = pickle.loads(f)
    except Exception:
        print("File format not supported!")
        exit()

    keypoints_1 = [
        cv2.KeyPoint(
            x=pt[0][0], y=pt[0][1], size=pt[1],
            angle=pt[2], response=pt[3],
            octave=pt[4], class_id=pt[5],
        ) for pt in keypoints_unpickled if isinstance(pt[0], (tuple, list))
    ]
    keypoints_1 = tuple(keypoints_1)

    # Receiving descriptor data
    size = client_socket.recv(8)
    data_size = int.from_bytes(size, 'big')
    descriptors = client_socket.recv(data_size)
    print("received")

    try:
        f = bz2.decompress(descriptors)
    except Exception as e:
        print(f"An exception occured {e}")
        client_socket.shutdown(socket.SHUT_RDWR)
        exit()

    descriptors_1 = pickle.loads(f)

    fingerprint_folder = r'E:\ISRO\VSSC\Fingerprint_analysis\Real_new'

    best_score = 0
    filename = None
    best_image = None
    kp1, kp2, mp = None, None, None

    sift = cv2.SIFT_create()
    matcher = cv2.FlannBasedMatcher({'algorithm': 1, 'trees': 10}, {})

    for file in os.listdir(fingerprint_folder):
        fingerprint_image_path = os.path.join(fingerprint_folder, file)

        fingerprint_image = cv2.imread(fingerprint_image_path, cv2.IMREAD_GRAYSCALE)
        if fingerprint_image is None:
            print(f"Failed to load fingerprint image: {fingerprint_image_path}")
            continue

        keypoints_2, descriptors_2 = sift.detectAndCompute(fingerprint_image, None)
        matches = matcher.knnMatch(descriptors_1, descriptors_2, k=2)

        match_points = []
        for p, q in matches:
            if p.distance < 0.1 * q.distance:
                match_points.append(p)

        keypoints = min(len(keypoints_1), len(keypoints_2))
        score = len(match_points) / keypoints * 100 if keypoints > 0 else 0

        if score > best_score:
            best_score = score
            filename = file
            best_image = fingerprint_image
            kp1, kp2, mp = keypoints_1, keypoints_2, match_points

    print(f"BEST MATCH: {filename}")
    print(f"SCORE: {best_score}")

    if best_image is not None:
        client_socket.send(b'Access Granted')

    if filename is None:
        client_socket.send(b'Access Denied')