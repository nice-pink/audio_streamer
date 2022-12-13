from lib.socket_connector import SocketClient
import pyaudio
import pickle
import struct
import time

class PyAudioReceiver:

    def __init__(self, port: int, host_ip: str) -> None:
        self.port: int = port
        self.socket_client: SocketClient = SocketClient(self.port, host_ip)

    def run(self) -> None:
        self.open_socket()
        self.receive_audio()

    def open_socket(self) -> None:
        print('Open socket.')
        self.socket_client.connect()

    def receive_audio(self) -> None:
        print('Receive audio.')
        p = pyaudio.PyAudio()
        chunk_size_stream: int = 1024
        stream = p.open(format=p.get_format_from_width(2),
                        channels=2,
                        rate=44100,
                        output=True,
                        frames_per_buffer=chunk_size_stream)
        
        data: bytearray = bytearray()
        payload_size = struct.calcsize("Q")

        chunk_size: int = 1024 * 4
        bytes_received: int = 0
        start = time.time()
        while True:
            try:
                while len(data) < payload_size:
                    packet = self.socket_client.read(chunk_size)
                    if not packet: break
                    data+=packet
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q",packed_msg_size)[0]
                while len(data) < msg_size:
                    data += self.socket_client.read(chunk_size)

                bytes_received += len(data)
                passed = time.time() - start
                print(bytes_received/passed, 'b/sec')

                frame_data = data[:msg_size]
                data  = data[msg_size:]
                frame = pickle.loads(frame_data)
                stream.write(frame)

            except:
                break

        self.socket_client.close()
        print('Socket closed')
