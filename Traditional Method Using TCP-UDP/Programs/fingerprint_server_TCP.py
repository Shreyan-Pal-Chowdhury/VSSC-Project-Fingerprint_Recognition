import socket
import cv2
import os


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
print("Server binded")

# put a while loop which terminates on keyboard interrupt
# inside the body of the while loop put all the processing before sever.close()

server.listen()

# fork a child process for serving multiple clients

print("Now Listening")

client_socket, client_address = server.accept()

size = client_socket.recv(2048)

file = open('request_image.BMP','wb')
image_data = client_socket.recv(int.from_bytes(size, 'big'))

file.write(image_data)

file.close()


fingerprint_folder = r'E:\ISRO\VSSC\Fingerprint_analysis\Real_new'
sample_image_path = r'E:\ISRO\VSSC\Fingerprint_analysis\fingerprint using client server\request_image.BMP'

sample = cv2.imread(sample_image_path, cv2.IMREAD_GRAYSCALE)
print("image loaded")
if sample is None:
    print(f"Failed to load sample image: {sample_image_path}")
    exit(1)

best_score = 0
filename = None
best_image = None
kp1, kp2, mp = None, None, None

sift = cv2.SIFT_create()

keypoints_1, descriptors_1 = sift.detectAndCompute(sample, None)

for file in os.listdir(fingerprint_folder):
    fingerprint_image_path = os.path.join(fingerprint_folder, file)

    fingerprint_image = cv2.imread(fingerprint_image_path, cv2.IMREAD_GRAYSCALE)
    if fingerprint_image is None:
        print(f"Failed to load fingerprint image: {fingerprint_image_path}")
        continue

    # implement the below line on the client side
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

if best_image is not None:
    result = cv2.drawMatches(sample, kp1, best_image, kp2, mp, None)
    result = cv2.resize(result, None, fx=4, fy=4)
    cv2.imshow("Result", result)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()
    client_socket.send(b'Access Granted')

if filename is None:
    result_none = cv2.resize(sample, None, fx=4, fy=4)
    client_socket.send(b'Access Denied')
    cv2.imshow("Result",result_none)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()

server.close()
