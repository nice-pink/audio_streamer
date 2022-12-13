import os
from lib.socket_connector import SocketConnector
import time

class DataReceiver:

    def __init__(self, port: int, host_ip: str, is_server: bool, data_handler = None) -> None:
        self.port: int = port
        self.is_server: bool = is_server
        self.data_handler = data_handler
        self.socket_connector: SocketConnector = SocketConnector(port, host_ip)

    def run(self) -> None:
        self.socket_connector.open_socket(self.is_server)
        self.receive_audio()

    def receive_audio(self) -> None:
        print('Receive data.')
        
        data: bytearray = bytearray()
        chunk_size: int = 1024
        bytes_received: int = 0

        start = time.time()
        while True:
            try:
                data = self.socket_connector.socket.read(chunk_size)
                if not data:
                    break
                
                bytes_received += len(data)
                passed = time.time() - start
                print(bytes_received/passed, 'b/sec')

                if self.data_handler:
                    self.data_handler.handle(data)
            except:
                break

        self.socket_connector.close()
        print('Socket closed')
        os._exit(1)
