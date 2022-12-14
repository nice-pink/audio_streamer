from typing import List
from lib.socket_connector import SocketConnector
import time

class DataReceiver:

    def __init__(self,
                 port: int,
                 host_ip: str,
                 is_server: bool,
                 data_handler = None,
                 metrics_handler = None) -> None:
        self.port: int = port
        self.is_server: bool = is_server
        self.data_handler = data_handler
        self.socket_connector: SocketConnector = SocketConnector(port, host_ip)
        self.metrics_handler = metrics_handler

    def run(self) -> None:
        self.socket_connector.open_socket(self.is_server)
        self.receive_data()

    def receive_data(self) -> None:
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
                    if self.metrics_handler:
                        metrics: List[str] = self.data_handler.get_metrics()
                        for metric in metrics:
                            self.metrics_handler.increase(metric)
            except:
                break

        self.socket_connector.close()
        print('Socket closed')

    @staticmethod
    def get_supported_metric() -> List[str]:
        return ['bytes_received', 'cycles']
