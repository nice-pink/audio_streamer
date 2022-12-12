from lib.socket_connector import SocketConnector
from lib.stream_data import StreamData
import lib.byte_time_helper as byte_time_helper
import os
import time

class DataStreamer:

    def __init__(self, port: int, data: StreamData, is_server: bool, data_enricher = None, companion_sender = None) -> None:
        self.port: int = port
        self.is_server = is_server
        self.data_enricher = data_enricher
        if data_enricher:
            print('Has data enricher of type', type(data_enricher))
        self.companion_sender = companion_sender
        if companion_sender:
            print('Has companion sender of type', type(companion_sender))
        self.data: StreamData = data
        self.socket_connector: SocketConnector = SocketConnector(port)

    def run(self) -> None:
        self.socket_connector.open_socket(self.is_server)
        self.stream_data()

    def stream_data(self) -> None:
        send_byte_rate: int = self.data.audio_bitrate/8 # self.data.audio_bitrate/8000 * 1024
        print('Stream data with', send_byte_rate, 'bytes/sec')
        bytes_ahead: int = 0
        previous_time = None

        sent_file_index: int = 0

        index: int = 0
        while True:
            if index == self.data.portions:
                if self.companion_sender:
                    self.companion_sender.send(sent_file_index, end=True)
                index = 0
                sent_file_index += 1
                print(sent_file_index, 'times sent file.')
                # break
            
            if index == 0 and self.companion_sender:
                self.companion_sender.send(sent_file_index)

            now: time = time.time()

            # get offset
            if previous_time:
                bytes_ahead -= byte_time_helper.get_bytes(now - previous_time, send_byte_rate)
            previous_time = now

            # if data enricher -> enrich data
            if self.data_enricher:
                data = self.data_enricher.handle(self.data.file_portions[index])
            else:
                data = self.data.file_portions[index]
            
            # send data
            bytes_sent = self.socket_connector.socket.send(data)
            if bytes_sent > 0:
                bytes_ahead += bytes_sent

                # wait to keep data output rate
                if bytes_ahead > 0:
                    sleep_for: float = byte_time_helper.get_seconds(bytes_ahead, send_byte_rate)
                    # print('Sleep for sec:', sleep_for)
                    time.sleep(sleep_for)
                else:
                    print('No data sent.')
                    break
            index += 1

        self.socket_connector.close()
        print('Done sending data.')
