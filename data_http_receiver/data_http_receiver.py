import requests
import time

class DataHttpReceiver:

    def __init__(self, url: str, headers: dict, data_handler = None) -> None:
        self.url: str = url
        self.headers: dict = headers
        self.data_handler = data_handler

    def run(self) -> None:
        self.receive_data()

    def receive_data(self) -> None:
        print('Receive data.')
        
        bytes_received: int = 0
        chunk_size: int = 1024
        start: time = time.time()
        
        session = requests.Session()
        with session.head(self.url, headers=self.headers, timeout=20, allow_redirects=True) as response:
            if self.data_handler:
                self.data_handler.update(response.headers)

        with session.get(self.url, headers=self.headers, stream=True, timeout=20, allow_redirects=True) as response:
            for line in response.iter_content(chunk_size=chunk_size, decode_unicode=True):
                bytes_received += len(line)
                passed = time.time() - start
                print(bytes_received/passed, 'b/sec')

                if self.data_handler:
                    self.data_handler.handle(line)
        print('Connection closed')
