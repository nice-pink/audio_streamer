from data_streamer.data_streamer import DataStreamer
from lib.stream_data import StreamData
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please define port as argument.')
        sys.exit(1)
    port: int = int(sys.argv[1])
    data: StreamData = StreamData('test_files/sweep_5sec.mp3', 320000)
    data.prepare()
    data_streamer: DataStreamer = DataStreamer(port, data, is_server=True)
    data_streamer.run()
