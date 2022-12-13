from lib.socket_connector import SocketServer
import os
import wave
import pickle
import struct

class PyAudioStreamer:

    def __init__(self, port: int, host_ip: str, audio_filepath: str) -> None:
        self.port: int = port
        self.socket_server: SocketServer = SocketServer(self.port, host_ip)
        self.audio_filepath: str = audio_filepath

    def run(self) -> None:
        self.open_socket()
        self.stream_audio()

    def open_socket(self) -> None:
        print('Open socket.')
        self.socket_server.listen()

    def stream_audio(self) -> None:
        print('Stream audio.')
        chunk_size: int = 1024
        audio_file = wave.open(self.audio_filepath, 'rb')
        
        self.socket_server.accept()
        print('Client socket accepted.')
    
        data = None
        if self.socket_server.is_connected:
            while True:
                data = audio_file.readframes(chunk_size)
                if not data:
                    break
                serialized_data = pickle.dumps(data)
                message = struct.pack("Q",len(serialized_data))+serialized_data
                self.socket_server.send(message)
        print('Close socket and quit.')
        self.socket_server.close()
