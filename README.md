# Enhanced Fingerprint Biometric Security Framework Applying SIFT, Deep Learning & Robust Encryption with RSA, SSL/TLS through Modern Network Protocols 
Biometric identification, especially fingerprint recognition, is essential in modern security systems. Traditional algorithms like SIFT are robust in feature detection, handling scale, rotation, and partial fingerprints. However, deep learning, particularly CNNs, has revolutionized fingerprint recognition by automatically learning features from raw data, improving accuracy and resilience to distortions. Our work compares SIFT and CNN-based systems, showing that while SIFT performs well in controlled settings, CNNs excel in diverse conditions with superior accuracy. Security is enhanced with TLS, RSA encryption, and protocols like TCP, UDP, and QUIC. This highlights deep learning's potential to advance fingerprint recognition, making systems more reliable for security-critical applications.

## Dataset - 
The dataset consists of 6,000 authentic fingerprint images and their corresponding
augmented versions. The dataset is hierarchically structured, with images classified
into three difficulty levels (easy, medium, and hard) and further categorized by
alteration type (CR, OBL, and Zcut).
• CR: CR refers to a Central Roll fingerprint image, where the fingerprint is
captured with the finger rolling from the center outward.
• OBL: OBL indicates an Oblique fingerprint image, taken at an angle to the
fingerprint.
• Zcut: Zcut represents a Z-cut fingerprint image, which is a specific type of
oblique capture often used in forensic applications.

The dataset can be found at - https://www.kaggle.com/datasets/ruizgara/socofing

## Repository explanation -
Our normal fingerprint.py code contains the traditional implementation of fingerprint analysis using SIFT without any network protocols. It is a standalone file which runs the Conventional algorithm, scans a image and tries to match it with the existing database. If a match is found then it shows the request image and the matched image along with matched features. If match not found then only request image is shown.

The fingerprint analysis using ML directory contains one directory called Machine Learning method using TCP-UDP, which
contains four individual files and those are fingerprint_ml_client_TCP.py, fingerprint_ml_client_UDP.py,fingerprint_ml_server_TCP.py,fingerprint_ml_server_UDP.py. This files implements the machine learning methods using TCP, UDP protocols for remote access.
Again fingerprint analysis using ML directory there is a Fingerprint.ipynb file which implements the machine learning approach for fingerprint analysis using CNN. This file also contains the data preprocessing and model training part along with model evaluation part. 
Finally the above mentioned folder contains the saved model which has accuracy 99.67%. 

The Fingerprint Analysis Using QUIC Protocols contains four individual files along with one Outputs directory. Among this four files there are two python files which are quic_client.py, quic_server.py files which implements conventional method using QUIC protocols. The other two files (server.crt, server.key) are the cerficate and key which are used for establishing the connection (Handshake). The outputs directory contains two jpg files and those are quic_client_output.jpg, quic_server_output.jpg. These images shows the QUIC protocol outputs showcassing the access control from the server side.

The Outputs directory contains one directory called Python Profiler Outputs & a jpg file called BZ2 output & normal output size.jpg . The image shows the different sizes created by different compression techniques. The Python Profiler Outputs directory contains 4 jpg files called Optimized stats.jpg, Pycharm output.jpg, Tuna output.jpg, normal_stats.jpg . The optimized stats.jpg file shows the time efficiency caused by the implementation of multiprocessing. The Pycharm output.jpg file shows further time optimization. The Tuna output.jpg shows a visual representation of time division caused by different function calls. The normal_stats.jpg shows the time caused by different function calls before the implementation of multiprocessing.

The Traditional Method Using TCP-UDP contains two sub directory which are outputs & Programs.
The program directory contains 4 individual python files which are fingerprint_client_TCP.py, fingerprint_client_UDP.py, fingerprint_server_TCP.py, fingerprint_server_UDP.py & 2 sub directories Fingerprint Analysis Using TCP-UDP and encryption & TCP using SSL. The 4 individual python files implements the conventional method using TCP and UDP protocols for remote access. The Fingerprint Analysis Using TCP-UDP and encryption sub directory contains 6 individual files. Among these the 4 python files use RSA encryption for client authentication. And the other 2 pickle files are privateKey.pickle and publicKey.pickle are the pickled version of the private and public key. The sub directory TCP using SSL contains 4 individual files. Among these two python files implement the TCP protocol using SSL. The other 2 files are the certificate & key files used for SSL verification.
The oputput sub directory contains 8 individual jpg files. Among these 4 files show the cases for granted and denied access in TCP. The two files show the UDP client server outputs. The other two files show the implementations of multiprocessing in TCP and UDP for multiple client processing at a time. 
