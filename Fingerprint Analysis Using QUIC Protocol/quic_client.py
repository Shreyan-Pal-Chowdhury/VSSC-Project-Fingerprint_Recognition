import asyncio
import logging
import pickle
import cv2
import bz2

from aioquic.asyncio import connect, QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import HandshakeCompleted, StreamDataReceived

logging.basicConfig(level=logging.INFO)

class EchoClientProtocol(QuicConnectionProtocol):
    def quic_event_received(self, event):
        if isinstance(event, HandshakeCompleted):
            logging.info("Handshake completed with server")
            path = input("Enter the image path: ")

            file = open(path)
            sample = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

            sift = cv2.SIFT_create()

            keypoints, descriptor = sift.detectAndCompute(sample, None)

            keypoints_as_tuples = [(kp.pt, kp.size, kp.angle, kp.response, kp.octave, kp.class_id) for kp in keypoints]
            keypoints_data = pickle.dumps(keypoints_as_tuples)
            descriptor_data = pickle.dumps(descriptor)

            # Compression using Bz2
            compressed_keypoints = bz2.compress(keypoints_data)
            compressed_descriptors = bz2.compress(descriptor_data)
            print(compressed_keypoints)
            print(compressed_descriptors)

            self._quic.send_stream_data(0, compressed_keypoints)
            self._quic.send_stream_data(0, b'', end_stream=True)
            self._quic.send_stream_data(4, compressed_descriptors)
            self._quic.send_stream_data(4, b'', end_stream=True)


        elif isinstance(event, StreamDataReceived):
                print("data receiving")
                massege = event.data
                print(massege.decode())
                self._loop.stop()


async def main():
    configuration = QuicConfiguration(is_client=True)
    configuration.load_verify_locations('E:\ISRO\VSSC\Fingerprint_analysis\server.crt')
    async with connect("localhost", 12345, configuration=configuration, create_protocol=EchoClientProtocol) as protocol:
        await  protocol.wait_closed()
        #await asyncio.sleep(1)  # Keep the connection alive for a bit

if __name__ == "__main__":
    asyncio.run(main())
