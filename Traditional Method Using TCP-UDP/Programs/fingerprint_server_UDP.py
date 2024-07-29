import socket
import time
import cv2
import os
import pickle
import bz2
import multiprocessing

def image_processing(total_received, total_descriptor, server, add):

    f = bz2.decompress(total_received)
    keypoints_decompossed = pickle.loads(f)
    keypoints_unpickled = pickle.loads(keypoints_decompossed)

    keypoints_1 = [
            cv2.KeyPoint(
                x=pt[0][0], y=pt[0][1], size=pt[1],
                angle=pt[2], response=pt[3],
                octave=pt[4], class_id=pt[5],
            ) for pt in keypoints_unpickled if isinstance(pt[0], (tuple, list))
        ]
    keypoints_1 = tuple(keypoints_1)
    print(keypoints_1)


    fd = bz2.decompress(total_descriptor)
    deccriptor_decompossed = pickle.loads(fd)
    descriptors_1 = pickle.loads(deccriptor_decompossed)
    print(descriptors_1)

    fingerprint_folder = r'E:\ISRO\VSSC\Fingerprint_analysis\Real_new'


    best_score = 0
    filename = None
    best_image = None
    kp1, kp2, mp = None, None, None

    sift = cv2.SIFT_create()

    for file in os.listdir(fingerprint_folder):
        fingerprint_image_path = os.path.join(fingerprint_folder, file)

        fingerprint_image = cv2.imread(fingerprint_image_path, cv2.IMREAD_GRAYSCALE)
        if fingerprint_image is None:
            print(f"Failed to load fingerprint image: {fingerprint_image_path}")
            continue

        keypoints_2, descriptors_2 = sift.detectAndCompute(fingerprint_image, None)

        matcher = cv2.FlannBasedMatcher({'algorithm': 1, 'trees': 10}, {})
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

    time.sleep(10)

    if best_image is not None:
        server.sendto(b'Access Granted', add)

    if filename is None:
        server.sendto(b'Access Denied', add)

if __name__=='__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('localhost', 12345))
    while True:
        print(multiprocessing.active_children())
        image_data, add = server.recvfrom(2048)

        total_received = b''

        # Receiving the Keypoints
        while image_data != b'0':
            total_received = total_received + image_data
            image_data, add = server.recvfrom(2048)
            print("receiving keypoints")

        # Receiving the descriptors
        descriptor_data, add = server.recvfrom(2048)
        total_descriptor = b''

        while descriptor_data != b'0':
            total_descriptor = total_descriptor + descriptor_data
            descriptor_data, add = server.recvfrom(2048)
            print("receiving descriptors")

        process = multiprocessing.Process(target=image_processing, args=(total_received, total_descriptor, server, add))
        process.start()

    server.close()
